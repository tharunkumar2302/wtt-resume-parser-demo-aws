from connection import resumeDetailsCollection,userDetailsCollection,ProfilequeuesCollection,s3_client
from utils import (return_non_null_status,return_non_null_status1,return_non_null_status2)
import json
# import datetime
from datetime import datetime, timezone
from bson import ObjectId
from logger import logging
from config import API_KEY,AWS_FILES_FOLDER,AWS_S3_BUCKET_NAME,AWS_ERRORS_FOLDER,PINECONE_API_KEY,PINECONE_ENVIRONMENT,EMBEDDING_MODEL,PINECONE_INDEX_NAME
import sys,os
# import traceback
import pandas as pd
# from openai.embeddings_utils import get_embedding
from openai import OpenAI
client = OpenAI(api_key=API_KEY)
import ast
import math
import numpy as np
import pinecone
import time

embedding_model=EMBEDDING_MODEL

#set pinecone credentials
api_key=PINECONE_API_KEY
environment=PINECONE_ENVIRONMENT

# Connect to the Pinecone index and insert the data
pinecone.init(api_key=api_key, environment=environment)
# pinecone.create_index(index_name, dimension=1536)
index = pinecone.Index(index_name=PINECONE_INDEX_NAME)

# def get_embedding(text, model="text-embedding-3-small"):
#     text = text.replace("\n", " ")
#     return client.embed(model, text).embedding
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def fetching_resume_id_from_MongoDb(pinecone_mongo_uuid_val):
    try:
        collection,conn = resumeDetailsCollection()
        query = {"pinecone_mongo_uuid_val": f"{pinecone_mongo_uuid_val}"}
        resume_id = [doc["_id"] for doc in collection.find(query)][0]
        print("resume_id====>:",resume_id)
        return resume_id
    except:
        pass
    finally:
        conn.close()

def updateinprofileQueues(filename):
    try:
        collection,conn=ProfilequeuesCollection()
        query = {"isProcessed": False,"file_path":f"{AWS_FILES_FOLDER}/{filename}"}
        update = {"$set": {
            "isProcessed": True,
            "processedDateTime": datetime.now(tz=timezone.utc),
            "Remarks": "processed successfully",
            "isDuplicate":True,
            "updatedAt": datetime.now(tz=timezone.utc),
        }}
        result = collection.update_one(query, update)
        logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
    finally:
        conn.close()


def insertingIntoMongoDb_xlsx_csv(firstName,lastName,email,phone_no,loc,present_address,
        DateofBirth,maritial_status,recent_designation,resume_organisation,experience,current_education,
        qualification,institute,marks_in_percentage,specialization,year_of_passing,resume_skill,
        secondary_skills,job_title,description,company_name,location,industry,headline,employment_type,
        date_of_joining,last_date,current_ctc,expected_ctc,current_employment_status,prefered_location,
        ready_to_relocate,overseas_experience,notice_period,having_passport,passport_validity,visa,About,
        status,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,filename,pinecone_mongo_uuid_val,df,filepath,cv_url,
        notice_period_in_month,notice_period_in_year,notice_period_in_days,notice_period_in_week):
    print("pinecone_mongo_uuid_val1:",pinecone_mongo_uuid_val)
    try:
        mycollection,conn = resumeDetailsCollection()
        obj=mycollection.find({"email":return_non_null_status(email) ,"phone_no":return_non_null_status(phone_no)})
        records=[]
        for record in obj:
            records.append(record)
        if records:
            print("entered into update")

            myquery =  record

            newvalues = { "$set": {
                    #   'id': id,
                    'updatedAt':datetime.now(tz=timezone.utc),
                    'firstName':str(return_non_null_status(firstName)).capitalize() if return_non_null_status(firstName) else return_non_null_status(firstName),
                    'lastName':str(return_non_null_status(lastName)).capitalize() if return_non_null_status(lastName) else return_non_null_status(lastName),
                    'email': return_non_null_status(email),
                    'phone_no': return_non_null_status(phone_no),
                    'current_location': return_non_null_status(loc),
                    'present_address': return_non_null_status(present_address),
                    'date_of_birth': return_non_null_status(DateofBirth),
                    'marital_status': return_non_null_status(maritial_status),
                    'current_designation': return_non_null_status(recent_designation),
                    'current_company': return_non_null_status(resume_organisation),
                    'experience': return_non_null_status1(experience) if return_non_null_status1(experience) else 0,
                    'education': return_non_null_status(current_education),
                    'education_details': [{
                                            "qualification":return_non_null_status(qualification),
                                            "institute":return_non_null_status(institute),
                                            "marks_in_percentage":return_non_null_status(marks_in_percentage),
                                            "specialization":return_non_null_status(specialization),
                                            "year_of_passing":return_non_null_status(year_of_passing)
                                            }],#[return_non_null_status(education_detailed_history)],
                    'primary_skill': return_non_null_status(resume_skill),
                    'secondary_skill': return_non_null_status(secondary_skills) if return_non_null_status(secondary_skills) else ' ',
                    'experience_details': [
                                            {
                                                "job_title":return_non_null_status(job_title),
                                                "description":return_non_null_status(description),
                                                "company_name":return_non_null_status(company_name),
                                                "company_location":return_non_null_status(location),
                                                "industry":return_non_null_status(industry),
                                                "headline":return_non_null_status(headline),
                                                "employment_type":return_non_null_status(employment_type),
                                                "date_of_joining":return_non_null_status(date_of_joining),
                                                "last_date":return_non_null_status(last_date)
                                            }
                                        ],#[return_non_null_status(experience_detailed_history)],
                    'status':status,
                    'uploaded_by':'RECRUITER',
                    'source':'ML Parse',
                    'organization':organization_id,
                    'createdByUserId':createdByUserId,
                    'modifiedByUserId':modifiedByUserId,
                    'createdByUserRole':createdByUserRole,
                    'modifiedByUserRole':modifiedByUserRole,
                    'current_ctc':current_ctc,
                    'expected_ctc':expected_ctc,
                    'current_employment_status':return_non_null_status(current_employment_status),
                    'industry':return_non_null_status(industry),
                    'prefered_location':return_non_null_status(prefered_location),
                    'ready_to_relocate':ready_to_relocate,
                    'overseas_experience':overseas_experience,
                    'isActive':'',
                    'notice_period':return_non_null_status(notice_period),
                    'notice_period_in_month':return_non_null_status2(notice_period_in_month),
                    'notice_period_in_year':return_non_null_status2(notice_period_in_year),
                    'notice_period_in_days':return_non_null_status2(notice_period_in_days),
                    'notice_period_in_week':return_non_null_status2(notice_period_in_week),
                    'having_passport':having_passport,
                    'passport_validity':return_non_null_status(passport_validity),
                    'visa':visa,
                    'About':return_non_null_status(About),
                    'is_cv_uploaded':True,
                    'pinecone_mongo_uuid_val':pinecone_mongo_uuid_val,
                    'file_path':filepath,
                    'cv_url':cv_url,
                        }
            }

            mycollection.update_one(myquery, newvalues)
            time.sleep(1)
            # updateinprofileQueues(filename)
            resume_id=fetching_resume_id_from_MongoDb(pinecone_mongo_uuid_val)
            updateIntoPineconewithEmbedding(df,pinecone_mongo_uuid_val,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,cv_url,resume_id,filepath)
        else:
            print("entered into insert")

            rec={
                    # 'id': id,
                    'createdAt':datetime.now(tz=timezone.utc),
                    'updatedAt':datetime.now(tz=timezone.utc),
                    'firstName':str(return_non_null_status(firstName)).capitalize() if return_non_null_status(firstName) else return_non_null_status(firstName),
                    'lastName':str(return_non_null_status(lastName)).capitalize() if return_non_null_status(lastName) else return_non_null_status(lastName),
                    'email': return_non_null_status(email),
                    'phone_no': return_non_null_status(phone_no),
                    'current_location': return_non_null_status(loc),
                    'present_address': return_non_null_status(present_address),
                    'date_of_birth': return_non_null_status(DateofBirth),
                    'marital_status': return_non_null_status(maritial_status),
                    'current_designation': return_non_null_status(recent_designation),
                    'current_company': return_non_null_status(resume_organisation),
                    'experience': return_non_null_status1(experience) if return_non_null_status1(experience) else 0,
                    'education': return_non_null_status(current_education),
                    'education_details': [{
                                            "qualification":return_non_null_status(qualification),
                                            "institute":return_non_null_status(institute),
                                            "marks_in_percentage":return_non_null_status(marks_in_percentage),
                                            "specialization":return_non_null_status(specialization),
                                            "year_of_passing":return_non_null_status(year_of_passing)
                                            }],#[return_non_null_status(education_detailed_history)],
                    'primary_skill': return_non_null_status(resume_skill),
                    'secondary_skill': return_non_null_status(secondary_skills) if return_non_null_status(secondary_skills) else ' ',
                    'experience_details': [
                                            {
                                                "job_title":return_non_null_status(job_title),
                                                "description":return_non_null_status(description),
                                                "company_name":return_non_null_status(company_name),
                                                "company_location":return_non_null_status(location),
                                                "industry":return_non_null_status(industry),
                                                "headline":return_non_null_status(headline),
                                                "employment_type":return_non_null_status(employment_type),
                                                "date_of_joining":return_non_null_status(date_of_joining),
                                                "last_date":return_non_null_status(last_date)
                                            }
                                        ],#[return_non_null_status(experience_detailed_history)],
                    'status':status,
                    'uploaded_by':'RECRUITER',
                    'source':'ML Parse',
                    'organization':organization_id,
                    'createdByUserId':createdByUserId,
                    'modifiedByUserId':modifiedByUserId,
                    'createdByUserRole':createdByUserRole,
                    'modifiedByUserRole':modifiedByUserRole,
                    'current_ctc':current_ctc,
                    'expected_ctc':expected_ctc,
                    'current_employment_status':return_non_null_status(current_employment_status),
                    'industry':return_non_null_status(industry),
                    'prefered_location':return_non_null_status(prefered_location),
                    'ready_to_relocate':ready_to_relocate,
                    'overseas_experience':overseas_experience,
                    'isActive':'',
                    'notice_period':return_non_null_status(notice_period),
                    'notice_period_in_month':return_non_null_status2(notice_period_in_month),
                    'notice_period_in_year':return_non_null_status2(notice_period_in_year),
                    'notice_period_in_days':return_non_null_status2(notice_period_in_days),
                    'notice_period_in_week':return_non_null_status2(notice_period_in_week),
                    'having_passport':having_passport,
                    'passport_validity':return_non_null_status(passport_validity),
                    'visa':visa,
                    'About':return_non_null_status(About),
                    'is_cv_uploaded':True,
                    'pinecone_mongo_uuid_val':pinecone_mongo_uuid_val,
                    'file_path':filepath,
                    'cv_url':cv_url,
                        }
            record = mycollection.insert_one(rec)
            time.sleep(1)
            resume_id=fetching_resume_id_from_MongoDb(pinecone_mongo_uuid_val)
            upsertIntoPineconewithEmbedding(df,pinecone_mongo_uuid_val,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,cv_url,resume_id,filepath)
        return True
    except Exception as msg:
        s3_client.upload_file(
        filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
        )
        logging.info(f"Error: {msg}, Type: {type(msg)}")
        try:
            collection,conn1=ProfilequeuesCollection()
            # Update the records with the specified criteria
            query = {"isProcessed": False,"file_path":f"{AWS_FILES_FOLDER}/{filename}"}
            update = {"$set": {
                "isProcessed": True,
                "processedDateTime": datetime.now(tz=timezone.utc),
                "isError":True,
                "errorMessage":f"Error: {msg}, Type: {type(msg)}",
                "updatedAt": datetime.now(tz=timezone.utc),
            }}
            result = collection.update_one(query, update)
        finally:
            conn1.close()

        logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
        s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

        os.remove(filename)
        pass

        return False
    
    finally:
        conn.close()

def getIdRoleOrganizationIDS(filepath):
    try:
        collection,conn=ProfilequeuesCollection()
        document=collection.find_one({"file_path":f"{filepath}"})
        if document is not None:
        # Get the value of the field you're interested in
            organization_id = ObjectId(document.get('organization'))
            createdByUserId = ObjectId(document.get('uploadedBy'))
            modifiedByUserId = createdByUserId
            try:
                usercollection,conn1=userDetailsCollection()
                document_user=usercollection.find_one({"_id":ObjectId(createdByUserId)})
                if document_user is not None:
                    createdByUserRole =ObjectId(document_user.get('role'))
                    modifiedByUserRole = createdByUserRole
            finally:
                conn1.close()

            return organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole
    
    except Exception as msg:
        logging.info(f"{msg}")
        pass
    finally:
        conn.close()

def upsertIntoPineconewithEmbedding(df,pinecone_mongo_uuid_val,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,cv_url,resume_id,filepath):
    print("df==>",df)
    df.replace("N/A", "", inplace=True)
    df.replace("NaN", "", inplace=True)
    df.replace("Not Specified", "", inplace=True)

    # Add a new column named "Text" and populate it with the desired text
    # df['Text'] = str(response)
    df['Text'] = df.apply(lambda row: ' '.join(row.astype(str)), axis=1)
    df = df.fillna('')
    print("df in middle:",df)

    df["embedded_column"] = df.Text.apply(lambda x: get_embedding(str(x), model=embedding_model) if str(x).strip() else None)
    # remove rows with None in embedded_column
    # df = df.dropna(subset=["embedded_column"])

    df['firstName']=df['firstName'].fillna('')
    df['lastName']=df['lastName'].fillna('')
    df['email']=df['email'].fillna('')
    df['phone_no']=df['phone_no'].fillna('')
    df['current_location']=df['current_location'].fillna('')
    df['present_address']=df['present_address'].fillna('')
    df['DateofBirth']=df['DateofBirth'].fillna('')
    df['maritial_status']=df['maritial_status'].fillna('')
    df['recent_designation']=df['recent_designation'].fillna('')
    df['resume_organisation']=df['resume_organisation'].fillna('')
    df['experience']=df['experience'].fillna(0)
    df['current_education']=df['current_education'].fillna('')
    df['qualification']=df['qualification'].fillna('')
    df['institute']=df['institute'].fillna('')
    try:
        df["marks_in_percentage"]=df["marks_in_percentage"].fillna('')
    except:
        df["marks_in_percentage"]=df["marks_in_percentage"].fillna('')

    df['specialization']=df['specialization'].fillna('')
    try:
        df['year_of_passing']=df['year_of_passing'].fillna('')
    except:
        df["year_of_passing"]=df["year_of_passing"].fillna('')
    df['resume_skill']=df['resume_skill'].fillna('')
    df['secondary_skills']=df['secondary_skills'].fillna('')
    df['job_title']=df['job_title'].fillna('')
    try:
        df['description']=df['description'].fillna('')
    except:
        df['description']=df['description'].fillna('')
    df['location']=df['location'].fillna('')
    df['industry']=df['industry'].fillna('')
    df['headline']=df['headline'].fillna('')

    try:
        df['employment_type']=df['employment_type'].fillna('')
    except:
        df['employment_type']=df['employment_type'].fillna('')

    try:
        df['date_of_joining']=df['date_of_joining'].fillna('')
    except:
        df['date_of_joining']=df['date_of_joining'].fillna('')

    try:
        df['last_date']=df['last_date'].fillna('')
    except:
        df['last_date']=df['last_date'].fillna('')

    df['current_ctc']=df['current_ctc'].fillna(0)
    df['expected_ctc']=df['expected_ctc'].fillna(0)
    df['current_employment_status']=df['current_employment_status'].fillna('')
    try:
        df['prefered_location']=df['prefered_location'].fillna('')
    except:
        df['prefered_location']=df['prefered_location'].fillna('')
    try:
        df['ready_to_relocate']=df['ready_to_relocate'].fillna('')
    except:
        df['ready_to_relocate']=df['ready_to_relocate'].fillna('')
    try:
        df['overseas_experience']=df['overseas_experience'].fillna('')
    except:
        df['overseas_experience']=df['overseas_experience'].fillna('')
    df['notice_period']=df['notice_period'].fillna(0)
    df['having_passport']=df['having_passport'].fillna('')
    df['passport_validity']=df['passport_validity'].fillna('')
    df['visa']=df['visa'].fillna('')
    df['About']=df['About'].fillna('')
    # df['Text']=df['Text'].fillna('')
    # df['embedded_column']=df['embedded_column'].fillna('')

    start_index = 0#6091  # Specify the index to start from

    batch_size = 10
    total_rows = len(df)
    num_batches = math.ceil((total_rows - start_index) / batch_size)
    # pinecone_mongo_uuid_val=str(uuid4())
    # df.to_csv("csvfile.csv")
    for i in range(num_batches):
        current_index = start_index + i * batch_size
        next_index = min(start_index + (i + 1) * batch_size, total_rows)

        data_to_insert = []

        for _, row in df.iloc[current_index:next_index].iterrows():
            print("entered into for")
            # vector_str = row['embedded_column']  # Assuming 'embedded_column' contains the string representation of a list
            # vector = ast.literal_eval(row['embedded_column'])  # Convert the string to a list
            # vector = np.array(vector, dtype=np.float32).tolist()  # Convert the list to a list of float values
            # vector = np.array(eval(row['embedded_column']), dtype=np.float32).tolist()
            # vector = np.array(ast.literal_eval(row['embedded_column']), dtype=np.float32).tolist()
            # vector = np.array(ast.literal_eval(str(row['embedded_column']).replace(" ", ",")), dtype=np.float32).tolist()
            # vector = np.array(json.loads(row['embedded_column']), dtype=np.float32).tolist()
            vector = np.array(json.loads(json.dumps(row['embedded_column'])), dtype=np.float32).tolist()
            if row['email'] and row['phone_no']:
                status='Published'
            else:
                status='Draft'
            print("entered after else")
            experience=''
            try:
                if row['experience'] and row['experience']!='':
                    exp=''
                    for value in row['experience']:
                        if value.isdigit() or value==".":
                            exp+=value
                    experience=float(exp)
            except:
                experience=''
                pass

            try:
                year_of_passing=row['year_of_passing']
            except:
                year_of_passing=row['year_of_passing']

            try:
                marks_in_percentage=row["marks_in_percentage"]
            except:
                marks_in_percentage=row["marks_in_percentage"]

            try:
                description=row['description']
            except:
                description=row['description']

            try:
                employment_type=row['employment_type']
            except:
                employment_type=row['employment_type']
            try:
                date_of_joining=row['date_of_joining']
            except:
                date_of_joining=row['date_of_joining']
            try:
                last_date=row['last_date']
            except:
                last_date=row['last_date']
            try:
                prefered_location=row['prefered_location']
            except:
                prefered_location=row['prefered_location']
            try:
                ready_to_relocate=row['ready_to_relocate']
            except:
                ready_to_relocate=row['ready_to_relocate']
            try:
                overseas_experience=row['overseas_experience']
            except:
                overseas_experience=row['overseas_experience']

            data ={
                    'updatedAt':datetime.now(tz=timezone.utc),
                    'firstName': str(row['firstName']).capitalize(),
                    'lastName':str(row['lastName']).capitalize(),
                    'email': row['email'],
                    'phone_no': row['phone_no'],
                    'current_location': str(row['current_location']).capitalize(),
                    'present_address': row['present_address'],
                    'date_of_birth': row['DateofBirth'],
                    'marital_status': row['maritial_status'],
                    'current_designation': row['recent_designation'],
                    'current_company': str(row['resume_organisation']).capitalize(),
                    'experience': experience,
                    'education':row['current_education'],
    #                 'education_details': {
                    "qualification":row['qualification'],
                    "institute":row['institute'],
                    "marks_in_percentage":marks_in_percentage,
                    "specialization":row['specialization'],
                    "year_of_passing":year_of_passing,
    #                                         },#[row[education_detailed_history)],
                    'primary_skill': row['resume_skill'],
                    'secondary_skill': row['secondary_skills'],
    #                 'experience_details': 
    #                                         {
                    "job_title":row['job_title'],
                    "description":description,
                    "company_name": row['resume_organisation'],
                    "company_location":row['location'],
    #                 "industry":row['Industry'],
                    "headline":row['headline'],
                    "employment_type":employment_type,
                    "date_of_joining":date_of_joining,
                    "last_date":last_date,
    #                                         },
    #                                     [row[experience_detailed_history)],
                    'status':status,
                    'uploaded_by':'RECRUITER',
                    'source':'ML Parse',
                    'organization':str(organization_id),
                    'createdByUserId':str(createdByUserId),
                    'modifiedByUserId':str(modifiedByUserId),
                    'createdByUserRole':str(createdByUserRole),
                    'modifiedByUserRole':str(modifiedByUserRole),
                    'current_ctc':row['current_ctc'],
                    'expected_ctc':row['expected_ctc'],
                    'current_employment_status':row['current_employment_status'],
                    'industry':row['industry'],
                    'prefered_location':prefered_location,
                    'ready_to_relocate':ready_to_relocate,
                    'overseas_experience':overseas_experience,
                    'isActive':'',
                    'notice_period':row['notice_period'],
                    'having_passport':row['having_passport'],
                    'passport_validity':row['passport_validity'],
                    'visa':row['visa'],
                    'About':row['About'],
                    'is_cv_uploaded':True,
                    'createdAt':datetime.now(tz=timezone.utc),
                    'pinecone_mongo_uuid_val':pinecone_mongo_uuid_val,
                    'cv_url':cv_url,
                    'resume_id':str(resume_id),
                    'file_path':filepath,
                    'Text':row['Text'],
            }
            print("pinecone_mongo_uuid_val",pinecone_mongo_uuid_val)
            data_to_insert.append(((pinecone_mongo_uuid_val), vector, data))
       
        index.upsert(data_to_insert)


def updateIntoPineconewithEmbedding(df,pinecone_mongo_uuid_val,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,cv_url,resume_id,filepath):
    print("df==>",df)
    df.replace("N/A", "", inplace=True)
    df.replace("NaN", "", inplace=True)
    df.replace("Not Specified", "", inplace=True)

    # Add a new column named "Text" and populate it with the desired text
    # df['Text'] = str(response)
    df['Text'] = df.apply(lambda row: ' '.join(row.astype(str)), axis=1)
    df = df.fillna('')
    print("df in middle:",df)

    df["embedded_column"] = df.Text.apply(lambda x: get_embedding(str(x), model=embedding_model) if str(x).strip() else None)
    # remove rows with None in embedded_column
    # df = df.dropna(subset=["embedded_column"])

    df['firstName']=df['firstName'].fillna('')
    df['lastName']=df['lastName'].fillna('')
    df['email']=df['email'].fillna('')
    df['phone_no']=df['phone_no'].fillna('')
    df['current_location']=df['current_location'].fillna('')
    df['present_address']=df['present_address'].fillna('')
    df['DateofBirth']=df['DateofBirth'].fillna('')
    df['maritial_status']=df['maritial_status'].fillna('')
    df['recent_designation']=df['recent_designation'].fillna('')
    df['resume_organisation']=df['resume_organisation'].fillna('')
    df['experience']=df['experience'].fillna(0)
    df['current_education']=df['current_education'].fillna('')
    df['qualification']=df['qualification'].fillna('')
    df['institute']=df['institute'].fillna('')
    try:
        df["marks_in_percentage"]=df["marks_in_percentage"].fillna('')
    except:
        df["marks_in_percentage"]=df["marks_in_percentage"].fillna('')

    df['specialization']=df['specialization'].fillna('')
    try:
        df['year_of_passing']=df['year_of_passing'].fillna('')
    except:
        df["year_of_passing"]=df["year_of_passing"].fillna('')
    df['resume_skill']=df['resume_skill'].fillna('')
    df['secondary_skills']=df['secondary_skills'].fillna('')
    df['job_title']=df['job_title'].fillna('')
    try:
        df['description']=df['description'].fillna('')
    except:
        df['description']=df['description'].fillna('')
    df['location']=df['location'].fillna('')
    df['industry']=df['industry'].fillna('')
    df['headline']=df['headline'].fillna('')

    try:
        df['employment_type']=df['employment_type'].fillna('')
    except:
        df['employment_type']=df['employment_type'].fillna('')

    try:
        df['date_of_joining']=df['date_of_joining'].fillna('')
    except:
        df['date_of_joining']=df['date_of_joining'].fillna('')

    try:
        df['last_date']=df['last_date'].fillna('')
    except:
        df['last_date']=df['last_date'].fillna('')

    df['current_ctc']=df['current_ctc'].fillna(0)
    df['expected_ctc']=df['expected_ctc'].fillna(0)
    df['current_employment_status']=df['current_employment_status'].fillna('')
    try:
        df['prefered_location']=df['prefered_location'].fillna('')
    except:
        df['prefered_location']=df['prefered_location'].fillna('')
    try:
        df['ready_to_relocate']=df['ready_to_relocate'].fillna('')
    except:
        df['ready_to_relocate']=df['ready_to_relocate'].fillna('')
    try:
        df['overseas_experience']=df['overseas_experience'].fillna('')
    except:
        df['overseas_experience']=df['overseas_experience'].fillna('')
    df['notice_period']=df['notice_period'].fillna(0)
    df['having_passport']=df['having_passport'].fillna('')
    df['passport_validity']=df['passport_validity'].fillna('')
    df['visa']=df['visa'].fillna('')
    df['About']=df['About'].fillna('')
    # df['Text']=df['Text'].fillna('')
    # df['embedded_column']=df['embedded_column'].fillna('')

    start_index = 0#6091  # Specify the index to start from

    batch_size = 10
    total_rows = len(df)
    num_batches = math.ceil((total_rows - start_index) / batch_size)
    # pinecone_mongo_uuid_val=str(uuid4())
    # df.to_csv("csvfile.csv")
    for i in range(num_batches):
        current_index = start_index + i * batch_size
        next_index = min(start_index + (i + 1) * batch_size, total_rows)

        data_to_insert = []

        for _, row in df.iloc[current_index:next_index].iterrows():
            print("entered into for")
            # vector_str = row['embedded_column']  # Assuming 'embedded_column' contains the string representation of a list
            # vector = ast.literal_eval(row['embedded_column'])  # Convert the string to a list
            # vector = np.array(vector, dtype=np.float32).tolist()  # Convert the list to a list of float values
            # vector = np.array(eval(row['embedded_column']), dtype=np.float32).tolist()
            # vector = np.array(ast.literal_eval(row['embedded_column']), dtype=np.float32).tolist()
            # vector = np.array(ast.literal_eval(str(row['embedded_column']).replace(" ", ",")), dtype=np.float32).tolist()
            # vector = np.array(json.loads(row['embedded_column']), dtype=np.float32).tolist()
            vector = np.array(json.loads(json.dumps(row['embedded_column'])), dtype=np.float32).tolist()
            if row['email'] and row['phone_no']:
                status='Published'
            else:
                status='Draft'
            print("entered after else")
            experience=''
            try:
                if row['experience'] and row['experience']!='':
                    exp=''
                    for value in row['experience']:
                        if value.isdigit() or value==".":
                            exp+=value
                    experience=float(exp)
                else:
                    experience=''
            except:
                experience=''
                pass

            try:
                year_of_passing=row['year_of_passing']
            except:
                year_of_passing=row['year_of_passing']

            try:
                marks_in_percentage=row["marks_in_percentage"]
            except:
                marks_in_percentage=row["marks_in_percentage"]

            try:
                description=row['description']
            except:
                description=row['description']

            try:
                employment_type=row['employment_type']
            except:
                employment_type=row['employment_type']
            try:
                date_of_joining=row['date_of_joining']
            except:
                date_of_joining=row['date_of_joining']
            try:
                last_date=row['last_date']
            except:
                last_date=row['last_date']
            try:
                prefered_location=row['prefered_location']
            except:
                prefered_location=row['prefered_location']
            try:
                ready_to_relocate=row['ready_to_relocate']
            except:
                ready_to_relocate=row['ready_to_relocate']
            try:
                overseas_experience=row['overseas_experience']
            except:
                overseas_experience=row['overseas_experience']

            data ={
                    'updatedAt':datetime.now(tz=timezone.utc),
                    'firstName': str(row['firstName']).capitalize(),
                    'lastName':str(row['lastName']).capitalize(),
                    'email': row['email'],
                    'phone_no': row['phone_no'],
                    'current_location': str(row['current_location']).capitalize(),
                    'present_address': row['present_address'],
                    'date_of_birth': row['DateofBirth'],
                    'marital_status': row['maritial_status'],
                    'current_designation': row['recent_designation'],
                    'current_company': str(row['resume_organisation']).capitalize(),
                    'experience': experience,
                    'education':row['current_education'],
    #                 'education_details': {
                    "qualification":row['qualification'],
                    "institute":row['institute'],
                    "marks_in_percentage":marks_in_percentage,
                    "specialization":row['specialization'],
                    "year_of_passing":year_of_passing,
    #                                         },#[row[education_detailed_history)],
                    'primary_skill': row['resume_skill'],
                    'secondary_skill': row['secondary_skills'],
    #                 'experience_details': 
    #                                         {
                    "job_title":row['job_title'],
                    "description":description,
                    "company_name": row['resume_organisation'],
                    "company_location":row['location'],
    #                 "industry":row['Industry'],
                    "headline":row['headline'],
                    "employment_type":employment_type,
                    "date_of_joining":date_of_joining,
                    "last_date":last_date,
    #                                         },
    #                                     [row[experience_detailed_history)],
                    'status':status,
                    'uploaded_by':'RECRUITER',
                    'source':'ML Parse',
                    'organization':str(organization_id),
                    'createdByUserId':str(createdByUserId),
                    'modifiedByUserId':str(modifiedByUserId),
                    'createdByUserRole':str(createdByUserRole),
                    'modifiedByUserRole':str(modifiedByUserRole),
                    'current_ctc':row['current_ctc'],
                    'expected_ctc':row['expected_ctc'],
                    'current_employment_status':row['current_employment_status'],
                    'industry':row['industry'],
                    'prefered_location':prefered_location,
                    'ready_to_relocate':ready_to_relocate,
                    'overseas_experience':overseas_experience,
                    'isActive':'',
                    'notice_period':row['notice_period'],
                    'having_passport':row['having_passport'],
                    'passport_validity':row['passport_validity'],
                    'visa':row['visa'],
                    'About':row['About'],
                    'is_cv_uploaded':True,
                    'createdAt':datetime.now(tz=timezone.utc),
                    'pinecone_mongo_uuid_val':pinecone_mongo_uuid_val,
                    'cv_url':cv_url,
                    'resume_id':str(resume_id),
                    'file_path':filepath,
                    'Text':row['Text'],
            }
            print("pinecone_mongo_uuid_val",pinecone_mongo_uuid_val)
            data_to_insert.append(((pinecone_mongo_uuid_val), vector, data))
       
        # index.upsert(data_to_insert)
        phrase_embedding = get_embedding(str(row['email']), model=embedding_model)
        query_result = index.query(queries=[phrase_embedding], top_k=1)
        update_response = index.update(
            id=query_result['results'][0]['matches'][0]['id'],
            values=row["embedded_column"],
            set_metadata=data,
            # namespace='example-namespace'
        )
        print("updated")

