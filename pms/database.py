from connection import resumeDetailsCollection,userDetailsCollection,ProfilequeuesCollection,s3_client
from utils import (return_non_null_status,return_non_null_status1,return_non_null_status2,insertingIntopreparingData)
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

embedding_model=EMBEDDING_MODEL

#set pinecone credentials
api_key=PINECONE_API_KEY
environment=PINECONE_ENVIRONMENT

# Connect to the Pinecone index and insert the data
pinecone.init(api_key=api_key, environment=environment)
# pinecone.create_index(index_name, dimension=1536)
index = pinecone.Index(index_name=PINECONE_INDEX_NAME)

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
    finally:
        conn.close()
    logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')

def updateUserTable(resume_id,firstName,lastName,emailAddress,mobileNumber,designation):
    try:
        collection,conn=userDetailsCollection()
        obj=collection.find({"emailAddress":str(emailAddress)})
        records=[]
        for record in obj:
            records.append(record)
        if records:
            query =  record
            newvalues_users = { "$set": {
            'firstName':firstName,
            'lastName':lastName,
            'emailAddress':emailAddress,
            'mobileNumber':mobileNumber,
            'designation':designation
            }}
            result = collection.update_one(query, newvalues_users)
    except:
        pass
    finally:
        conn.close()



def insertingIntoMongoDb(firstName,lastName,email,phone_no,loc,present_address,
        DateofBirth,maritial_status,recent_designation,resume_organisation,experience,current_education,
        qualification,institute,marks_in_percentage,specialization,year_of_passing,resume_skill,
        secondary_skills,job_title,description,company_name,location,industry,headline,employment_type,
        date_of_joining,last_date,current_ctc,expected_ctc,current_employment_status,prefered_location,
        ready_to_relocate,overseas_experience,notice_period,having_passport,passport_validity,visa,About,
        status,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,filename,pinecone_mongo_uuid_val,df,filepath,cv_url,
        notice_period_in_month,notice_period_in_year,notice_period_in_days,notice_period_in_week,text,response):
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
            updateinprofileQueues(filename)
            resume_id=fetching_resume_id_from_MongoDb(pinecone_mongo_uuid_val)
            updateUserTable(resume_id,return_non_null_status(firstName),return_non_null_status(lastName),return_non_null_status(email),
            return_non_null_status(phone_no),return_non_null_status(recent_designation))
            updateIntoPineconewithEmbedding(df,pinecone_mongo_uuid_val,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,cv_url,resume_id,filepath)
            # try:
            #     updatingIntopreparingData(text,myquery,newvalues,response)
            # except:
            #     pass
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
            resume_id=fetching_resume_id_from_MongoDb(pinecone_mongo_uuid_val)
            upsertIntoPineconewithEmbedding(df,pinecone_mongo_uuid_val,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,cv_url,resume_id,filepath)
            try:
                insertingIntopreparingData(text,rec,response)
            except:
                pass
        return True
    except Exception as msg:
        s3_client.upload_file(
        filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
        )
        logging.info(f"Error: {msg}, Type: {type(msg)}")
        try:
            collection, conn=ProfilequeuesCollection()
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
            conn.close()

        logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
        s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

        os.remove(filename)
        pass

        return False
    finally:
        conn.close()

# def getIdRoleOrganizationIDS(filepath):
#     try:
#         print("=============================before============================")
#         # collection,conn=ProfilequeuesCollection()
#         profile_collection_tuple = ProfilequeuesCollection()
#         print(profile_collection_tuple)  # Debugging: Check the return value
#         collection, conn = profile_collection_tuple
#         print("collection===================",collection)
#         document=collection.find_one({"file_path":f"{filepath}"})
#         if document is not None:
#         # Get the value of the field you're interested in
#             organization_id = ObjectId(document.get('organization'))
#             createdByUserId = ObjectId(document.get('uploadedBy'))
#             modifiedByUserId = createdByUserId
#             try:
#                 # usercollection,conn=userDetailsCollection()
#                 user_collection_tuple = userDetailsCollection()
#                 print(user_collection_tuple)  # Debugging: Check the return value
#                 usercollection, conn1 = user_collection_tuple
#                 document_user=usercollection.find_one({"_id":ObjectId(createdByUserId)})
#                 if document_user is not None:
#                     createdByUserRole =ObjectId(document_user.get('role'))
#                     modifiedByUserRole = createdByUserRole
#             finally:
#                 conn1.close()

#             return organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole
    
#     except Exception as msg:
#         logging.info(f"{msg}")
#         pass
#     finally:
#         conn.close()
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

# def get_embedding(text, model="text-embedding-3-small"):
#     text = text.replace("\n", " ")
#     return client.embed(model, text).embedding
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

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

    # df["embedded_column"] = df.Text.apply(lambda x: get_embedding(str(x), engine=embedding_model) if str(x).strip() else None)
    df["embedded_column"] = df.Text.apply(lambda x: get_embedding(str(x), model=embedding_model) if str(x).strip() else None)

    # remove rows with None in embedded_column
    # get_embedding(str(query), model=embedding_model)
    # df = df.dropna(subset=["embedded_column"])

    df['First Name']=df['First Name'].fillna('')
    df['Last Name']=df['Last Name'].fillna('')
    df['Email ID']=df['Email ID'].fillna('')
    df['Mobile number']=df['Mobile number'].fillna('')
    df['Location']=df['Location'].fillna('')
    df['Present Address']=df['Present Address'].fillna('')
    df['Date of Birth']=df['Date of Birth'].fillna('')
    df['Marital Status']=df['Marital Status'].fillna('')
    df['Designation']=df['Designation'].fillna('')
    df['Company']=df['Company'].fillna('')
    df['Experience']=df['Experience'].fillna(0)
    df['Education']=df['Education'].fillna('')
    df['Qualification']=df['Qualification'].fillna('')
    df['Education Institute']=df['Education Institute'].fillna('')
    try:
        df["Marks in percentage"]=df["Marks in percentage"].fillna('')
    except:
        df["Marks in Percentage"]=df["Marks in Percentage"].fillna('')

    df['Specialization']=df['Specialization'].fillna('')
    try:
        df['Year of passing']=df['Year of passing'].fillna('')
    except:
        df["Year of Passing"]=df["Year of Passing"].fillna('')
    df['Primary Skills']=df['Primary Skills'].fillna('')
    df['Secondary Skills']=df['Secondary Skills'].fillna('')
    df['Job Title']=df['Job Title'].fillna('')
    try:
        df['Job description']=df['Job description'].fillna('')
    except:
        df['Job Description']=df['Job Description'].fillna('')
    df['Company Location']=df['Company Location'].fillna('')
    df['Industry']=df['Industry'].fillna('')
    df['Headline']=df['Headline'].fillna('')

    try:
        df['Employment type']=df['Employment type'].fillna('')
    except:
        df['Employment Type']=df['Employment Type'].fillna('')

    try:
        df['Date of joining']=df['Date of joining'].fillna('')
    except:
        df['Date of Joining']=df['Date of Joining'].fillna('')

    try:
        df['Last date']=df['Last date'].fillna('')
    except:
        df['Last Date']=df['Last Date'].fillna('')

    df['Current CTC']=df['Current CTC'].fillna(0)
    df['Expected CTC']=df['Expected CTC'].fillna(0)
    df['Current Employment Status']=df['Current Employment Status'].fillna('')
    try:
        df['Prefered Location']=df['Prefered Location'].fillna('')
    except:
        df['Prefered location']=df['Prefered location'].fillna('')
    try:
        df['Ready to relocate']=df['Ready to relocate'].fillna('')
    except:
        df['Ready to Relocate']=df['Ready to Relocate'].fillna('')
    try:
        df['Overseas Experience']=df['Overseas Experience'].fillna('')
    except:
        df['Overseas experience']=df['Overseas experience'].fillna('')
    df['Notice Period']=df['Notice Period'].fillna(0)
    df['Having Passport']=df['Having Passport'].fillna('')
    df['Passport Validity']=df['Passport Validity'].fillna('')
    df['Visa']=df['Visa'].fillna('')
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
            if row['Email ID'] and row['Mobile number']:
                status='Published'
            else:
                status='Draft'
            print("entered after else")
            try:
                if row['Experience'] and row['Experience']!='':
                    exp=''
                    for value in row['Experience']:
                        if value.isdigit() or value==".":
                            exp+=value
                    experience=float(exp)
            except:
                experience=''
                pass

            try:
                year_of_passing=row['Year of Passing']
            except:
                year_of_passing=row['Year of passing']

            try:
                marks_in_percentage=row["Marks in percentage"]
            except:
                marks_in_percentage=row["Marks in Percentage"]

            try:
                description=row['Job description']
            except:
                description=row['Job Description']

            try:
                employment_type=row['Employment type']
            except:
                employment_type=row['Employment Type']
            try:
                date_of_joining=row['Date of joining']
            except:
                date_of_joining=row['Date of Joining']
            try:
                last_date=row['Last date']
            except:
                last_date=row['Last Date']
            try:
                prefered_location=row['Prefered Location']
            except:
                prefered_location=row['Prefered location']
            try:
                ready_to_relocate=row['Ready to relocate']
            except:
                ready_to_relocate=row['Ready to Relocate']
            try:
                overseas_experience=row['Overseas Experience']
            except:
                overseas_experience=row['Overseas experience']

            data ={
                    'updatedAt':datetime.now(tz=timezone.utc),
                    'firstName': str(row['First Name']).capitalize(),
                    'lastName':str(row['Last Name']).capitalize(),
                    'email': row['Email ID'],
                    'phone_no': row['Mobile number'],
                    'current_location': str(row['Location']).capitalize(),
                    'present_address': row['Present Address'],
                    'date_of_birth': row['Date of Birth'],
                    'marital_status': row['Marital Status'],
                    'current_designation': row['Designation'],
                    'current_company': str(row['Company']).capitalize(),
                    'experience': experience,
                    'education':row['Education'],
    #                 'education_details': {
                    "qualification":row['Qualification'],
                    "institute":row['Education Institute'],
                    "marks_in_percentage":marks_in_percentage,
                    "specialization":row['Specialization'],
                    "year_of_passing":year_of_passing,
    #                                         },#[row[education_detailed_history)],
                    'primary_skill': row['Primary Skills'],
                    'secondary_skill': row['Secondary Skills'],
    #                 'experience_details': 
    #                                         {
                    "job_title":row['Job Title'],
                    "description":description,
                    "company_name": row['Company'],
                    "company_location":row['Company Location'],
    #                 "industry":row['Industry'],
                    "headline":row['Headline'],
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
                    'current_ctc':row['Current CTC'],
                    'expected_ctc':row['Expected CTC'],
                    'current_employment_status':row['Current Employment Status'],
                    'industry':row['Industry'],
                    'prefered_location':prefered_location,
                    'ready_to_relocate':ready_to_relocate,
                    'overseas_experience':overseas_experience,
                    'isActive':'',
                    'notice_period':row['Notice Period'],
                    'having_passport':row['Having Passport'],
                    'passport_validity':row['Passport Validity'],
                    'visa':row['Visa'],
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

    df['First Name']=df['First Name'].fillna('')
    df['Last Name']=df['Last Name'].fillna('')
    df['Email ID']=df['Email ID'].fillna('')
    df['Mobile number']=df['Mobile number'].fillna('')
    df['Location']=df['Location'].fillna('')
    df['Present Address']=df['Present Address'].fillna('')
    df['Date of Birth']=df['Date of Birth'].fillna('')
    df['Marital Status']=df['Marital Status'].fillna('')
    df['Designation']=df['Designation'].fillna('')
    df['Company']=df['Company'].fillna('')
    df['Experience']=df['Experience'].fillna(0)
    df['Education']=df['Education'].fillna('')
    df['Qualification']=df['Qualification'].fillna('')
    df['Education Institute']=df['Education Institute'].fillna('')
    try:
        df["Marks in percentage"]=df["Marks in percentage"].fillna('')
    except:
        df["Marks in Percentage"]=df["Marks in Percentage"].fillna('')

    df['Specialization']=df['Specialization'].fillna('')
    try:
        df['Year of passing']=df['Year of passing'].fillna('')
    except:
        df["Year of Passing"]=df["Year of Passing"].fillna('')
    df['Primary Skills']=df['Primary Skills'].fillna('')
    df['Secondary Skills']=df['Secondary Skills'].fillna('')
    df['Job Title']=df['Job Title'].fillna('')
    try:
        df['Job description']=df['Job description'].fillna('')
    except:
        df['Job Description']=df['Job Description'].fillna('')
    df['Company Location']=df['Company Location'].fillna('')
    df['Industry']=df['Industry'].fillna('')
    df['Headline']=df['Headline'].fillna('')

    try:
        df['Employment type']=df['Employment type'].fillna('')
    except:
        df['Employment Type']=df['Employment Type'].fillna('')

    try:
        df['Date of joining']=df['Date of joining'].fillna('')
    except:
        df['Date of Joining']=df['Date of Joining'].fillna('')

    try:
        df['Last date']=df['Last date'].fillna('')
    except:
        df['Last Date']=df['Last Date'].fillna('')

    df['Current CTC']=df['Current CTC'].fillna(0)
    df['Expected CTC']=df['Expected CTC'].fillna(0)
    df['Current Employment Status']=df['Current Employment Status'].fillna('')
    try:
        df['Prefered Location']=df['Prefered Location'].fillna('')
    except:
        df['Prefered location']=df['Prefered location'].fillna('')
    try:
        df['Ready to relocate']=df['Ready to relocate'].fillna('')
    except:
        df['Ready to Relocate']=df['Ready to Relocate'].fillna('')
    try:
        df['Overseas Experience']=df['Overseas Experience'].fillna('')
    except:
        df['Overseas experience']=df['Overseas experience'].fillna('')
    df['Notice Period']=df['Notice Period'].fillna(0)
    df['Having Passport']=df['Having Passport'].fillna('')
    df['Passport Validity']=df['Passport Validity'].fillna('')
    df['Visa']=df['Visa'].fillna('')
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
            if row['Email ID'] and row['Mobile number']:
                status='Published'
            else:
                status='Draft'
            print("entered after else")
            try:
                if row['Experience'] and row['Experience']!='':
                    exp=''
                    for value in row['Experience']:
                        if value.isdigit() or value==".":
                            exp+=value
                    experience=float(exp)
                else:
                    experience=''
            except:
                experience=''
                pass

            try:
                year_of_passing=row['Year of Passing']
            except:
                year_of_passing=row['Year of passing']

            try:
                marks_in_percentage=row["Marks in percentage"]
            except:
                marks_in_percentage=row["Marks in Percentage"]

            try:
                description=row['Job description']
            except:
                description=row['Job Description']

            try:
                employment_type=row['Employment type']
            except:
                employment_type=row['Employment Type']
            try:
                date_of_joining=row['Date of joining']
            except:
                date_of_joining=row['Date of Joining']
            try:
                last_date=row['Last date']
            except:
                last_date=row['Last Date']
            try:
                prefered_location=row['Prefered Location']
            except:
                prefered_location=row['Prefered location']
            try:
                ready_to_relocate=row['Ready to relocate']
            except:
                ready_to_relocate=row['Ready to Relocate']
            try:
                overseas_experience=row['Overseas Experience']
            except:
                overseas_experience=row['Overseas experience']

            data ={
                    'updatedAt':datetime.now(tz=timezone.utc),
                    'firstName': str(row['First Name']).capitalize(),
                    'lastName':str(row['Last Name']).capitalize(),
                    'email': row['Email ID'],
                    'phone_no': row['Mobile number'],
                    'current_location': str(row['Location']).capitalize(),
                    'present_address': row['Present Address'],
                    'date_of_birth': row['Date of Birth'],
                    'marital_status': row['Marital Status'],
                    'current_designation': row['Designation'],
                    'current_company': str(row['Company']).capitalize(),
                    'experience': experience,
                    'education':row['Education'],
    #                 'education_details': {
                    "qualification":row['Qualification'],
                    "institute":row['Education Institute'],
                    "marks_in_percentage":marks_in_percentage,
                    "specialization":row['Specialization'],
                    "year_of_passing":year_of_passing,
    #                                         },#[row[education_detailed_history)],
                    'primary_skill': row['Primary Skills'],
                    'secondary_skill': row['Secondary Skills'],
    #                 'experience_details': 
    #                                         {
                    "job_title":row['Job Title'],
                    "description":description,
                    "company_name": row['Company'],
                    "company_location":row['Company Location'],
    #                 "industry":row['Industry'],
                    "headline":row['Headline'],
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
                    'current_ctc':row['Current CTC'],
                    'expected_ctc':row['Expected CTC'],
                    'current_employment_status':row['Current Employment Status'],
                    'industry':row['Industry'],
                    'prefered_location':prefered_location,
                    'ready_to_relocate':ready_to_relocate,
                    'overseas_experience':overseas_experience,
                    'isActive':'',
                    'notice_period':row['Notice Period'],
                    'having_passport':row['Having Passport'],
                    'passport_validity':row['Passport Validity'],
                    'visa':row['Visa'],
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
        phrase_embedding = get_embedding(str(row['Email ID']), model=embedding_model)
        query_result = index.query(queries=[phrase_embedding], top_k=1)
        update_response = index.update(
            id=query_result['results'][0]['matches'][0]['id'],
            values=row["embedded_column"],
            set_metadata=data,
            # namespace='example-namespace'
        )
        print("updated")

