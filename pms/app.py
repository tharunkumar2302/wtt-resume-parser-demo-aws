import os
import time
import wget
import pandas as pd
from datetime import datetime, timezone
# import datetime
import textract
# import camelot
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
import numpy as np
import sys
import traceback
from utils import return_non_null_status
import PyPDF2
# from PyPDF2 import PdfReader
# import pdfplumber
from uuid import uuid4
import threading
import queue
import re
import csv
import openpyxl

import io
from io import BufferedReader
from connection import s3_client,ProfilequeuesCollection
from config import (API_KEY,DOCX_EXTENSIONS,DOC_EXTENSIONS,PDF_EXTENSIONS,AWS_S3_BUCKET_NAME,
                    AWS_ERRORS_FOLDER,AWS_FILES_FOLDER,CSV_EXTENSIONS,CSV_EXCEL_EXTENSIONS,XLSX_EXTENSIONS)
                   
from logger import logging
from constants import param_names,default_values

from utils import (totalTextProcessor, totalTextProcessorPDF,extract_secondary_skills,contains_days,contains_month,contains_week,contains_year,
                   get_experience,num_of_tokens_from_text,remove_brackets,extract_text_from_doc,change_dict_key,
                   extract_phone_number,extracting_entities_using_gpt,experience_processing)

from database import insertingIntoMongoDb,getIdRoleOrganizationIDS,updateinprofileQueues#emailPhonenumberCheckUpdate
from database_for_xlsx_csv import insertingIntoMongoDb_xlsx_csv,getIdRoleOrganizationIDS
from collections import defaultdict
import openai
openai.api_key = API_KEY
# MODEL_NAME = 'gpt-3.5-turbo'
MODEL_NAME = 'gpt-3.5-turbo-16k'

import json
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
#######
ocr = PaddleOCR(use_angle_cls=True, lang='en')
confidence_threshold = 0.1


from openai import OpenAI
# client = OpenAI(api_key=API_KEY)
from groq import Groq

current_date = datetime.now().strftime("%Y-%m-%d")
client = Groq(
    api_key="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",
)

delimiter = "####"
system_message = f"""<s>[INST]
Today's Date: {current_date}
**Task** - You are an experienced and very helpful job resume parser. Given the resume text delimited by {delimiter}, \
your goal is to analyze the resume and extract all given attributes.

**Procedure**
1. Rearrange the entire resume first for better resume attribute extraction. 
2. All the below attributes are crucial, please provide output for as many attributes possible.
3. Rearrange and filter the text further for better resume attribute extraction.
4. Provide "N/A" when corresponding attribute info is not provided.
5. Please extract ALL the following attributes using the given names ONLY, ensure consistent format :-
First Name:
Last Name:
Email ID: provide email id separated by commas
Mobile number: comma-separated for 2 numbers
Location: current city, state
Permanent Address:Full Address with all info
Date of Birth:date of birth in mm/dd/yyyy
Marital Status:"Married" or "Not Married"
Designation:Latest Designation of Person
Company:Latest Company name of Person
Experience: Parse the entire text. Please list the candidate's professional experiences within corporate environments. Determine the total years of corporate work experience as of today's data : {current_date}, excluding education, personal projects, or internships. Share the numerical value representing the total corporate work experience.
Education:return latest education of a person
Qualification:department or major of latest education
Education Institute:where the person pursued the latest degree
Marks in percentage:percentage or gpa person scored in latest education degree with unit
Specialization:
Year of passing:from the latest education degree
Primary Skills: Begin by thoroughly parsing the entire resume. Please provide comprehensive list of skills by extracting all programming languages, every technical skills, all coding languages, every coding/technical frameworks person has worked with in the text. Please provide your findings in the form of a detailed list.
Secondary Skills: Any other acquired skills which are not mentioned in primary skills or other attributes
Job Title:title of current job/designation
Job description:summarized description of the current job in 3 sentences(max 50 tokens)
Company Location:Current company location of a person
Industry:IT or Health or Hardware or Software industry e.t.c
Headline: Resume Main Experience Headline of the Person
Employment type:Full Time or Part Time of a person
Date of joining:joining date in latest company in "dd/mm/yyyy"
Last date: extract last working date of latest work experience and return in "mm/yyyy" 
Current CTC:return 0 if not present
Expected CTC:return 0 if not present
Current Employment Status: check Last employment date against Today's date, or check current working status mentioned in the text, return "working" if employee is presently working, else "not working"
Prefered Location:prefered job locations of a person
Ready to relocate:"Yes" if candidate is open to relocation else "No" if candidate is Not Open to Relocation.
Overseas Experience:Do person work experience span multiple countries? Please indicate with a simple True or False.
Notice Period: If candidate has specifically provided this information, please return value in number of days
Having Passport:Do person have a valid passport? Please indicate with a simple True or False.
Passport Validity:return the validity of a passport
Visa:True or False
About:Absolutely Mandatory field. Generate a short summary of the profile in less than 50 tokens

6. Make an effort again to extract info for all attributes marked as "N/A", if you cannot, mark as "N/A". Thank YOU.

"""
def extracting_entities_using_groq(text):
    time.sleep(4)
    try:
        user_message = f"""{text}"""

        messages =  [
                    {'role':'system',
                    'content': system_message},
                    {'role':'user',
                        'content': f"{delimiter}{user_message}{delimiter}" + """\nAdhere to all instructions and extract info for all attributes marked as "N/A" till 'About' attribute, if you cannot, mark as "N/A".Thank YOU.[/INST]"""},
                    ]
        chat_completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages,
            temperature=0.0,
            max_tokens=None,
            top_p = 1,
            frequency_penalty=0.1            
            )

        response=chat_completion.choices[0].message.content
        return response
    except:
        return None
# def text_with_gpt_turbo(formatted_text):
#     openai.api_key = API_KEY
#     # MODEL_NAME = 
#     llm = ChatOpenAI(model_name=MODEL_NAME, temperature=0, openai_api_key=openai.api_key)
    
#     # llm = ChatOpenAI(model_name=MODEL_NAME,openai_api_key=API_KEY)
#     # Few-shot learning prompt
#     prompt = """You are an experienced resume attributes extracter. Given the following resume, you will extract the requested information in JSON format.
#     {formatted_text}
#     Please extract the following information using the given names ONLY:
#     - First Name
#     - Last Name
#     - Email ID: sample output format: email1, email2
#     - Mobile number: sample ouy
#     - Location
#     - Present Address
#     - Date of Birth
#     - Marital Status
#     - Designation:return Latest Designation of a Person else return empty string
#     - Company:return Latest Company name of a Person else return empty string
#     - Experience:return the total years of experience the candidate has since the first job till Today's Date. return just the numerical else return 0
#     - Education:return Highest degree of a person if present else empty string
#     - Qualification:return Highest degree of a person if present else empty string
#     - Education Institute:return the institute/college name where the person studied highest degree if present else empty string
#     - Marks in percentage:return how much percentage person scored in higest degree if present else empty string
#     - Specialization:return specialization in higest degree if present else empty string
#     - Year of passing:return in which year he passed the highest degree if present else empty string
#     - Primary Skills: return ALL the technical skills provided in the content as a list else return empty string. ALWAYS Include all the technical skills from experience section and any section named like "Technical Skills" in the entire given content.Exclude any text that are mentioned inside the Products Specialization and skills that are prefixed with "Trained on", "having knowledge of", or "Learned".
#     - Secondary Skills: Extract skills that are prefixed with "Trained on", "having knowledge of", or "Learned". Exclude any skills that are not prefixed with these phrases. Also exclude any skills that are listed as primary skills, mentioned in the projects or experience sections, or mentioned in any other section. If no matching skills are found, return an empty string.
#     - Job Title:return the title of a job/designation if present else empty string
#     - Job description:return description of the job if present else empty string
#     - Company Location:Latest company location of a person if present else empty string
#     - Industry:return IT or Health or Hardware or Software industry e.t.c... else return empty string
#     - Headline:return Experience Headline of a person if present else empty string
#     - Employment type:return Full Time or Part Time of a person
#     - Date of joining:return joined date of the last company if present else empty string
#     - Last date:return last date of a company if present else empty string
#     - Current CTC:return just the numerical of current ctc if present else return 0 if not present
#     - Expected CTC:return just the numerical of expected ctc if present else return 0 if not present
#     - Current Employment Status:return employee status if present else empty string
#     - Prefered Location:return prefered location of a person if present else empty string
#     - Ready to relocate:return True if present else False
#     - Overseas Experience:return True if present else False
#     - Notice Period:Extract the notice period should be a numerical value along with its unit (weeks,months, days, or years)e.g:5 days or 3 months or 2 weeks e.t.c. return 0 if Immediate joining present in the text else return empty string.
#     - Having Passport:return True if present else False
#     - Passport Validity:return the validity of a passport if present else empty string
#     - Visa:return True if present else False
#     - About: Generate a Summary of the profile in 2-3 lines
#     """
#     prompt_template = PromptTemplate(input_variables=["formatted_text"], template=prompt)
#     extract_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="response")
#     resp = extract_chain.run(formatted_text=formatted_text)
#     print(resp)
    
#     # Handle 'Not mentioned' and convert to empty string
#     data = json.loads(resp)
#     for key, value in data.items():
#         if isinstance(value, str) and value == 'Not mentioned':
#             data[key] = ''
    
#     print(type(data))
#     return data


# def small_text(formatted_text):
#     # try:
#     response = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": f"{delimiter}{formatted_text}{delimiter}"},#formatted_text},
#     ],
#     temperature=0.0
#     # max_tokens=2000,
#     # api_key=API_KEY  # Pass the API key here
#     )
#     #completion = client.completions.create(model="gpt-3.5-turbo", prompt=system_message)
#     # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[f"{delimiter}{formatted_text}{delimiter}"])

#     # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
#     # print(response)
#     extracted_info=response.choices[0].message.content.strip()
#     print(extracted_info)
#     # extracted_info = response['choices'][0]['message']['content'].strip()
#     dictionary = {}
#     lines = extracted_info.split('\n')
#     lines = [s.lstrip( '- ' ) if s.startswith( '-' ) else s for s in lines]
#     for line in lines:
#         if line.strip():
#             key, value = line.split(':')
#             dictionary[key.strip()] = value.strip()

#     # dictionary = {key.lstrip('- '): value for key, value in dictionary.items()}
#     # dictionary = {key.lstrip( '- ' ): value for key, value in dictionary.items() if key.startswith( '- ' )} 
#     # dictionary.update({key: value for key, value in dictionary.items() if not key.startswith( '- ' )}) 
#     return dictionary
#     # except Exception as e:
    #     print(f"Error: {e}")
    #     pass

    # return dictionary

# def chunk_text(text, max_chunk_length):
#     chunks = []
#     current_chunk = ''
#     for sentence in text.split('.'):
#         if len(current_chunk) + len(sentence) + 1 <= max_chunk_length:
#             current_chunk += sentence + '. '
#         else:
#             chunks.append(current_chunk.strip())
#             current_chunk = sentence + '. '
#     if current_chunk:
#         chunks.append(current_chunk.strip())
#     return chunks

# def long_text(formatted_text):
#     delimiter = "####"
#     text_chunks = chunk_text(formatted_text, max_chunk_length=2000)
#     # print(text_chunks)
#     params = {
#         "First Name": "",
#         "Last Name": "",
#         "Email ID": "",
#         "Mobile number": "",
#         "Location": "",
#         "Present Address": "",
#         "Date of Birth": "",
#         "Marital Status": "",
#         "Designation": "",
#         "Company": "",
#         "Experience": "",
#         "Education": "",
#         "Qualification": "",
#         "Education Institute": "",
#         "Marks in percentage": "",
#         "Specialization": "",
#         "Year of passing": "",
#         "Primary Skills": "",
#         "Secondary Skills": "",
#         "Job Title": "",
#         "Job description": "",
#         "Company Location": "",
#         "Industry": "",
#         "Headline": "",
#         "Employment type": "",
#         "Date of joining": "",
#         "Last date": "",
#         "Current CTC": "",
#         "Expected CTC": "",
#         "Current Employment Status": "",
#         "Prefered Location": "",
#         "Ready to relocate": "",
#         "Overseas Experience": "",
#         "Notice Period": "",
#         "Having Passport": "",
#         "Passport Validity": "",
#         "Visa": "",
#         "About": ""
#     }
    
#     for chunk in text_chunks:
#         # try:
#     #     response = openai.ChatCompletion.create(
#     #     model="gpt-3.5-turbo",
#     #     messages=[
#     #     {"role": "system", "content": system_message},
#     #     {"role": "user", "content": f"{delimiter}{chunk}{delimiter}"},#formatted_text},
#     # ],
#     #     temperature=0.0,
#     #     max_tokens=2000,
#     #     api_key=API_KEY  # Pass the API key here
#     #     )
#         response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": f"{delimiter}{chunk}{delimiter}"},#formatted_text},
#         ],
#         temperature=0.0
#         # max_tokens=2000,
#         # api_key=API_KEY  # Pass the API key here
#         )

#         # extracted_info = response['choices'][0]['message']['content'].strip()
#         extracted_info=response.choices[0].message.content.strip()
#         print(extracted_info)

        
#         lines = extracted_info.split("\n")
#         # print("lines====",lines)
#         lines = [s.lstrip( '- ' ) if s.startswith( '-' ) else s for s in lines]
#         # print("lines1====",lines)
#         for line in lines:
#             line=line.strip()
#             for param in params:
#                 if line.startswith(param):
#                     value = line.split(":")[-1].strip()
#                     if not params[param]:
#                         params[param] = value
#         # except Exception as e:
#         #     print(e)
        
#     for key, value in params.items():
#         if value == 'Not mentioned':
#             params[key] = ''
#     # print(params)
#     # params = {key.lstrip( '- ' ): value for key, value in params.items() if key.startswith( '- ' )} 
#     # params.update({key: value for key, value in params.items() if not key.startswith( '- ' )}) 
#     # print("params=====",params)
#     # print(type(params))
#     return params
    # return params

def insert_into_mongo(filename,total_text_with_info, total_text, res,job_list_append,filepath):
    logging.info(f"entered into insert_into_mongo function ")
    experience = "" 
    try:
        text=" ".join(total_text)
        logging.info(f'total_text:{text}')
        if len(text)>100:
            # token_count=num_of_tokens_from_text(text,model='gpt-3.5-turbo')
            # logging.info(f"token count: {token_count}")
            # if token_count<3000:
            #     print("entered into ============>if")
            #     try:
            #         print("entered into ===========try block inside if")
            #         time.sleep(1)
            #         response=small_text(text)
            #         # print(response)
            #     except:
            #         try:
            #             print("Exception occurred in small_text method==>try")
            #             time.sleep(1)
            #             logging.info(f'entered into try')
            #             response=text_with_gpt_turbo(text)
            #         except:
            #             time.sleep(2)
            #             logging.info(f'entered into except')
            #             try:
            #                 response=long_text(text)
            #                 # print("response=====",response)
            #                 # print(type(response))
            #             except:
            #                 logging.info(f"got error for this file  {filename}")
            #                 pass
            # else:
            #     print("entered into ============>else")
            #     try:
            #         time.sleep(1)
            #         response=long_text(text)
            #         # print("response=====",response)
            #         # print(type(response))
            #         # print(response)
            #     except:
            #         try:
            #             time.sleep(1)
            #             logging.info(f'entered into try')
            #             response=text_with_gpt_turbo(text)
            #         except:
            #             time.sleep(2)
            #             logging.info(f'entered into except')
            #             try:
            #                 response=small_text(text)
            #             except:
            #                 logging.info(f"got error for this file  {filename}")
            #                 pass

            # user_message = f"""{text}"""

            # messages =  [
            #             {'role':'system',
            #             'content': system_message},
            #             {'role':'user',
            #             'content': f"{delimiter}{user_message}{delimiter}"},
            #             ]
            # chat_completion = client.chat.completions.create(
            #     model="mixtral-8x7b-32768",
            #     messages=messages,
            #     temperature=0.0,
            #     max_tokens=None,
            #     top_p = 1,
            #     frequency_penalty=0.0            
            #     )
            
            # response=chat_completion.choices[0].message.content
            response=extracting_entities_using_groq(text)
            

            # print(response)
            logging.info(f"extracting_entities_using_groq :{response}")

            organization_id=''
            createdByUserId=''
            modifiedByUserId=''
            createdByUserRole=''
            modifiedByUserRole=''

            try:
                organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole=getIdRoleOrganizationIDS(filepath)
            except Exception as msg:
                logging.info(f"{msg}")
                pass
            try:
                if response:
                    # response=extract_info(response)
                    if type(response) == str:
                        try:
                            # Splitting the string into lines and then into key-value pairs
                            lines = response.strip().split('\n')
                            response_dict = {}
                            key = None
                            for line in lines:
                                parts = line.strip().split(': ', 1)
                                if len(parts) == 2:
                                    key, value = parts
                                    response_dict[key.strip()] = value.strip()
                                elif key is not None:
                                    response_dict[key] += '\n' + line.strip()
                            
                            response = response_dict

                            print("dict length:", len(response))
                            len_value = 0
                            if len(response) < 38 and len_value < 3:
                                for i in range(2):
                                    response = extracting_entities_using_groq(text)
                                    lines = response.strip().split('\n')
                                    response_dict = {}
                                    key = None
                                    for line in lines:
                                        parts = line.strip().split(': ', 1)
                                        if len(parts) == 2:
                                            key, value = parts
                                            response_dict[key.strip()] = value.strip()
                                        elif key is not None:
                                            response_dict[key] += '\n' + line.strip()
                                    response = response_dict
                                    print("dict length:", len(response))
                                    len_value += 1
                        except Exception as e:
                            print("Exception occurred:", e)
                            print("Entered into except block")
                            pass
                            # Handle the exception gracefully
                            # response = {}
                        # try:
                        #     # Splitting the string into lines and then into key-value pairs
                        #     pairs = [line.strip().split(': ', 1) for line in response.strip().split('\n')]
                        #     # Converting the list of key-value pairs into a dictionary
                        #     if pairs:
                        #         # print("pairs=====",pairs)
                        #         # Converting the list of key-value pairs into a dictionary
                        #         response = dict(pairs)
                        #         # print(response)
                        #         print("dict length", len(response))
                        #         len_value=0
                        #         if len(response)<38 and len_value<3:
                        #             for i in range(2):
                        #                 response=extracting_entities_using_groq(text)
                        #                 pairs = [line.strip().split(': ', 1) for line in response.strip().split('\n')]
                        #                 response = dict(pairs)
                        #                 print("dict length", len(response))
                        #                 len_value+=1
                        # except:
                        #     print("entered into except===========")
                        #     # response = {}

                        #     # Parse the data and populate the dictionary
                        #     lines = response.strip().split('\n')

                        #     response = {}
                        #     for line in lines:
                        #         if ':' in line:
                        #             key, value = line.strip().split(': ', 1)
                        #             response[key.strip()] = value.strip()
                        #         else:
                        #             response[key] = response.get(key, '') + '\n' + line.strip()


                            # Print the resulting dictionary
                            # print(response)

                    for key in response:
                        response[key] = response[key].strip()


                    try:
                        change_dict_key(response, 'Permanent Address', 'Present Address')
                    except:
                        pass
                    print(response)
                        # response = dict(pairs)
                        # print("dict length",len(response))
                    

                    # Printing the resulting dictionary
                    # response=change_dict_key(response, 'Permanent Address', 'Present Address')
                    # print(response)
                    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', response['Email ID'])
                    if email:
                        response['Email ID'] = email.group()
                    else:
                        response['Email ID'] = ''

                    # Extracting mobile number
                    mobile_number = extract_phone_number(response['Mobile number'])
                    # re.search(r'\+\d{1,2}\s?\d{10}', response['Mobile number'])
                    if mobile_number:
                        response['Mobile number'] = mobile_number
                    else:
                        response['Mobile number'] = ''

                    # Filtering Experience to be numerical or float
                    try:
                        if re.search(r"\d+\s+(Months|months|month|MONTH|Month)", str(response['Experience'])):
                            response['Experience'] = experience_processing(str(response['Experience']))
                        else:
                            try:
                                experience = re.search(r'\d+(\.\d+)?', response['Experience'])
                                if experience:
                                    response['Experience'] = experience.group()
                                else:
                                    response['Experience'] = ''
                            except:
                                response['Experience'] = ''
                    except:
                        response['Experience']=''

                    # Replacing 'N/A', 'Not provided', or 'Not specified' with empty string
                    for key, value in response.items():
                        if value.strip() in ['N/A', 'Not provided', 'Not specified']:
                            response[key] = ''
                    merged_data = {**default_values, **response}
                    df = pd.DataFrame([merged_data], index=[0])
            except:
                print("============NER using gpt============")
                logging.info("============NER using gpt============")
                response=extracting_entities_using_gpt(text,filename)
                merged_data = {**default_values, **response}
                df = pd.DataFrame([merged_data], index=[0])
                # pass

            if len(response) < 38:
                print("============NER using gpt============")
                logging.info("============NER using gpt============")
                logging.info("============NER using gpt len(response) < 38============")
                response=extracting_entities_using_gpt(text,filename)
                merged_data = {**default_values, **response}
                df = pd.DataFrame([merged_data], index=[0])

            if response==None:
                print("============NER using gpt============")
                logging.info("============NER using gpt============")
                response=extracting_entities_using_gpt(text,filename)
                merged_data = {**default_values, **response}
                df = pd.DataFrame([merged_data], index=[0])


            try:
                cv_url=None
                collection,conn = ProfilequeuesCollection()
                query = {"file_path": f"{filepath}"}
                cv_url = [doc["cv_url"] for doc in collection.find(query)][0]
                print("filepath====>:",filepath)
                print("cv_url====>:",cv_url)
            except:
                pass
            finally:
                conn.close()
                
            # logging.info(f'response====>:{response}')
            # logging.info(f'firstName:{response["First Name"]}')
            # logging.info(f'lastName:{response["Last Name"]}')
            logging.info(f'email:{response["Email ID"]}')
            logging.info(f'phone_no:{response["Mobile number"]}')
            try:
                firstName=response["First Name"]
            except:
                firstName=''
            
            try:
                lastName=response["Last Name"]
            except:
                lastName=''

            try:
                email=response["Email ID"]
            except:
                email=""

            try:
                phone_no=response["Mobile number"]
            except:
                phone_no=""

            try:
                loc=response["Location"]
            except:
                loc=""

            try:
                present_address=response["Present Address"]
            except:
                present_address=""

            try:
                DateofBirth=response["Date of Birth"]
            except:
                DateofBirth=""

            try:
                maritial_status=response["Marital Status"]
            except:
                maritial_status=""

            try:
                recent_designation=response["Designation"]
            except:
                recent_designation=""

            try:
                resume_organisation=response["Company"]
            except:
                resume_organisation=""

            try:
                experience=response["Experience"]
                if re.search(r"\d+\s+(Months|months|month|MONTH|Month)", str(experience)):
                    experience = experience_processing(str(experience))
                else:
                    try:
                        experience = re.search(r'\d+(\.\d+)?', str(experience))
                        if experience:
                            experience = experience.group()
                        else:
                            experience = ''
                    except:
                        experience = ''
            except:
                experience=""
            
            try:
                current_education=response["Education"]
            except:
                current_education=""

            try:
                qualification=response["Qualification"]
            except:
                qualification=""

            try:
                institute=response["Education Institute"]
            except:
                institute=""

            try:
                try:
                    marks_in_percentage=response["Marks in percentage"]
                except:
                    marks_in_percentage=response["Marks in Percentage"]
            except:
                marks_in_percentage=""

            try:
                specialization=response["Specialization"]
            except:
                specialization=''

            try:
                try:
                    year_of_passing=response["Year of passing"]
                except:
                    year_of_passing=response["Year of Passing"]
            except:
                year_of_passing=""

            try:
                resume_skill=response["Primary Skills"]
            except:
                resume_skill=""

            try:   
                if type(resume_skill)==str:
                    resume_skill = [item.strip() for item in resume_skill.split(",")]
            except:
                pass

            try:
                resume_skill = remove_brackets(resume_skill)
            except:
                pass
            

            try:
                secondary_skills=extract_secondary_skills(str(total_text))
            except:
                secondary_skills=""

            # response["Secondary Skills"]
            # if type(secondary_skills)==str:
            #     secondary_skills = [item.strip() for item in secondary_skills.split(",")]


            try:
                job_title=response["Job Title"]
            except:
                job_title=''
            try:
                try:
                    description=response["Job description"]
                except:
                    description=response["Job Description"]
            except:
                description=''

            try:
                company_name=response["Company"]
            except:
                company_name=""

            try:
                location=response["Company Location"]
            except:
                location=""

            try:
                industry=response["Industry"]
            except:
                industry=""

            try:
                headline=response["Headline"]
            except:
                headline=""

            try:
                try:
                    employment_type=response["Employment type"]
                except:
                    employment_type=response["Employment Type"]
            except:
                employment_type=""

            try:
                try:
                    date_of_joining=response["Date of joining"]
                except:
                    date_of_joining=response["Date of Joining"]
            except:
                date_of_joining=""

            try:
                try:
                    last_date=response["Last date"]
                except:
                    last_date=response["Last Date"]
            except:
                last_date=""
                
            try:
                current_ctc=response["Current CTC"]
            except:
                current_ctc=""

            try:
                current_ctc=int(current_ctc)
            except:
                try:
                    current_ctc=float(current_ctc)
                except:
                    current_ctc=""
                    pass
            
            try:
                expected_ctc=response["Expected CTC"]
            except:
                expected_ctc=""

            try:
                expected_ctc=int(expected_ctc)
            except:
                try:
                    expected_ctc=float(expected_ctc)
                except:
                    expected_ctc=""
                    pass

            try:
                current_employment_status=response["Current Employment Status"]
            except:
                current_employment_status=""

            try:
                try:
                    prefered_location=response["Prefered Location"]
                except:
                    prefered_location=response["Prefered location"]
            except:
                prefered_location=""

            try:
                try:
                    ready_to_relocate=response["Ready to relocate"]
                except:
                    ready_to_relocate=response["Ready to Relocate"]
            except:
                ready_to_relocate=""
                
            try:
                try:
                    overseas_experience=response["Overseas Experience"]
                except:
                    overseas_experience=response["Overseas experience"]
            except:
                overseas_experience=""

            notice_period_in_month=0
            notice_period_in_year=0
            notice_period_in_days=0
            notice_period_in_week=0
            try:
                notice_period=response["Notice Period"]
                if notice_period:
                    if contains_month(str(notice_period)):
                        try:
                            notice_period_in_month=int(str(notice_period).split()[0])
                        except:
                            notice_period_in_month=float(str(notice_period).split()[0])
                    elif contains_year(str(notice_period)):
                        try:
                            notice_period_in_year=int(str(notice_period).split()[0])
                        except:
                            notice_period_in_year=float(str(notice_period).split()[0])
                    elif contains_days(str(notice_period)):
                        try:
                            notice_period_in_days=int(str(notice_period).split()[0])
                        except:
                            notice_period_in_days=float(str(notice_period).split()[0])
                    elif contains_week(str(notice_period)):
                        try:
                            notice_period_in_week=int(str(notice_period).split()[0])
                        except:
                            notice_period_in_week=int(str(notice_period).split()[0])
                # notice_period=int(notice_period)
            except:
                notice_period=0
            
            try:
                having_passport=response["Having Passport"]
            except:
                having_passport=""

            try:
                passport_validity=response["Passport Validity"]
            except:
                passport_validity=""

            try:
                visa=response["Visa"]
            except:
                visa=""

            try:
                About=response["About"]
            except:
                About=""

            if email and phone_no:
                status='Published'
            else:
                status='Draft'

            try:
                if experience and experience!='':
                    exp=''
                    for value in experience:
                        if value.isdigit() or value==".":
                            exp+=value
                    experience=float(exp)
            except:
                experience=''
                pass

            # try:
            #     exp=get_experience(text)
            #     if exp!='':
            #         if "." in exp:
            #             exp = float(re.search(r'\d+(\.\d+)?', str(exp)).group())
            #             experience=exp
            #         else:
            #             exp=int(re.search(r'\d+', str(exp)).group())
            #             experience=exp
            # except:
            #     pass

            if phone_no:
                # Remove non-digit characters and extract the last 10 digits
                try:
                    phone_no = re.sub(r'\D', '', phone_no)
                    phone_no = phone_no[-10:]
                except:
                    try:
                        phone_no = phone_no[0]
                    except:
                        pass


            pinecone_mongo_uuid_val=str(uuid4())
            logging.info(f'response====>:{response}')
            #inserting into mongodb
            insert_status=insertingIntoMongoDb(firstName,lastName,email,phone_no,loc,present_address,
            DateofBirth,maritial_status,recent_designation,resume_organisation,experience,current_education,
            qualification,institute,marks_in_percentage,specialization,year_of_passing,resume_skill,
            secondary_skills,job_title,description,company_name,location,industry,headline,employment_type,
            date_of_joining,last_date,current_ctc,expected_ctc,current_employment_status,prefered_location,
            ready_to_relocate,overseas_experience,notice_period,having_passport,passport_validity,visa,About,
            status,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,filename,pinecone_mongo_uuid_val,df,filepath,cv_url,
            notice_period_in_month,notice_period_in_year,notice_period_in_days,notice_period_in_week,text,response)
            
            # filename,candidate_name,
            #                     loc,present_address,DateofBirth,maritial_status,recent_designation,
            #                     resume_organisation,experience,current_education,education_detailed_history,
            #                         resume_skill,secondary_skills,experience_detailed_history,status,
            #                         organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,total_text)
            
            logging.info(f'insert_status :{insert_status}')
            if insert_status==True:
                try:
                    collection,conn=ProfilequeuesCollection()
                    # Update the records with the specified criteria
                    query = {"isProcessed": False,"file_path":f"{AWS_FILES_FOLDER}/{filename}"}
                    update = {"$set": {
                        "isProcessed": True,
                        "processedDateTime": datetime.now(tz=timezone.utc),
                        "Remarks": "processed successfully",
                        "updatedAt": datetime.now(tz=timezone.utc),
                    }}
                    result = collection.update_one(query, update)

                    logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
                finally:
                    conn.close()
            return firstName,lastName,email,phone_no,loc,present_address,DateofBirth,maritial_status,recent_designation,resume_organisation,experience,current_education,qualification,institute,marks_in_percentage,specialization,year_of_passing,resume_skill,secondary_skills,job_title,description,company_name,location,industry,headline,employment_type,date_of_joining,last_date,current_ctc,expected_ctc,current_employment_status,prefered_location,ready_to_relocate,overseas_experience,notice_period,having_passport,passport_validity,visa,About,status,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,filename
            #email,phone_no,id,filename,candidate_name,loc,present_address,DateofBirth,maritial_status,recent_designation,resume_organisation,experience,current_education,education_detailed_history,resume_skill,secondary_skills,experience_detailed_history,status,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole
        else:
            s3_client.upload_file(
            filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
            )
            logging.info(f"Error: {msg}, Type: {type(msg)} ,{traceback.print_exc()}")
            try:
                collection,conn=ProfilequeuesCollection()
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
            s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

            logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
            os.remove(filename)
            pass
            
    except Exception as msg:
        s3_client.upload_file(
        filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
        )
        logging.info(f"Error: {msg}, Type: {type(msg)} ,{traceback.print_exc()}")
        try:
            collection,conn=ProfilequeuesCollection()
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
        s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

        logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
        os.remove(filename)
        pass
    



def textExtractionFromResume(filename,filepath):
    print("=============Extraction from resume================")
    try:
        experience = None 
        logging.info(f"filename in textExtractionFromResume :{filename}")
        # document_path=filename
        suffix1=tuple(DOCX_EXTENSIONS)
        suffix2=tuple(DOC_EXTENSIONS)
        suffix3=tuple(PDF_EXTENSIONS)
        suffix4=tuple(CSV_EXCEL_EXTENSIONS)
        suffix5=tuple(CSV_EXTENSIONS)
        suffix6=tuple(XLSX_EXTENSIONS)
        filename=str(filename)
        if filename.endswith(suffix2):#if file name ends with .doc
            logging.info(f"using doc:{filename}")
            try:
                education_list_append=[]
                job_list_append=[]
                # file='/home/walkingtree/pathfiles/old_path/'
                try:
                    textract_data = textract.process(filename)
                    text1 = textract_data.decode("utf-8")
                except:
                    text1 = extract_text_from_doc(filename)
                # text1 = textract_data.decode("utf-8")
                lines = text1.split('\n')
                total_text_with_info=[]
                total_text=[]
                for ele in enumerate(lines):
                    dict = {}
                    dict['text']=ele[1]
                    dict['line_number']=ele[0]
                    total_text_with_info.append(dict)
                    total_text.append(ele[1])

                total_text=totalTextProcessor(total_text)
                extracted_data=insert_into_mongo(filename,total_text_with_info, total_text,education_list_append,job_list_append,filepath)
            except Exception as msg:
                s3_client.upload_file(
                filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
                )
                logging.info(f"Error: {msg}, Type: {type(msg)} ,{traceback.print_exc()}")
                try:
                    collection,conn=ProfilequeuesCollection()
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
                s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

                # logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
                os.remove(filename)
                pass

        elif filename.endswith((".csv",".xlsx")):#if file name ends with .csv/ xlsx
            print("using csv/xlsx")
            logging.info(f"using csv/xlsx:{filename}")
            # Create a dictionary to store the variable names and their corresponding values
            variables = {param_name: "" for param_name in param_names}
            try:
                if filename.endswith(suffix5):
                    # Open the CSV file
                    with open(filename, newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        
                        # Determine the column names from the CSV file and modify them
                        column_names= [col for col in reader.fieldnames]
                        # Iterate through each row
                        for row in reader:
                            # Assign values to variables based on matching column names (case-insensitive)
                            for param_name in param_names:
                                modified_param_name = re.sub(r'\([^)]*\)|_', '', param_name.lower())
                                for column_name in column_names:
                                    column_name1=re.sub(r'\([^)]*\)|_', '', column_name.lower())
                                    column_name1=''.join(column_name1.split())
                                    if str(modified_param_name).strip() == str(column_name1).strip():
                                        variables[param_name] = row[column_name]
                                        break
                        
                            # # Print the assigned variable values
                            # for param_name, value in variables.items():
                            #     print(f"{param_name}: {value}")
                            firstName=variables['firstName']
                            lastName=variables['lastName']
                            email= variables['email']
                            phone_no= variables['phone_no']
                            loc= variables['current_location']
                            present_address= variables['present_address']
                            DateofBirth= variables['DateofBirth']
                            maritial_status= variables['maritial_status']
                            recent_designation= variables['recent_designation']
                            resume_organisation= variables['resume_organisation']
                            experience= variables['experience']
                            current_education= variables['current_education']
                            qualification= variables['qualification']
                            institute= variables['institute']
                            marks_in_percentage= variables['marks_in_percentage']
                            specialization= variables['specialization']
                            year_of_passing= variables['year_of_passing']
                            resume_skill= variables['resume_skill']
                            secondary_skills= variables['secondary_skills']
                            job_title= variables['job_title']
                            description= variables['description']
                            company_name= variables['company_name']
                            location= variables['company_location']
                            industry= variables['industry']
                            headline= variables['headline']
                            employment_type= variables['employment_type']
                            date_of_joining= variables['date_of_joining']
                            last_date= variables['last_date']
                            current_ctc= variables['current_ctc']
                            expected_ctc= variables['expected_ctc']
                            current_employment_status= variables['current_employment_status']
                            prefered_location= variables['prefered_location']
                            ready_to_relocate= variables['ready_to_relocate']
                            overseas_experience= variables['overseas_experience']
                            notice_period_in_month=0
                            notice_period_in_year=0
                            notice_period_in_days=0
                            notice_period_in_week=0
                            notice_period= variables['notice_period']
                            if notice_period:
                                if contains_month(str(notice_period)):
                                    try:
                                        notice_period_in_month=int(str(notice_period).split()[0])
                                    except:
                                        notice_period_in_month=float(str(notice_period).split()[0])
                                elif contains_year(str(notice_period)):
                                    try:
                                        notice_period_in_year=int(str(notice_period).split()[0])
                                    except:
                                        notice_period_in_year=float(str(notice_period).split()[0])
                                elif contains_days(str(notice_period)):
                                    try:
                                        notice_period_in_days=int(str(notice_period).split()[0])
                                    except:
                                        notice_period_in_days=float(str(notice_period).split()[0])
                                elif contains_week(str(notice_period)):
                                    try:
                                        notice_period_in_week=int(str(notice_period).split()[0])
                                    except:
                                        notice_period_in_week=int(str(notice_period).split()[0])
                            having_passport= variables['having_passport']
                            passport_validity= variables['passport_validity']
                            visa= variables['visa']
                            About= variables['About']

                            organization_id=''
                            createdByUserId=''
                            modifiedByUserId=''
                            createdByUserRole=''
                            modifiedByUserRole=''

                            try:
                                organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole=getIdRoleOrganizationIDS(filepath)
                            except Exception as msg:
                                logging.info(f"{msg}")
                                pass

                            if variables:
                                # print(response)
                                df = pd.DataFrame(variables, index=[0])
                                print("df=======>",df)

                            try:
                                cv_url=""
                                # collection = ProfilequeuesCollection()
                                # query = {"file_path": f"{filepath}"}
                                # cv_url = [doc["cv_url"] for doc in collection.find(query)][0]
                                # print("filepath====>:",filepath)
                                # print("cv_url====>:",cv_url)
                            except:
                                pass

                            if email and phone_no:
                                status='Published'
                            else:
                                status='Draft'

                            pinecone_mongo_uuid_val=str(uuid4())

                            insert_status=insertingIntoMongoDb_xlsx_csv(firstName,lastName,email,phone_no,loc,present_address,
                            DateofBirth,maritial_status,recent_designation,resume_organisation,experience,current_education,
                            qualification,institute,marks_in_percentage,specialization,year_of_passing,resume_skill,
                            secondary_skills,job_title,description,company_name,location,industry,headline,employment_type,
                            date_of_joining,last_date,current_ctc,expected_ctc,current_employment_status,prefered_location,
                            ready_to_relocate,overseas_experience,notice_period,having_passport,passport_validity,visa,About,
                            status,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,filename,pinecone_mongo_uuid_val,df,filepath,cv_url,
                            notice_period_in_month,notice_period_in_year,notice_period_in_days,notice_period_in_week)
                    updateinprofileQueues(filename)

                elif filename.endswith(suffix6):
                    # Create a dictionary to store the variable names and their corresponding values
                    variables = {param_name: "" for param_name in param_names}

                    # Open the Excel file
                    workbook = openpyxl.load_workbook(filename)
                    worksheet = workbook.active
                    worksheet.insert_rows(1)

                    # Determine the column names from the Excel file and modify them
                    column_names = [col.value for col in worksheet[2]]

                    # Iterate through each row, skipping the first row (header)
                    for row in worksheet.iter_rows(min_row=2, values_only=True):
                        # Assign values to variables based on matching column names (case-insensitive)
                        for param_name in param_names:
                            modified_param_name = re.sub(r'\([^)]*\)|_', '', param_name.lower())
                            for column_name in column_names:
                                column_name1 = re.sub(r'\([^)]*\)|_', '', str(column_name).lower())
                                column_name1=''.join(column_name1.split())
                                if str(modified_param_name).strip() == str(column_name1).strip():
                                    variables[param_name] = row[column_names.index(column_name)]
                                    break

                        # Print the assigned variable values
                        # for param_name, value in variables.items():
                        #     print(f"{param_name}: {value}")
                        firstName=variables['firstName']
                        lastName=variables['lastName']
                        email= variables['email']
                        phone_no= variables['phone_no']
                        loc= variables['current_location']
                        present_address= variables['present_address']
                        DateofBirth= variables['DateofBirth']
                        maritial_status= variables['maritial_status']
                        recent_designation= variables['recent_designation']
                        resume_organisation= variables['resume_organisation']
                        experience= variables['experience']
                        current_education= variables['current_education']
                        qualification= variables['qualification']
                        institute= variables['institute']
                        marks_in_percentage= variables['marks_in_percentage']
                        specialization= variables['specialization']
                        year_of_passing= variables['year_of_passing']
                        resume_skill= variables['resume_skill']
                        secondary_skills= variables['secondary_skills']
                        job_title= variables['job_title']
                        description= variables['description']
                        company_name= variables['company_name']
                        location= variables['company_location']
                        industry= variables['industry']
                        headline= variables['headline']
                        employment_type= variables['employment_type']
                        date_of_joining= variables['date_of_joining']
                        last_date= variables['last_date']
                        current_ctc= variables['current_ctc']
                        expected_ctc= variables['expected_ctc']
                        current_employment_status= variables['current_employment_status']
                        prefered_location= variables['prefered_location']
                        ready_to_relocate= variables['ready_to_relocate']
                        overseas_experience= variables['overseas_experience']
                        notice_period_in_month=0
                        notice_period_in_year=0
                        notice_period_in_days=0
                        notice_period_in_week=0
                        notice_period= variables['notice_period']
                        if notice_period:
                            if contains_month(str(notice_period)):
                                try:
                                    notice_period_in_month=int(str(notice_period).split()[0])
                                except:
                                    notice_period_in_month=float(str(notice_period).split()[0])
                            elif contains_year(str(notice_period)):
                                try:
                                    notice_period_in_year=int(str(notice_period).split()[0])
                                except:
                                    notice_period_in_year=float(str(notice_period).split()[0])
                            elif contains_days(str(notice_period)):
                                try:
                                    notice_period_in_days=int(str(notice_period).split()[0])
                                except:
                                    notice_period_in_days=float(str(notice_period).split()[0])
                            elif contains_week(str(notice_period)):
                                try:
                                    notice_period_in_week=int(str(notice_period).split()[0])
                                except:
                                    notice_period_in_week=int(str(notice_period).split()[0])

                        having_passport= variables['having_passport']
                        passport_validity= variables['passport_validity']
                        visa= variables['visa']
                        About= variables['About']

                        organization_id=''
                        createdByUserId=''
                        modifiedByUserId=''
                        createdByUserRole=''
                        modifiedByUserRole=''

                        try:
                            organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole=getIdRoleOrganizationIDS(filepath)
                        except Exception as msg:
                            logging.info(f"{msg}")
                            pass

                        if variables:
                            # print(response)
                            df = pd.DataFrame(variables, index=[0])
                            print("df=======>",df)

                        try:
                            cv_url=""
                            # collection = ProfilequeuesCollection()
                            # query = {"file_path": f"{filepath}"}
                            # cv_url = [doc["cv_url"] for doc in collection.find(query)][0]
                            # print("filepath====>:",filepath)
                            # print("cv_url====>:",cv_url)
                        except:
                            pass

                        if email and phone_no:
                            status='Published'
                        else:
                            status='Draft'

                        pinecone_mongo_uuid_val=str(uuid4())
                        print(df)

                        insert_status=insertingIntoMongoDb_xlsx_csv(firstName,lastName,email,phone_no,loc,present_address,
                        DateofBirth,maritial_status,recent_designation,resume_organisation,experience,current_education,
                        qualification,institute,marks_in_percentage,specialization,year_of_passing,resume_skill,
                        secondary_skills,job_title,description,company_name,location,industry,headline,employment_type,
                        date_of_joining,last_date,current_ctc,expected_ctc,current_employment_status,prefered_location,
                        ready_to_relocate,overseas_experience,notice_period,having_passport,passport_validity,visa,About,
                        status,organization_id,createdByUserId,modifiedByUserId,createdByUserRole,modifiedByUserRole,filename,pinecone_mongo_uuid_val,df,filepath,cv_url,
                        notice_period_in_month,notice_period_in_year,notice_period_in_days,notice_period_in_week)
                        
                updateinprofileQueues(filename)
            except Exception as msg:
                s3_client.upload_file(
                filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
                )
                # time.sleep(3)
                logging.info(f"Error: {msg}, Type: {type(msg)} ,{traceback.print_exc()}")
                try:
                    collection,conn=ProfilequeuesCollection()
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
                s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

                # logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
                os.remove(filename)
                pass
        elif filename.endswith(suffix1):#if file name ends with .dox 
            logging.info(f"using docx:{filename}")
            try:
                education_list_append=[]
                job_list_append=[]
                textract_data = textract.process(filename, extension='docx')
                text1 = textract_data.decode("utf-8")
                lines = text1.split('\n')
                total_text_with_info=[]
                total_text=[]
                for ele in enumerate(lines):
                    dict = {}
                    dict['text']=ele[1]
                    dict['line_number']=ele[0]
                    total_text_with_info.append(dict)
                    total_text.append(ele[1])
                total_text=totalTextProcessor(total_text)
            
                extracted_data=insert_into_mongo(filename,total_text_with_info, total_text, education_list_append,job_list_append,filepath)
            except Exception as msg:
                s3_client.upload_file(
                filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
                )
                logging.info(f"Error: {msg}, Type: {type(msg)} ,{traceback.print_exc()}")
                try:
                    collection,conn=ProfilequeuesCollection()
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
                s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

                # logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
                os.remove(filename)
                pass

        elif filename.endswith(suffix3):#if file name ends with .Pdf 
            print("using pdf")
            logging.info(f"using pdf:{filename}")
            try:
                education_list_append=[]
                job_list_append=[]
                try:          
                    with open(filename, "rb") as file:
                        logging.info(f"entered after with")
                        total_text_with_info=[]
                        total_text=[]
                        # Create a PDF object
                        pdf = PyPDF2.PdfReader(file)
                        logging.info(f"entered after PyPDF2")
                        # Get the number of pages in the PDF document
                        num_pages = len(pdf.pages)
                        # Iterate over every page
                        for page in range(num_pages):
                            # Extract the text from the page
                            page_text = pdf.pages[page].extract_text()
                            lines = page_text.split('\n')
                            for ele in enumerate(lines):
                                dict = {}
                                dict['text']=ele[1]
                                dict['line_number']=ele[0]
                                total_text_with_info.append(dict)
                                total_text.append(ele[1])
                            total_text=totalTextProcessorPDF(total_text)
                            print("total_text:",total_text)

                        if total_text==[] or len(total_text)<5:
                            try:
                                total_text_with_info=[]
                                total_text=[]
                                # pad_ocr = []
                                print(f"Processing file: {filename}")
                                # Convert PDF to images
                                PAGES = convert_from_path(filename, dpi=300)

                                # Loop through each page of the PDF
                                for i, img_page in enumerate(PAGES):
                                    print("Page number is ", i + 1)
                                    #print(i)
                                    if i == 0 or i > 0:
                                        cropped_image_np = np.array(img_page)
                                        result = ocr.ocr(cropped_image_np, cls=True)
                                        #print(result)
                                        try:
                                            for line in result:
                                                if line[-1] and line[-1][1] > confidence_threshold:
                                                    total_text.append(line[-1][0])
                                        except:
                                            for line in result[0]:
                                                if line[-1] and line[-1][1] > confidence_threshold:
                                                    total_text.append(line[-1][0])
                                total_text = "\n".join(total_text)

                                # print(total_text)
                            except Exception as msg:
                                s3_client.upload_file(
                                filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
                                )
                                # time.sleep(3)
                                logging.info(f"Error: {msg}, Type: {type(msg)} ,{traceback.print_exc()}")
                                try:
                                    collection,conn=ProfilequeuesCollection()
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
                                s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

                                # logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
                                os.remove(filename)
                                pass
                                    
                except:
                    # if total_text=='' or total_text<100:
                    
                    total_text_with_info=[]
                    total_text=[]
                    # pad_ocr = []
                    print(f"Processing file: {filename}")
                    # Convert PDF to images
                    PAGES = convert_from_path(filename, dpi=300)
                    # print(PAGES)

                    # Loop through each page of the PDF
                    for i, img_page in enumerate(PAGES):
                        print("Page number is ", i + 1)
                        #print(i)
                        if i == 0 or i > 0:
                            cropped_image_np = np.array(img_page)
                            result = ocr.ocr(cropped_image_np, cls=True)
                            #print(result)
                            try:
                                for line in result:
                                    if line[-1] and line[-1][1] > confidence_threshold:
                                        total_text.append(line[-1][0])
                            except:
                                for line in result[0]:
                                    if line[-1] and line[-1][1] > confidence_threshold:
                                        total_text.append(line[-1][0])
                    total_text = "\n".join(total_text)

                    # print(total_text)
                



                extracted_data=insert_into_mongo(filename,total_text_with_info, total_text, education_list_append,job_list_append,filepath)
            except Exception as msg:
                s3_client.upload_file(
                filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
                )
                # time.sleep(3)
                logging.info(f"Error: {msg}, Type: {type(msg)} ,{traceback.print_exc()}")
                try:
                    collection,conn=ProfilequeuesCollection()
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
                s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

                # logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
                os.remove(filename)
                pass

            # os.remove(filename)
        

        else:
            s3_client.upload_file(
            filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
            )
            try:
                collection,conn=ProfilequeuesCollection()
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
            s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

            # logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
            os.remove(filename)
            pass

        return 1
        # return {
        #         'createdAt':datetime.now(tz=timezone.utc),
        #         'updatedAt':datetime.now(tz=timezone.utc),
        #         'firstName': return_non_null_status(extracted_data[0]),
        #         'lastName':return_non_null_status(extracted_data[1]),
        #         'email': return_non_null_status(extracted_data[2]),
        #         'phone_no': return_non_null_status(extracted_data[3]),
        #         'current_location': return_non_null_status(extracted_data[4]),
        #         'present_address': return_non_null_status(extracted_data[5]),
        #         'date_of_birth': return_non_null_status(extracted_data[6]),
        #         'marital_status': extracted_data[7],
        #         'current_designation': return_non_null_status(extracted_data[8]),
        #         'current_company': return_non_null_status(extracted_data[9]),
        #         'experience': return_non_null_status(extracted_data[10]) if return_non_null_status(extracted_data[10]) else 0,
        #         'education': return_non_null_status(extracted_data[11]),
        #         'education_details':[{
        #                                     "qualification":return_non_null_status(extracted_data[12]),
        #                                     "institute":return_non_null_status(extracted_data[13]),
        #                                     "marks_in_percentage":return_non_null_status(extracted_data[14]),
        #                                     "specialization":return_non_null_status(extracted_data[15]),
        #                                     "year_of_passing":return_non_null_status(extracted_data[16])
        #                                     }] ,#[return_non_null_status(extracted_data[13])],
        #         'primary_skill': return_non_null_status(extracted_data[17]),
        #         'secondary_skill': ",".join(return_non_null_status(extracted_data[18])) if return_non_null_status(extracted_data[18]) else ' ',
        #         'experience_details':[
        #                                     {
        #                                         "job_title":return_non_null_status(extracted_data[19]),
        #                                         "description":return_non_null_status(extracted_data[20]),
        #                                         "company_name":return_non_null_status(extracted_data[21]),
        #                                         "location":return_non_null_status(extracted_data[22]),
        #                                         "industry":return_non_null_status(extracted_data[23]),
        #                                         "headline":return_non_null_status(extracted_data[24]),
        #                                         "employment_type":return_non_null_status(extracted_data[25]),
        #                                         "date_of_joining":return_non_null_status(extracted_data[26]),
        #                                         "last_date":return_non_null_status(extracted_data[27])
        #                                     }
        #                                 ] ,#[return_non_null_status(extracted_data[16])],
        #         'status':return_non_null_status(extracted_data[39]),
        #         'uploaded_by':'RECRUITER',
        #         'source':'ML Parse',
        #         'organization':return_non_null_status(extracted_data[40]),
        #         'createdByUserId':return_non_null_status(extracted_data[41]),
        #         'modifiedByUserId':return_non_null_status(extracted_data[42]),
        #         'createdByUserRole':return_non_null_status(extracted_data[43]),
        #         'modifiedByUserRole':return_non_null_status(extracted_data[44]),
        #         'current_ctc':extracted_data[28],
        #         'expected_ctc':extracted_data[29],
        #         'current_employment_status':return_non_null_status(extracted_data[30]),
        #         'industry':return_non_null_status(extracted_data[24]),
        #         'prefered_location':return_non_null_status(extracted_data[31]),
        #         'ready_to_relocate':extracted_data[32],
        #         'overseas_experience':extracted_data[33],
        #         'isActive':'',
        #         'notice_period':return_non_null_status(extracted_data[34]),
        #         'having_passport':extracted_data[35],
        #         'passport_validity':return_non_null_status(extracted_data[36]),
        #         'visa':extracted_data[37],
        #         'About':return_non_null_status(extracted_data[38]),
        #         'is_cv_uploaded':True,
        #                 }
    except Exception as msg:
        logging.info(f"Error: {msg}, Type: {type(msg)} ,{traceback.print_exc()}")
        s3_client.upload_file(
            filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
            )
        try:
            collection,conn=ProfilequeuesCollection()
            # Update the records with the specified criteria
            query = {"isProcessed": False,"file_path":f"{AWS_FILES_FOLDER}/{filename}"}
            update = {"$set": {
                "isProcessed": True,
                "processedDateTime": datetime.now(tz=timezone.utc),
                "isError":True,
                "errorMessage":f"filename extension is not correct format",
                "updatedAt": datetime.now(tz=timezone.utc), 
            }}
            result = collection.update_one(query, update)
        finally:
            conn.close()
        s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

        logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
        try:
            os.remove(filename)
        except:
            pass


def process_file(filepath):
    try:
        # Your existing file processing logic here
        print(filepath)
        time.sleep(2)
        logging.info(f"filename: {filepath}")
        filename = str(filepath).split("/")[-1]
        logging.info(f"filename: {filename}")
        s3_client.download_file(AWS_S3_BUCKET_NAME, filepath, filename)
        time.sleep(3)
        logging.info(f"filename: {filename}")
        start_time = time.time()
        TotalTextWithInfo = textExtractionFromResume(filename, filepath)
        print("Key=", f"{AWS_FILES_FOLDER}/{filename}")
        s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=f"{AWS_FILES_FOLDER}/{filename}")
        try:
            os.remove(filename)
        except:
            pass
        end_time = time.time()
        logging.info(f"Time taken to extract {filename} resume is {(end_time - start_time)}")
    except Exception as msg:
        s3_client.upload_file(
            filename, AWS_S3_BUCKET_NAME, f"{AWS_ERRORS_FOLDER}/{filename}"
        )
        logging.info(f"Error: {msg}, Type: {type(msg)} ,{traceback.print_exc()}")
        try:
            collection,conn = ProfilequeuesCollection()
            query = {"isProcessed": False, "file_path": f"{AWS_FILES_FOLDER}/{filename}"}
            update = {
                "$set": {
                    "isProcessed": True,
                    "processedDateTime": datetime.now(tz=timezone.utc),
                    "isError": True,
                    "errorMessage": f"Error: {msg}, Type: {type(msg)}",
                    "updatedAt": datetime.now(tz=timezone.utc),
                }
            }
            result = collection.update_one(query, update)
        finally:
            conn.close()
        s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=f"{AWS_FILES_FOLDER}/{filename}")
        logging.info(f"status of ProfilequeuesCollection: {result.modified_count}")
        try:
            os.remove(filename)
        except:
            pass

processed_file_paths = set()

def process_files_thread(file_queue):
    while not file_queue.empty():
        filepath = file_queue.get()
        if filepath in processed_file_paths:
            print("Skipping file:", filepath)
            file_queue.task_done()
            continue

        print("Processing file:", filepath)
        try:
            print("Processing file2:", filepath)
            process_file(filepath)
        except:
            pass
        processed_file_paths.add(filepath)
        file_queue.task_done()
        print("Task done")
#threading
def resume_selection():
    try:
        collection,conn = ProfilequeuesCollection()
        query = {"isProcessed": False, "isError": False}
        filepaths = [doc["file_path"] for doc in collection.find(query)]
        # filepaths = ["/home/walkingtree/Downloads/Naukri_VinodPatidar[2y_5m].pdf"]
        print(filepaths)

        num_threads = min(len(filepaths), 1)#8
        file_queue = queue.Queue()

        for filepath in filepaths:
            file_queue.put(filepath)

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=process_files_thread, args=(file_queue,))
            thread.start()
            threads.append(thread)

        file_queue.join()

        for thread in threads:
            thread.join()

        return "Extraction Completed"
    finally:
        conn.close()



# def resume_selection():
#     try:
#         print("entered in to resume_selection")
#         collection=ProfilequeuesCollection()
#         query = {"isProcessed": False, "isError": False}
#         filepaths = [doc["file_path"] for doc in collection.find(query)]

#         for filepath in filepaths:
#             try:
#                 logging.info(f"filename :{filepath}")
#                 filename=str(f"{filepath}").split("/")[-1]
#                 # print("filename:",filename)
#                 logging.info(f"filename :{filename}")
#                 s3_client.download_file(AWS_S3_BUCKET_NAME, f"{filepath}", f"{filename}")
#                 time.sleep(3)
#                 logging.info(f"filename :{filename}")
#                 start_time=time.time()
#                 TotalTextWithInfo=textExtractionFromResume(filename,filepath)
#                 # if TotalTextWithInfo:
#                     # skillfile.insertDetailsBasedOnSkills(TotalTextWithInfo)
#                 print("Key=",f"{AWS_FILES_FOLDER}/{filename}")
#                 s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")
#                 # os.remove(filename)
#                 # end_time=time.time()
#                 # logging.info(f"Time taken to extract  {filename} resume is {(end_time-start_time)}")
#                 # collection=ProfilequeuesCollection()
#                 # Update the records with the specified criteria
#                 # query = {"isProcessed": False,"file_path":f"{AWS_FILES_FOLDER}/{filename}"}
#                 # update = {"$set": {
#                 #     "isProcessed": True,
#                 #     "processedDateTime": datetime.now(tz=timezone.utc),
#                 #     "isError":True,
#                 #     "errorMessage":f"Error: {msg}, Type: {type(msg)}",
#                 #     "updatedAt": datetime.now(tz=timezone.utc), 
#                 # }}
#                 # result = collection.update_one(query, update)

#                 os.remove(filename)
#                 end_time=time.time()
#                 logging.info(f"Time taken to extract  {filename} resume is {(end_time-start_time)}")
#             except Exception as msg:
#                 s3_client.upload_file(
#                 filename,AWS_S3_BUCKET_NAME,f"{AWS_ERRORS_FOLDER}/{filename}"
#                 )
#                 logging.info(f"Error: {msg}, Type: {type(msg)} ,{traceback.print_exc()}")
#                 collection=ProfilequeuesCollection()
#                 # Update the records with the specified criteria
#                 query = {"isProcessed": False,"file_path":f"{AWS_FILES_FOLDER}/{filename}"}
#                 update = {"$set": {
#                     "isProcessed": True,
#                     "processedDateTime": datetime.now(tz=timezone.utc),
#                     "isError":True,
#                     "errorMessage":f"Error: {msg}, Type: {type(msg)}",
#                     "updatedAt": datetime.now(tz=timezone.utc), 
#                 }}
#                 result = collection.update_one(query, update)
#                 s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME,Key=f"{AWS_FILES_FOLDER}/{filename}")

#                 logging.info(f'status of ProfilequeuesCollection:{result.modified_count}')
#                 os.remove(filename)
#                 pass
#     except:
#         pass

#     try:
#         os.remove(filename)
#     except:
#         pass




