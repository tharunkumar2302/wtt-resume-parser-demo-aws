from flask import Flask, jsonify, request,make_response
import pinecone
import openai
from openai.embeddings_utils import get_embedding
# import jsonpickle
from main import ResumeParser,resume_parser
from flask_cors import CORS
from connection import s3_client,resumeDetailsCollection
from config import AWS_S3_BUCKET_NAME,API_KEY,PINECONE_API_KEY,PINECONE_ENVIRONMENT,EMBEDDING_MODEL,PINECONE_INDEX_NAME
import os
from logger import logging
import json
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import re
from bson import ObjectId,Decimal128


openai.api_key=API_KEY#'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'
pinecone_api_key = PINECONE_API_KEY#"ad5d67cd-e301-407a-a5f8-f276846d7154"#"c9b87bce-2944-4e8a-bd47-58b730f1063e"
environment = PINECONE_ENVIRONMENT#"us-west4-gcp-free"#"us-west1-gcp-free"
index_name = PINECONE_INDEX_NAME
embedding_model = EMBEDDING_MODEL#"text-embedding-ada-002"

MODEL_NAME="gpt-3.5-turbo"

from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to its string representation
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO format
        if isinstance(obj, Decimal128):
            return float(str(obj))
        return super().default(obj)
app = Flask(__name__)
CORS(app)	

def transform_response(match):
    new_match = {
    "id": str(ObjectId(match["_id"])),  # match["pinecone_mongo_uuid_val"],
    "metadata": {
        "About": match.get("About", ""),  
        "Text": f"{match.get('firstName', '')} {match.get('lastName', '')} {match.get('email', '')} {match.get('experience', '')}",
        "company_name": match.get("current_company", ""),  
        "createdAt": match.get("createdAt", ""),  
        "createdByUserId": str(ObjectId(match["createdByUserId"])),  
        "createdByUserRole": str(ObjectId(match["createdByUserRole"])),  
        "current_company": match.get("current_company", ""),  
        "current_ctc": match.get("current_ctc", ""),  
        "current_designation": match.get("current_designation", ""),  
        "current_employment_status": match.get("current_employment_status", ""),  
        "current_location": match.get("current_location", ""),  
        "cv_url": match.get("cv_url", ""),  
        "date_of_birth": match.get("date_of_birth", ""),  
        "date_of_joining": match.get("experience_details[0].date_of_joining", ""),  
        "description": match.get("experience_details[0].description", ""),  
        "education": match.get("education", ""),  
        "email": match.get("email", ""),  
        "employment_type": match.get("experience_details[0].employment_type", ""),  
        "expected_ctc": match.get("expected_ctc", ""),  
        "experience": match.get("experience", ""),  
        "file_path": match.get("file_path", ""),  
        "firstName": match.get("firstName", ""),  
        "having_passport": match.get("having_passport", ""),  
        "headline": match.get("experience_details[0].headline", ""),  
        "industry": match.get("experience_details[0].industry", ""),  
        "institute": match.get("education_details[0].institute", ""),  
        "isActive": match.get("isActive", ""),  
        "is_cv_uploaded": match.get("is_cv_uploaded", ""),  
        "job_title": match.get("experience_details[0].job_title", ""),  
        "lastName": match.get("lastName", ""),  
        "last_date": match.get("experience_details[0].last_date", ""),  
        "company_location": match.get("experience_details[0].company_location", ""),  
        "marital_status": match.get("marital_status", ""),  
        "marks_in_percentage": match.get("education_details[0].marks_in_percentage", ""),  
        "modifiedByUserId": str(ObjectId(match["modifiedByUserId"])),  
        "modifiedByUserRole": str(ObjectId(match["modifiedByUserRole"])),  
        "notice_period": match.get("notice_period", ""),  
        "organization": str(ObjectId(match["organization"])),  
        "overseas_experience": match.get("overseas_experience", ""),  
        "passport_validity": match.get("passport_validity", ""),  
        "phone_no": match.get("phone_no", ""),  
        "pinecone_mongo_uuid_val": match.get("pinecone_mongo_uuid_val", ""),  
        "prefered_location": match.get("prefered_location", ""),  
        "present_address": match.get("present_address", ""),  
        "primary_skill":",".join(match.get("primary_skill","")) if match.get("primary_skill","") else " ",  # Provide an empty list as default
        "qualification": match.get("education_details[0].qualification", ""),  
        "ready_to_relocate": match.get("ready_to_relocate", ""),  
        "resume_id": str(ObjectId(match["_id"])),  # match["_id"],
        "secondary_skill": match.get("secondary_skill", ""),  
        "source": match.get("source", ""),  
        "specialization": match.get("education_details[0].specialization", ""),  
        "status": match.get("status", ""),  
        "updatedAt": match.get("updatedAt", ""),  
        "uploaded_by": match.get("uploaded_by", ""),  
        "visa": match.get("visa", ""),  
        "year_of_passing": match.get("education_details[0].year_of_passing", ""),  
    },
    "score": 0.85
}

    return new_match

# #http://0.0.0.0:5000/job_opening?current_location=Delhi&organization_id=64e87ca35c8c0229aeacc266&primary_skill=Python,Machine Learning,Nodejs&education=MBA&min_experience=1&max_experience=10&notice_period=1.5&status=Published&industry=IT   
@app.route('/job_opening', methods=['GET'])
def job_opening():
    try:
        logging.info("Entered into job_opening")

        if request.method == 'GET':
            try:
                print("try")
                current_location = request.args.getlist('current_location', []) 
            except:
                print("except")
                current_location = request.args.get('current_location',[]) 

            organization_id = request.args.get('organization_id', "")
            try:
                print("try")
                primary_skill = request.args.getlist('primary_skill', [])
            except:
                print("except")
                primary_skill = request.args.get('primary_skill', [])
            education = request.args.get('education', "")
            min_experience = request.args.get('min_experience', "")
            max_experience = request.args.get('max_experience', "")
            notice_period = request.args.get('notice_period', "")
            status = request.args.get('status', "")
            industry = request.args.get('industry', "")
            print("current_location:",current_location)
            print(type(current_location))
            print("organization_id:",organization_id)
            print("primary_skill:",primary_skill)
            print("education:",education)
            print("min_experience:",min_experience)
            print("max_experience:",max_experience)
            print("notice_period:",notice_period)
            print("status:",status)
            print("industry:",industry)
            # current_location=list(current_location)
            # primary_skill=list(primary_skill)
            # Correct the code to remove extra spaces from the list
            # current_location = list(map(str.strip, current_location.split(',')))
            # primary_skill = list(map(str.strip, primary_skill.split(',')))
            print(type(current_location))
            print(type(primary_skill))
            

            keyword_query = []
            res = {}

            if current_location:
                print(current_location)
                print(len(current_location))
                curr_location=current_location.split(",")
                print(curr_location)
                print(len(curr_location))
                print(type(curr_location))
                if len(curr_location)>1:
                    location_queries = [{"current_location": {"$regex": location, "$options": "i"}} for location in curr_location]
                    keyword_query.extend(location_queries)
                else:
                    location_queries = {"current_location": {"$regex": current_location, "$options": "i"}}
                    keyword_query.append(location_queries)
              
            if primary_skill:
                primary_skill_list=primary_skill.split(",")
                print(primary_skill_list)
                print(type(primary_skill_list))
                if len(primary_skill_list)>1:
                    skill_queries = [{"primary_skill": {"$regex": skill, "$options": "i"}} for skill in primary_skill_list]
                    keyword_query.extend(skill_queries)
                else:
                    skill_queries = {"primary_skill": {"$regex": primary_skill, "$options": "i"}}
                    keyword_query.append(skill_queries)
                
               

                # skill_queries = [{"primary_skill": {"$regex": skill, "$options": "i"}} for skill in primary_skill[0].split(",")]
                # keyword_query.extend(skill_queries)
            if organization_id:
                res["organization"] = ObjectId(organization_id)
            if education:
                keyword_query.append({"education": {"$regex": education, "$options": "i"}})
            if status:
                keyword_query.append({"status": {"$regex": status, "$options": "i"}})
            if industry:
                keyword_query.append({"industry": {"$regex": industry, "$options": "i"}})

            if min_experience or max_experience:
                res["experience"]={"$gte": min_experience, "$lte": max_experience}

            if notice_period:
                value = str(notice_period).split()[0]
                keyword_query.append({"notice_period": {"$regex": value, "$options": "i"}})


            res["$and"] = keyword_query
            print("res :",res)

            mycollection = resumeDetailsCollection()
            obj=mycollection.find(res)
            records=[]
            for record in obj:
                records.append(record)
            if records:
                records=records[:10]

            exact_match = []
            for resp in range(len(records)):
                print("resp:",resp)
                # new_response["response"]["results"][0]["matches"]
                exact_match.append(transform_response(records[resp]))

            results_dict = {'results': [{'matches': exact_match}]}
            results_dict = {'response': results_dict}

            json_data = json.dumps(results_dict, cls=CustomJSONEncoder)

            
            json_data = json.loads(json_data)
            logging.info(f"data: {json_data}")

            print("in if condition")
            logging.info("in if condition")
            # return jsonify(json_data)
            print(json_data)
            # if results_dict['response']['results'][0]['matches']:
            #     print("inside if condition")
            return jsonify(json_data)

           

    except Exception as e:
        print("error:",e)
        logging.info("error:",e)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
