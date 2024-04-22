from config import (AWS_SERVICE,AWS_REGION_NAME,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,
                   AWS_S3_BUCKET_NAME,MONGODB_HOST,MONGODB_PORT,MONGODB_DATABASE_NAME,
                   MONGODB_RESUME_DETAILS_COLLECTION_NAME,MONGODB_USER_DETAILS_COLLECTION_NAME,
                   MONGODB_FILTER_WITH_SKILL_COLLECTION_NAME,MONGODB_FEEDBACK_DETAIL_COLLECTION_NAME,
                   MONGODB_FEEDBACK_PROFILEQUEUES_COLLECTION_NAME,MONGODB_PREPARING_PROFILE_QUEUES_COLLECTION_FOR_TRAINING)#,POSTGRES_HOST,POSTGRES_PORT,
                #    POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_DATABASE)

import ftplib
from pymongo import MongoClient
import boto3
# import psycopg2

#connecting to MongoDB
def resumeDetailsCollection():
    conn = MongoClient(str(f"{MONGODB_HOST}"), int(MONGODB_PORT))
    database = conn[f"{MONGODB_DATABASE_NAME}"]
    resume_details_collection = database[f"{MONGODB_RESUME_DETAILS_COLLECTION_NAME}"]
    return resume_details_collection,conn

def userDetailsCollection():
    conn = MongoClient(str(f"{MONGODB_HOST}"), int(MONGODB_PORT))
    database = conn[f"{MONGODB_DATABASE_NAME}"]
    user_details_collection = database[f"{MONGODB_USER_DETAILS_COLLECTION_NAME}"]
    return user_details_collection,conn

def filterWithSkillCollection():
    conn = MongoClient(str(f"{MONGODB_HOST}"), int(MONGODB_PORT))
    database = conn[f"{MONGODB_DATABASE_NAME}"]
    skill_details_collection = database[f"{MONGODB_FILTER_WITH_SKILL_COLLECTION_NAME}"]
    return skill_details_collection

def feedbackdetailsCollection():
    conn = MongoClient(str(f"{MONGODB_HOST}"), int(MONGODB_PORT))
    database = conn[f"{MONGODB_DATABASE_NAME}"]
    feedback_details_collection = database[f"{MONGODB_FEEDBACK_DETAIL_COLLECTION_NAME}"]
    return feedback_details_collection

def ProfilequeuesCollection():
    conn = MongoClient(str(f"{MONGODB_HOST}"), int(MONGODB_PORT))
    database = conn[f"{MONGODB_DATABASE_NAME}"]
    profile_queues_collection = database[f"{MONGODB_FEEDBACK_PROFILEQUEUES_COLLECTION_NAME}"]
    return profile_queues_collection,conn

def PreaparingProfilequeuesCollectionforTraining():
    conn = MongoClient(str(f"{MONGODB_HOST}"), int(MONGODB_PORT))
    database = conn[f"{MONGODB_DATABASE_NAME}"]
    preparing_profile_queues_collection = database[f"{MONGODB_PREPARING_PROFILE_QUEUES_COLLECTION_FOR_TRAINING}"]
    return preparing_profile_queues_collection,conn
#connecting to AWS
s3_client = boto3.client(f"{AWS_SERVICE}", region_name=f"{AWS_REGION_NAME}", aws_access_key_id=f"{AWS_ACCESS_KEY_ID}",
                            aws_secret_access_key=f"{AWS_SECRET_ACCESS_KEY}")


# def get_postgres_db_connection():
#     db_params = {
#         'dbname': str(f"{POSTGRES_DATABASE}"),
#         'user':str(f"{POSTGRES_USER}"),
#         'password': str(f"{POSTGRES_PASSWORD}"),
#         'host':str(f"{POSTGRES_HOST}"),
#         'port':str(f"{POSTGRES_PORT}")
#     }
#     return psycopg2.connect(**db_params)
# class MongoDBConnectionManager():
#     def __init__(self, hostname, port):
#         self.hostname = hostname
#         self.port = port
#         self.connection = None
 
#     def __enter__(self):
#         self.connection = MongoClient(self.hostname, self.port)
#         return self.connection
 
#     def __exit__(self, exc_type, exc_value, exc_traceback):
#         self.connection.close()