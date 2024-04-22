from flask import Flask, jsonify, request,make_response
import pinecone
import openai
# from openai.embeddings_utils import get_embedding
# import jsonpickle
from main import ResumeParser,resume_parser
from flask_cors import CORS
from connection import s3_client,resumeDetailsCollection
from config import AWS_S3_BUCKET_NAME,API_KEY,PINECONE_API_KEY,PINECONE_ENVIRONMENT,EMBEDDING_MODEL,PINECONE_INDEX_NAME
import os
from logger import logging
import json
# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import re
from bson import ObjectId,Decimal128
from utils import contains_days, contains_month, contains_year, contains_week
from nlp_search_using_groq import nlp_using_groq
from openai import OpenAI
client = OpenAI(api_key=API_KEY)

openai.api_key=API_KEY#'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'
pinecone_api_key = PINECONE_API_KEY#"ad5d67cd-e301-407a-a5f8-f276846d7154"#"c9b87bce-2944-4e8a-bd47-58b730f1063e"
environment = PINECONE_ENVIRONMENT#"us-west4-gcp-free"#"us-west1-gcp-free"
index_name = PINECONE_INDEX_NAME
embedding_model = EMBEDDING_MODEL#"text-embedding-ada-002"

MODEL_NAME="gpt-3.5-turbo"

import json
from bson import ObjectId
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

def entity_extract(formatted_text):
    llm = ChatOpenAI(model_name=MODEL_NAME,temperature=0,openai_api_key=openai.api_key)
    # Few-shot learning prompt
    prompt = """You are a recruitment specialist. Given an input text or query, you will always extract the requested information in the below JSON format.
    Please extract the following information using the given names ONLY:
    - firstName:extract First Name from text if present else return an empty string e.g:""
    - lastName:extract Last Name from text if present else return an empty string  e.g:"" 
    - phone_no:extract Mobile number from text if present else return an empty string  e.g:""
    - current_location: return where he is living else return an empty string  e.g:"" 
    - primary_skill: return whatever skills are there else return an empty string  e.g:""
    - current_company: return the company name from text else return an empty string e.g:""
    - current_designation: return the designation name from text else return an empty string e.g:""
    - notice_period: return the notice period information from the text. Specify whether it's '$lt,' '$gt,' or just a certain number of months ,return in the format to filter in the MongoDB.
    - experience: Extract the years of experience information from the text. If the experience is in months, do not return any number. If the experience is specified in years, return the number of years in the format to filter in MongoDB, including whether it is $lt (less than), $gt (greater than), or just a certain number of years.
    if multiple Locations or Primary Skills or Company add in single json.
    Example JSON if text present: 
        "firstName": firstName in the format of string,
        "lastName": lastName in the format of string,
        "phone_no": phone_no in the format of string,
        "current_location": current_location in the format of list of strings e.g ["Hyderabad", "Bangalore, "Chennai"],
        "primary_skill": primary_skill in the format of list of strings e.g ["Python","Java","Html","css"],
        "current_company":current_company in the format of list of strings e.g ["TCS","Infosys","Microsoft","Google","Walking Tree Technologies"]
        "current_designation": current_designation in the format of list of strings e.g ["Software Engineer","Data Scientist","Data Engineer","Devops Engineer"]
        "notice_period":'$eq 4' or '$lt 2' or '$gt 1' or 2 or '$eq 6.5' or '$lt 1.5' or '$gt 10.5' or 2.5
        "experience":'$eq 3' or '$lt 6' or '$gt 8' or 6 or '$eq 10.5' or '$lt 7.5' or '$gt 5.5' or 1.5


    The given text is:{formatted_text}.
    Result Json is :"""
    #in Example JSON if text not present return empty string for perticular key.
    # Create a prompt template
    prompt_template = PromptTemplate(input_variables=["formatted_text"], template=prompt)
    # Create an LLMChain
    extract_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="response")
    # Run the chain
    resp = extract_chain.run(formatted_text=formatted_text)
    # Parse the response
    print(resp)
    response = json.loads(resp)
    return response

def notice_period_process(notice_period,period,res):
    try:
        if len(str(notice_period).split())>1:
            try:
                value = int(str(notice_period).split()[1])
                comparison = str(notice_period).split()[0]
                res[f"{period}"] = {str(comparison): value}
            except:
                res[f"{period}"] = int(str(notice_period).split()[0])
        else:
            res[f"{period}"] = int(notice_period)
    except:
        if len(str(notice_period).split())>1:
            try:
                value = float(str(notice_period).split()[1])
                comparison = str(notice_period).split()[0]
                res[f"{period}"] = {str(comparison): value}
            except:
                res[f"{period}"] = float(str(notice_period).split()[0])
        else:
            res[f"{period}"] = float(notice_period)

def key_word_search_with_len(query,phone_no,experience,organization_id,notice_period):
    try:
        keyword_query = []
        print("key_word_search_with_len")

        # Construct the keyword_query for fields with values
        
        keyword_query.append({"firstName": {"$regex": query, "$options": "i"}})
        keyword_query.append({"lastName": {"$regex": query, "$options": "i"}})
        # Add more fields as needed

        # Construct the keyword_query for locations
        keyword_query.append({"current_location": {"$regex": query, "$options": "i"}})
        keyword_query.append({"current_company": {"$regex": query, "$options": "i"}})
        keyword_query.append({"current_designation": {"$regex": query, "$options": "i"}})
        keyword_query.append({"notice_period": {"$regex": query, "$options": "i"}})



        # Construct the keyword_query for skills  current_designation
        keyword_query.append({"primary_skill": {"$regex": query, "$options": "i"}})

        # Construct the final query
        res = {}

        if ' and ' in query or ',' in query:
            print("in combination if keyword")
            if keyword_query:
                res["$and"] = keyword_query
        else:
            print("in combination else keyword")
            if keyword_query:
                res["$or"] = keyword_query

        # if keyword_query:
        #     res["$or"] = keyword_query
            
        if phone_no:
            res["phone_no"] = str(phone_no)

        if notice_period:
            if type(notice_period) == dict:
                res['notice_period'] = notice_period
            else:
                try:
                    if contains_month(str(notice_period)):
                        period="notice_period_in_month"
                        notice_period_process(notice_period,period,res)
                        # res["notice_period_in_month"]=str(notice_period).split()[0]
                    elif contains_year(str(notice_period)):
                        period="notice_period_in_year"
                        notice_period_process(notice_period,period,res)
                        # res["notice_period_in_year"]=str(notice_period).split()[0]
                    elif contains_days(str(notice_period)):
                        period="notice_period_in_days"
                        notice_period_process(notice_period,period,res)
                        # res["notice_period_in_days"]=str(notice_period).split()[0]
                    elif contains_week(str(notice_period)):
                        period="notice_period_in_week"
                        notice_period_process(notice_period,period,res)

                except:
                    try:
                        if len(str(notice_period).split())>1:
                            try:
                                value = int(str(notice_period).split()[1])
                                comparison = str(notice_period).split()[0]
                                res["notice_period"] = {str(comparison): value}
                            except:
                                res["notice_period"] = int(str(notice_period).split()[0])
                        else:
                            res["notice_period"] = int(notice_period)
                    except:
                        if len(str(notice_period).split())>1:
                            try:
                                value = float(str(notice_period).split()[1])
                                comparison = str(notice_period).split()[0]
                                res["notice_period"] = {str(comparison): value}
                            except:
                                res["notice_period"] = float(str(notice_period).split()[0])
                        else:
                            res["notice_period"] = float(notice_period)

                # res["notice_period"] = int(notice_period)
            
        if experience:
            if type(experience) == dict:
                res["experience" ]= experience
            else:
                try:
                    if len(str(experience).split())>1:
                        value = int(str(experience).split()[1])
                        if value==0:
                            res["experience"] = 0
                        else:
                            comparison = str(experience).split()[0]
                            res["experience"] = {str(comparison): value}
                    else:
                        res["experience"] = int(experience)
                except:
                    if len(str(experience).split())>1:
                        value = float(str(experience).split()[1])
                        if value==0:
                            res["experience"] = 0
                        else:
                            comparison = str(experience).split()[0]
                            res["experience"] = {str(comparison): value}
                    else:
                        res["experience"] = float(experience)
                
            
        if keyword_query or phone_no or experience or notice_period:
            if organization_id:
                res["organization"] = ObjectId(organization_id)
        mycollection,conn = resumeDetailsCollection()
        if not conn:
            print("======connection not established=============")
        print(mycollection,conn)
        obj=mycollection.find(res)
        records=[]
        print("obj=========",obj)
        records = [record for record in obj]
        # for record in obj:
        #     records.append(record)
        print("records=========",records)
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

        print("in elif condition")
        logging.info("in elif condition")
        print(json_data)
        # return jsonify(json_data)
        return json_data
    finally:
        conn.close()

# def get_embedding(text, model="text-embedding-3-small"):
#     text = text.replace("\n", " ")
#     return client.embed(model, text).embedding
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def transform_response_pinecone(match):
    # Remove the 'location' column if present
    if 'location' in match["metadata"]:
        del match["metadata"]["location"]

    # Convert 'primary_skill' list to string
    match["metadata"]["primary_skill"] = ", ".join(match["metadata"]["primary_skill"])

    # Convert 'secondary_skill' list to string
    match["metadata"]["secondary_skill"] = ", ".join(match["metadata"]["secondary_skill"])

    # Convert date format for 'createdAt' column
    if 'createdAt' in match["metadata"]:
        created_at = match["metadata"]["createdAt"]
        match["metadata"]["createdAt"] = datetime.strftime(created_at, "%Y-%m-%dT%H:%M:%S.%f")

    # Convert date format for 'updatedAt' column
    if 'updatedAt' in match["metadata"]:
        updated_at = match["metadata"]["updatedAt"]
        match["metadata"]["updatedAt"] = datetime.strftime(updated_at, "%Y-%m-%dT%H:%M:%S.%f")

    return match

def pinecone_search(query,organization_id,firstName,lastName,phone_no,locations,current_company,skills,current_designation,notice_period):
    # phrase_embedding = get_embedding(str(query), engine=embedding_model)
    phrase_embedding = get_embedding(str(query), model=embedding_model)
    # print(phrase_embedding)

    print("pinecone_search")
    top_k = 5  # Number of nearest neighbors to retrieve
    
    filter_conditions = []

    if organization_id:
        filter_conditions.append({"organization": {"$eq": str(organization_id)}})

    if firstName:
        filter_conditions.append({"firstName": {"$eq": str(firstName).capitalize()}})

    if lastName:
        filter_conditions.append({"lastName": {"$eq": str(lastName).capitalize()}})

    if phone_no:
        filter_conditions.append({"phone_no": {"$eq": str(phone_no)}})

    if notice_period:
        if type(notice_period) == dict:
            filter_conditions.append({"notice_period": notice_period})
        else:
            filter_conditions.append({"notice_period": {"$eq": str(notice_period)}})
    

    # Filter by multiple locations
    if locations:
        location_filters = [{"current_location": {"$in": [str(loc).capitalize() for loc in str(locations).split(",")]}}]
        print("location_filters:",location_filters)
        filter_conditions.extend(location_filters)

    if current_company:
        company_filters = [{"current_company": {"$in": [str(company).capitalize() for company in str(current_company).split(",")]}}]
        print("company_filters:",company_filters)
        filter_conditions.extend(company_filters)
    
    if current_designation:
        designation_filters = [{"current_designation": {"$in": [str(designation).capitalize() for designation in str(current_designation).split(",")]}}]
        print("company_filters:",designation_filters)
        filter_conditions.extend(designation_filters)

    # Filter by multiple skills
    if skills:
        skill_filters = [{"primary_skill": {"$in": [str(skill).capitalize() for skill in str(skills).split(",")]}}]
        filter_conditions.extend(skill_filters)

    # Combine all conditions with the $and operator
    if ' and ' in query or ',' in query:
        print("in combination if keyword")
        filter_query = {"$and": filter_conditions}
    else:
        print("in combination else keyword")
        filter_query = {"$or": filter_conditions}


    # filter_query = {"$and": filter_conditions}
    logging.info(f'filter_query : {filter_query}')


    pinecone.init(api_key=pinecone_api_key, environment=environment)
    index = pinecone.Index(index_name=index_name)
    results = index.query(queries=[phrase_embedding], filter=filter_query, top_k=top_k, include_metadata=True)
    exact_match = []
    
    for resp in range(len(results.results[0].matches)):
        match = results.results[0].matches[resp]
        metadata = match.get("metadata", {})  # Get the existing metadata (or an empty dictionary if not present)
        primary_skills = match.get("primary_skill", [])  # Get the primary skills (or an empty list if not present)
        
        # Add "primary_skill" to metadata if it exists
        if primary_skills:
            metadata["primary_skill"] = ", ".join(primary_skills)
        
        match_data = {
            "id": match.id,
            "score": match.score,
            "metadata": metadata,
        }
        company_location = match_data.get("metadata.company_location", "")
        # If 'company_location' is not present, set a default value
        if not company_location:
            company_location = " "  # You can change this default value as needed
        # Add 'company_location' to the metadata dictionary
            match_data["metadata"]["company_location"] = company_location

        match_data = transform_response_pinecone(match_data)
        exact_match.append(match_data)

        

    results_dict = {'results': [{'matches': exact_match}]}

    print("in else condition")
    logging.info("in else condition")
    print(type(jsonify({'response': results_dict})))
    # return jsonify({'response': results_dict})
    return {'response': results_dict}

def transform_response(match):
    new_match = {
    "id": str(ObjectId(match["_id"])),  # match["pinecone_mongo_uuid_val"],
    "metadata": {
        "About": match.get("About", ""),  
        "Text": f"{match.get('firstName', '')} {match.get('lastName', '')} {match.get('email', '')} {match.get('experience', '')}",
        "company_location": match.get("experience_details[0].company_location", ""),
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
        # "company_location": match.get("experience_details[0].company_location", ""),  
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
    company_location = match.get("experience_details[0].company_location", "")

    # If 'company_location' is not present, set a default value
    if not company_location:
        company_location = " "  # You can change this default value as needed

    # Add 'company_location' to the metadata dictionary
    new_match["metadata"]["company_location"] = company_location
    print(new_match)

    return new_match

files_processed = []
files_in_process = set()

@app.route('/', methods=['POST'])
def get_path():   
    if request.method == 'POST':
        filepath = request.json.get('filename')  # Get the query parameter from the URL
        # data=resume_parser()
        if filepath in files_processed:
            return jsonify({'status': 'File already processed'})

        # Check if the file is already in process
        if filepath in files_in_process:
            return jsonify({'status': 'File is already in process'})
        
        try:
            logging.info("entered into try in get_path")
            mycollection, conn = resumeDetailsCollection()
            obj = mycollection.find({"file_path": str(filepath)})
            records = []
            for record in obj:
                records.append(record)
            if not records:
                logging.info("filepath: %s", filepath)
                filename = str(filepath).split("/")[-1]
                logging.info("filename: %s", filename)
                
                # Mark the file as in process
                files_in_process.add(filepath)
                
                s3_client.download_file(AWS_S3_BUCKET_NAME, filepath, filename)
                data = ResumeParser(filename, filepath).get_extracted_data()

                logging.info("Entered before return")
                try:
                    os.remove(filename)
                except:
                    pass
                
                files_processed.append(filepath)
                # Remove the file from the files in process set
                files_in_process.remove(filepath)
                
                return jsonify({'response': data})
        finally:
            conn.close()

     
@app.route('/fetch_result', methods=['GET'])
def main():
    try:
        logging.info("Entered into main")
        
        if request.method == 'GET':
            print("length==>:",len(request.args))
            if len(request.args) <=2:
                query = request.args.get('query')  # Get the query parameter from the URL
                organization_id = request.args.get('org_id')
                
                logging.info("added=========================")
                logging.info(f'query : {query}')
                logging.info(f'organization_id : {organization_id}')
                logging.info("=========================")

                formatted_text = str(query)
                response=nlp_using_groq(formatted_text)
                print(response)
                print(type(response))
                if response==None:
                    logging.info(f'response in if: {response}')
                    response = entity_extract(formatted_text)


                # response = entity_extract(formatted_text)
                logging.info(f'response : {response}')

                firstName = response.get("firstName", "")
                lastName = response.get("lastName", "")

                phone_no = response.get("phone_no", "")
                notice_period = response.get("notice_period", "")
                print("notice_period:", notice_period)

                # Extract multiple locations and skills if present
                locations = response.get("current_location","")
                current_company=response.get("current_company", "")
                current_designation=response.get("current_designation", "")
                skills = response.get("primary_skill","")
                experience = response.get("experience","")

                # Initialize the $or list for keyword queries
                keyword_query = []

                # Construct the keyword_query for fields with values
                if firstName:
                    keyword_query.append({"firstName": {"$regex": firstName, "$options": "i"}})
                if lastName:
                    keyword_query.append({"lastName": {"$regex": lastName, "$options": "i"}})
                # Construct the keyword_query for locations
                location_queries = [{"current_location": {"$regex": location, "$options": "i"}} for location in locations]

                current_company_queries = [{"current_company": {"$regex": company, "$options": "i"}} for company in current_company]            # Construct the keyword_query for skills
                current_designation_queries = [{"current_designation": {"$regex":designation, "$options": "i"}} for designation in current_designation]
                skill_queries = [{"primary_skill": {"$regex": f'^{skill}$', "$options": "i"}} for skill in skills]

                # Combine all keyword queries using $or
                keyword_query.extend(location_queries)
                keyword_query.extend(skill_queries)
                keyword_query.extend(current_company_queries)
                keyword_query.extend(current_designation_queries)

                # Construct the final query
                res = {}

                if ' and ' in query or ',' in query:
                    print("in combination if keyword")
                    if keyword_query:
                        res["$and"] = keyword_query
                else:
                    print("in combination else keyword")
                    if keyword_query:
                        res["$or"] = keyword_query

                if phone_no:
                    res["phone_no"] = str(phone_no)

                if notice_period:
                    if type(notice_period) == dict:
                        res['notice_period'] = notice_period
                    else:
                        try:
                            if contains_month(str(notice_period)):
                                period="notice_period_in_month"
                                notice_period_process(notice_period,period,res)
                                # res["notice_period_in_month"]=str(notice_period).split()[0]
                            elif contains_year(str(notice_period)):
                                period="notice_period_in_year"
                                notice_period_process(notice_period,period,res)
                                # res["notice_period_in_year"]=str(notice_period).split()[0]
                            elif contains_days(str(notice_period)):
                                period="notice_period_in_days"
                                notice_period_process(notice_period,period,res)
                                # res["notice_period_in_days"]=str(notice_period).split()[0]
                            elif contains_week(str(notice_period)):
                                period="notice_period_in_week"
                                notice_period_process(notice_period,period,res)

                        except:
                            try:
                                if len(str(notice_period).split())>1:
                                    try:
                                        value = int(str(notice_period).split()[1])
                                        comparison = str(notice_period).split()[0]
                                        res["notice_period"] = {str(comparison): value}
                                    except:
                                        res["notice_period"] = int(str(notice_period).split()[0])
                                else:
                                    res["notice_period"] = int(notice_period)
                            except:
                                if len(str(notice_period).split())>1:
                                    try:
                                        value = float(str(notice_period).split()[1])
                                        comparison = str(notice_period).split()[0]
                                        res["notice_period"] = {str(comparison): value}
                                    except:
                                        res["notice_period"] = float(str(notice_period).split()[0])
                                else:
                                    res["notice_period"] = float(notice_period)

                        # res["notice_period"] = int(notice_period)

            
                if experience:
                    print(experience)
                    print(type(experience))
                    if type(experience) == dict:
                        res["experience" ]= experience
                    else:
                        try:
                            if len(str(experience).split())>1:
                                value = int(str(experience).split()[1])
                                if value==0:
                                    res["experience"] = 0
                                else:
                                    comparison = str(experience).split()[0]
                                    res["experience"] = {str(comparison): value}
                            else:
                                res["experience"] = int(experience)
                        except:
                            if len(str(experience).split())>1:
                                value = float(str(experience).split()[1])
                                if value==0:
                                    res["experience"] = 0
                                else:
                                    comparison = str(experience).split()[0]
                                    res["experience"] = {str(comparison): value}
                            else:
                                res["experience"] = float(experience)
                    

                if firstName or lastName or experience or phone_no or locations or skills or current_company or current_designation or notice_period:
                    if organization_id:
                        res["organization"] = ObjectId(organization_id)

                print("res====>",res)
                # {"skills": {"$in": [skill_to_query]}}
                if any(value != "" and value!=[] for value in response.values()):
                    try:
                        mycollection,conn = resumeDetailsCollection()
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
                        # print(json_data)
                        if results_dict['response']['results'][0]['matches']:
                            print("inside if condition")
                            return jsonify(json_data)
                        else:
                            print("inside else condition")
                            response=key_word_search_with_len(query,phone_no,experience,organization_id,notice_period)
                            print(response)
                            return jsonify(response)
                    finally:
                        conn.close()

                elif len(query)<25:
                    response=key_word_search_with_len(query,phone_no,experience,organization_id,notice_period)
                    return jsonify(response)

                elif "month" in query:
                    print("inside 2nd elif condition")
                    return jsonify({'response': {'results': [{'matches': []}]}})
                
                # elif "recruitment" in query or "Recruitment" in query:
                #     response=key_word_search_with_len(query,phone_no,experience,organization_id,notice_period)
                #     return jsonify(response)

                else:
                    response=pinecone_search(query,organization_id,firstName,lastName,phone_no,locations,current_company,skills,current_designation,notice_period)
                    return jsonify(response)

            else:
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
                keyword_query_location_experience = []
                # keyword_query_location_experience1 = []
                res = {}

                if current_location:
                    # location_queries = 
                    res["current_location"] ={"$regex": current_location, "$options": "i"}
                    # keyword_query.append(location_queries)
                    # print(current_location)
                    # print(len(current_location))
                    # curr_location=current_location.split(",")
                    # print(curr_location)
                    # print(len(curr_location))
                    # print(type(curr_location))
                    # if len(curr_location)>1:
                    #     location_queries = [{"current_location": {"$regex": location, "$options": "i"}} for location in curr_location]
                    #     keyword_query_location_experience.extend(location_queries)
                    # else:
                    #     location_queries = {"current_location": {"$regex": current_location, "$options": "i"}}
                    #     keyword_query_location_experience.append(location_queries)
                
                if primary_skill:
                    primary_skill_list=primary_skill.split(",")
                    primary_skill_list = [s.replace('\xa0', ' ') for s in primary_skill_list]
                    print(primary_skill_list)
                    print(type(primary_skill_list))
                    if len(primary_skill_list)>1:
                        print("in if primary_skill ")
                        skill_queries = [{"primary_skill": {"$regex": f'^{skill}$', "$options": "i"}} for skill in primary_skill_list]
                        keyword_query_location_experience.extend(skill_queries)
                    else:
                        print("in else primary_skill ")
                        skill_queries = {"primary_skill": {"$regex": f'^{primary_skill}$', "$options": "i"}}
                        keyword_query_location_experience.append(skill_queries)
                    
                

                    # skill_queries = [{"primary_skill": {"$regex": skill, "$options": "i"}} for skill in primary_skill[0].split(",")]
                    # keyword_query.extend(skill_queries)
                if organization_id:
                    res["organization"] = ObjectId(organization_id)
                # if education:
                #     keyword_query.append({"education": {"$regex": education, "$options": "i"}})
                # if status:
                #     keyword_query.append({"status": {"$regex": status, "$options": "i"}})
                # if industry:
                #     keyword_query.append({"industry": {"$regex": industry, "$options": "i"}})

                if min_experience or max_experience:
                    res["experience"]={"$gte": int(min_experience), "$lte": int(max_experience)}

                # if notice_period:
                #     value = str(notice_period).split()[0]
                #     keyword_query.append({"notice_period": {"$regex": value, "$options": "i"}})

                
                if keyword_query_location_experience:
                    res["$or"] =keyword_query_location_experience
                    print("res :",res)

                # if keyword_query:
                #     res["$and"] = keyword_query
                #     print("res :",res)
                # if keyword_query_location_experience1:
                #     res["$or"] =keyword_query_location_experience1
                #     print("res :",res)
                try:
                    mycollection,conn = resumeDetailsCollection()
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
                    # print(json_data)
                    # if results_dict['response']['results'][0]['matches']:
                    #     print("inside if condition")
                    return jsonify(json_data)
                finally:
                    conn.close()

               
    except Exception as e:
        print("error:",e)
        logging.info("error:",e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
