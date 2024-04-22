from pymongo import MongoClient
import pandas as pd
import csv  
import ftplib
from io import BufferedReader
import wget
import os
from connection import feedbackdetailsCollection
from config import (SKILL_KEY,DESIGNATION_KEY,ORGANIZATION_SET_KEY,EDUCATION_SET_KEY,CITIES_KEY,PRESENTADDRESS_KEY,
                    DATE_OF_BIRTH_KEY,COMPANIES_KEY,SECONDARY_SKILLS_KEY)
from logger import logging

skill_key = f"{SKILL_KEY}"
designation_key = f"{DESIGNATION_KEY}"
organization_set_key=f"{ORGANIZATION_SET_KEY}"
education_set_key=f"{EDUCATION_SET_KEY}"
cities_key=f"{CITIES_KEY}"
presentaddress_key=f"{PRESENTADDRESS_KEY}"
date_of_birth_key=f"{DATE_OF_BIRTH_KEY}"
companies_key=f"{COMPANIES_KEY}"
secondaryskill_key=f"{SECONDARY_SKILLS_KEY}"

cursor = feedbackdetailsCollection().find()
print(cursor)
def list_of_values_to_append(entity,cursor):
    # print(entity)
    feedback_list=[]
    for record in cursor:
        if type(record[entity])!=list:
            feedback_list.append(record[entity])
        elif type(record[entity])==list:
            feedback_list.extend(record[entity])
        elif record[entity]:
            feedback_list.append(record[entity])
        
        remove_emptyString=list(set(feedback_list))
        while("" in remove_emptyString) :
            remove_emptyString.remove("")
        while(" " in remove_emptyString) :
            remove_emptyString.remove(" ")
    return (remove_emptyString)


def writing_into_csv(new_list,csvfile):
    df=pd.read_csv(csvfile)
    entity_list=df['Header'].to_list()
    new_value=[]
    for value in new_list:
        if value not in entity_list:
            new_value.append([value])
    if 'Header' in new_value:
        new_value=new_value.remove('Header')

    data = new_value
    with open(csvfile, 'a', encoding='UTF8') as f:
        writer = csv.writer(f)

        for i in data:
            writer.writerow(i)

    print(1)
   

def feedback_fun():
    try:
        cursor = feedbackdetailsCollection().find()
        current_location_list=list_of_values_to_append("current_location",cursor)
        logging.info(f"current_location_list :{current_location_list}")

        cursor = feedbackdetailsCollection().find()
        current_designation_list=list_of_values_to_append("current_designation",cursor)
        logging.info(f"current_designation_list :{current_designation_list}")

        cursor = feedbackdetailsCollection().find()
        primary_skill_list=list_of_values_to_append("primary_skill",cursor)
        logging.info(f"primary_skill_list :{primary_skill_list}")

        education_list=list_of_values_to_append("education",cursor)
        logging.info(f"education_list :{education_list}")

        cursor = feedbackdetailsCollection().find()
        current_company_list=list_of_values_to_append("current_company",cursor)
        logging.info(f"current_company_list :{current_company_list}")

        # writing_into_csv(current_location_list,cities_key)
        # writing_into_csv(current_designation_list,designation_key)
        # writing_into_csv(primary_skill_list,skill_key)
        # writing_into_csv(education_list,education_set_key)
        # writing_into_csv(current_company_list,companies_key)
    except Exception as msg:
        print(msg)



