from logger import logging
import re
import tiktoken
from connection import PreaparingProfilequeuesCollectionforTraining
import time
# import calendar
# import datetime
# import pandas as pd
# from dateutil.relativedelta import relativedelta
def return_element(data):
    logging.info(f"entered into return_element function")
    val = ''
    if(data):
        val = data[0]
    return val

def totalTextProcessor(total_text):
    logging.info(f"entered into totalTextProcessor function")
    total_text = [text.strip() for text in total_text]
    total_text = list(filter(None, total_text))
    total_text = [text.replace(':', '') for text in total_text]
    total_text = [text.replace('\t', ' ') for text in total_text]
    return total_text

def return_non_null_status(element):
    if(element==[]):
        element_to_return=element
    elif(element):
        element_to_return=element
    elif (element==None):
        element_to_return=' '
    else:
        element_to_return=' '        
    return element_to_return 

def return_non_null_status1(element):
    if(element==[]):
        element_to_return=element
    elif(element):
        element_to_return=element
    elif (element==None):
        element_to_return=' '
    else:
        element_to_return=0       
    return element_to_return 

def return_non_null_status2(element):
    if(element):
        element_to_return=element
    else:
        element_to_return=0       
    return element_to_return 

def totalTextProcessorPDF(total_text):
    logging.info(f"entered into totalTextProcessorPDF function")
    while("" in total_text) :
        total_text.remove("")
    while(" " in total_text) :
        total_text.remove(" ")
    while(': ' in total_text) :
        total_text.remove(': ')
    total_text=[i.replace("\t"," ").replace("\n","") for i in total_text ]
    return total_text

def extract_secondary_skills(text):
    """Extracts the secondary skills from the given text.

    Args:
        text: The text to extract the skills from.

    Returns:
        A list of secondary skills.
    """

    # Updated regular expression pattern
    matches = re.findall(r'\b(?:Trained on|Having knowledge of|having knowledge of|Learned skills|Learned on|Learned)\s+([A-Za-z,]+)\b', text)
    skills = [skill.strip() for match in matches for skill in match.split(",")]
    return ', '.join(skills)

def contains_month(string):
    words_to_check = ["month", "months", "Months", "Month"]

    for word in words_to_check:
        if word.lower() in string.lower():
            return True
    
    return False

def contains_year(string):
    words_to_check = ["year", "years", "Years", "Year"]

    for word in words_to_check:
        if word.lower() in string.lower():
            return True
    
    return False

def contains_days(string):
    words_to_check = ["days", "day", "Days", "Day"]

    for word in words_to_check:
        if word.lower() in string.lower():
            return True
    
    return False

def contains_week(string):
    words_to_check = ["week", "weeks", "Week", "Weeks"]

    for word in words_to_check:
        if word.lower() in string.lower():
            return True
    
    return False

def get_experience(resume_text):
    '''This function is for returning a total year of experience from resume using regular expression'''
    try:
        logging.info(f"entered into get_experience function function")

        result = re.findall(r"([\d*\.?\d+]+)\s+(years?)", str(resume_text), re.IGNORECASE)
        result2 = re.findall(r"([\d*\.?\d+]+)\s+(yrs?)", str(resume_text), re.IGNORECASE)
        result3 = re.findall(r"([\d*\.?\d+]+)\s+(year?)", str(resume_text), re.IGNORECASE)
        result4 = re.findall(r"([\d*\.?\d+]+)\s+(YEAR?)", str(resume_text), re.IGNORECASE)
        if(result):
            experience=result[0][0] + ' '+ result[0][1]
            return experience
        elif(result2):
            experience=result2[0][0] + ' '+ result2[0][1]
            return experience
        elif(result3):
            experience=result3[0][0] + ' '+ result3[0][1]
            return experience
        elif(result4):
            experience=result4[0][0] + ' '+ result4[0][1]
            return experience
        else:
            experience=''
            return experience
        # text = resume_text
        
        # if experience=='':
        #     try:
        #         months = "|".join(calendar.month_abbr[1:] + calendar.month_name[1:])
        #         pattern = fr"(?i)((?:{months}) *\d{{4}}) *(?:-|-) *(present|current|till(?:{months}) *\d{{4}})"
        #         total_experience = None
        #         duration=None
        #         today = datetime.datetime.today() 
        #         if re.findall(pattern, str(text)):
        #             for start, end in re.findall(pattern, str(text)):
        #                 if end.lower() == "present" or end.lower() == "current" or end.lower() == "till":
        #                     today = datetime.datetime.today()
        #                     end = f"{calendar.month_abbr[today.month]} {today.year}"
                        
        #                 end1 = pd.to_datetime(end)
        #                 start1=pd.to_datetime(start)
        #                 duration=relativedelta(end1,start1)

        #                 if total_experience:
        #                     total_experience += duration
        #                 else: 
        #                     total_experience = duration

        #                 logging.info(f"{start1}-{end1} ({duration.years} years, {duration.months} months)")

                
        #             if total_experience:
        #                 if total_experience.years:
        #                     experience=total_experience.years
        #                     return str(experience) +" "+"years"
        #                 else:
        #                     experience=duration.months
        #                     return str(experience) +" " +"months"
                    
                    
        #     except Exception as msg:
        #         logging.info(f"Error: {msg}")
        #         pass
                
        # else:
        #     return experience
    except Exception as msg:
        logging.info(f"Error: {msg}")
        pass


def  num_of_tokens_from_text(text:str,model:str)->int:

    """Return the numbers of tokens in the given text"""

    encoding=tiktoken.encoding_for_model(model_name=model)
    num_tokens=len(encoding.encode(text=text))
    return num_tokens

def insertingIntopreparingData(text,rec,response):
    mycollection,conn = PreaparingProfilequeuesCollectionforTraining()
    # response['text']=text
    try:
        resp={
            'text':text,
            'response':[response],
            'cv_url':rec['cv_url'],    
        }
        mycollection.insert_one(resp)
    except:
        pass
    finally:
        conn.close()

from docx import Document

def extract_text_from_doc(doc_filename):
    # try:
    doc = Document(doc_filename)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text
    # except Exception as e:
    #     print(f"Error occurred while extracting text from {doc_filename}: {e}")
    #     return None




# def updatingIntopreparingData(text,myquery,newvalues,response):
#     mycollection,conn = PreaparingProfilequeuesCollectionforTraining()
#     response["$set"]['text']=text
#     try:
#         resp={
#             'text':text,
#             'response':[response],
#             'cv_url':newvalues['cv_url'],    
#         }
#         mycollection.update_one(resp)
#     except:
#         pass
#     finally:
#         conn.close()


def remove_brackets(strings):
    cleaned_strings = []
    for string in strings:
        cleaned_string = string.replace("[", "").replace("]", "")
        cleaned_strings.append(cleaned_string)
    return cleaned_strings



# text_to_count="""resume_text"""
# print(num_of_tokens_from_text(text_to_count,model='gpt-3.5-turbo'))

# from datetime import datetime
# from dateutil.relativedelta import relativedelta
def change_dict_key(d, old_key, new_key, default_value=None):
    d.setdefault(new_key, d.pop(old_key, default_value))



def extract_phone_number(resume_text):
    '''
    This Function is for extraction of phone numbers from resume using regular expression
    '''
    try:
        # resume_text=" ".join(resume_text1)
        # logging.info(f"entered into extract_phone_number function")
        # text = resume_text
        # numbers = phonenumbers.PhoneNumberMatcher(text, "IN")
        # number1=[]
        # for number in numbers:
        #     number1.append(number)
        #     pattern = r".*linkedin\.com/in/.+-(\d+)\s*\ "
        #     match = re.match(pattern, str(number))
        #     if match:
        #         number = match.group(1)
        #         return ' '
        
        PHONE_REG1 = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
        PHONE_REG2 = re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?')
        phone1 = re.findall(PHONE_REG1, resume_text)
        phone2 = re.findall(PHONE_REG2, resume_text)
        if phone1:
            number = ''.join(phone1[0])
            if resume_text.find(number) >= 0 and len(number) == 10:
                return number
            else:
                return number
        elif phone2:
            number = ''.join(phone2[0])
            if resume_text.find(number) >= 0 and len(number) == 10:
                return number
            else:
                return number
        # elif number1:
        #     number2=number1[0].number.national_number
        #     return number2
        try:
            print("entered into try")
            phone_regex = r'\d{2}-\d{10}|\+\d{2}\d{10}'
            # Find all phone numbers in text using regex
            phone_numbers = re.findall(phone_regex, resume_text)
            if phone_numbers:
                print(phone_numbers)
                return phone_numbers[0]
        except:
            try:
                print("entered into except")
                phone_regex = re.compile(r'(\+?\d{1,2}\s)?(\d{10})')
                match = phone_regex.search(resume_text)
                if match:
                    phone_number = match.group(0)
                    return phone_number
            except:
                return " "
                # if number1:
                #     number2=len(number1[0].number.national_number)==10
                #     return number2
        return " "
    except Exception as msg:
        logging.info(f"Error: {msg}, Type: {type(msg)}")
        pass


from datetime import datetime
current_date = datetime.now().strftime("%Y-%m-%d")
from config import API_KEY
import openai
openai.api_key = API_KEY

from openai import OpenAI
client = OpenAI(api_key=API_KEY)



delimiter = "####"
system_message = f"""
Today's Date: {current_date}
You are an experienced resume attributes extracter. Given the resume delimited by {delimiter}, your goal is to extract the requested attributes.Please extract the following information using the given names ONLY \
make use of your resume parsing expertise:
                   - First Name
                   - Last Name
                   - Email ID
                   - Mobile number
                   - Location:return where he is living else return empty string
                   - Present Address:return Full Address of a Person like with House Number and Pincode e.t.c.. else return empty string
                   - Date of Birth:return date of birth if present else empty string
                   - Marital Status:return whether he is Married or Not Married if present else empty string
                   - Designation:return Latest Designation of a Person else return empty string
                   - Company:return Latest Company name of a Person else return empty string
                   - Experience:return the total years of experience the candidate has since the first job till Today's Date. return just the numerical else return 0
                   - Education:return Highest degree of a person if present else empty string
                   - Qualification:return Highest degree of a person if present else empty string
                   - Education Institute:return the institute/college name where the person studied highest degree if present else empty string
                   - Marks in percentage:return how much percentage person scored in higest degree if present else empty string
                   - Specialization:return specialization in higest degree if present else empty string
                   - Year of passing:return in which year he passed the highest degree if present else empty string
                   - Primary Skills: return ALL the technical skills provided in the content as a list else return empty string. ALWAYS Include all the technical skills from experience section and any section named like "Technical Skills" in the entire given content.Exclude any text that are mentioned inside the Products Specialization and skills that are prefixed with "Trained on", "having knowledge of", or "Learned".
                   - Secondary Skills: Extract skills that are prefixed with "Trained on", "having knowledge of", or "Learned". Exclude any skills that are not prefixed with these phrases. Also exclude any skills that are listed as primary skills, mentioned in the projects or experience sections, or mentioned in any other section. If no matching skills are found, return an empty string.
                   - Job Title:return the title of a job/designation if present else empty string
                   - Job description:return description of the job if present else empty string
                   - Company Location:Latest company location of a person if present else empty string
                   - Industry:return IT or Health or Hardware or Software industry e.t.c... else return empty string
                   - Headline:return Experience Headline of a person if present else empty string
                   - Employment type:return Full Time or Part Time of a person
                   - Date of joining:return joined date of a company if present else empty string
                   - Last date:return last date of a company if present else empty string
                   - Current CTC:return just the numerical of current ctc if present else return 0 if not present 
                   - Expected CTC:return just the numerical of expected ctc if presentelse return 0 if not present
                   - Current Employment Status:return employee status if present else empty string
                   - Prefered Location:return prefered location of a person if present else empty string
                   - Ready to relocate:return True if present else False
                   - Overseas Experience:return True if present else False
                   - Notice Period:Extract the notice period should be a numerical value along with its unit (weeks,months, days, or years)e.g:5 days or 3 months or 2 weeks e.t.c. return 0 if Immediate joining present in the text else return empty string.
                   - Having Passport:return True if present else False
                   - Passport Validity:return the validity of a passport if present else empty string
                   - Visa:return True if present else False
                   - About:Generate a Summary of the profile in 2-3 lines else return empty string if not present
                    """


def small_text(formatted_text):
    # try:
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{formatted_text}{delimiter}"},#formatted_text},
    ],
    temperature=0.0
    # max_tokens=2000,
    # api_key=API_KEY  # Pass the API key here
    )
    #completion = client.completions.create(model="gpt-3.5-turbo", prompt=system_message)
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[f"{delimiter}{formatted_text}{delimiter}"])

    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print(response)
    extracted_info=response.choices[0].message.content.strip()
    print(extracted_info)
    # extracted_info = response['choices'][0]['message']['content'].strip()
    dictionary = {}
    lines = extracted_info.split('\n')
    lines = [s.lstrip( '- ' ) if s.startswith( '-' ) else s for s in lines]
    for line in lines:
        if line.strip():
            key, value = line.split(':')
            dictionary[key.strip()] = value.strip()

    # dictionary = {key.lstrip('- '): value for key, value in dictionary.items()}
    # dictionary = {key.lstrip( '- ' ): value for key, value in dictionary.items() if key.startswith( '- ' )} 
    # dictionary.update({key: value for key, value in dictionary.items() if not key.startswith( '- ' )}) 
    return dictionary
    # except Exception as e:
    #     print(f"Error: {e}")
    #     pass

    # return dictionary

def chunk_text(text, max_chunk_length):
    chunks = []
    current_chunk = ''
    for sentence in text.split('.'):
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_length:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def long_text(formatted_text):
    delimiter = "####"
    text_chunks = chunk_text(formatted_text, max_chunk_length=2000)
    # print(text_chunks)
    params = {
        "First Name": "",
        "Last Name": "",
        "Email ID": "",
        "Mobile number": "",
        "Location": "",
        "Present Address": "",
        "Date of Birth": "",
        "Marital Status": "",
        "Designation": "",
        "Company": "",
        "Experience": "",
        "Education": "",
        "Qualification": "",
        "Education Institute": "",
        "Marks in percentage": "",
        "Specialization": "",
        "Year of passing": "",
        "Primary Skills": "",
        "Secondary Skills": "",
        "Job Title": "",
        "Job description": "",
        "Company Location": "",
        "Industry": "",
        "Headline": "",
        "Employment type": "",
        "Date of joining": "",
        "Last date": "",
        "Current CTC": "",
        "Expected CTC": "",
        "Current Employment Status": "",
        "Prefered Location": "",
        "Ready to relocate": "",
        "Overseas Experience": "",
        "Notice Period": "",
        "Having Passport": "",
        "Passport Validity": "",
        "Visa": "",
        "About": ""
    }
    
    for chunk in text_chunks:
        # try:
    #     response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #     {"role": "system", "content": system_message},
    #     {"role": "user", "content": f"{delimiter}{chunk}{delimiter}"},#formatted_text},
    # ],
    #     temperature=0.0,
    #     max_tokens=2000,
    #     api_key=API_KEY  # Pass the API key here
    #     )
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"{delimiter}{chunk}{delimiter}"},#formatted_text},
        ],
        temperature=0.0
        # max_tokens=2000,
        # api_key=API_KEY  # Pass the API key here
        )

        # extracted_info = response['choices'][0]['message']['content'].strip()
        extracted_info=response.choices[0].message.content.strip()
        print(extracted_info)

        
        lines = extracted_info.split("\n")
        # print("lines====",lines)
        lines = [s.lstrip( '- ' ) if s.startswith( '-' ) else s for s in lines]
        # print("lines1====",lines)
        for line in lines:
            line=line.strip()
            for param in params:
                if line.startswith(param):
                    value = line.split(":")[-1].strip()
                    if not params[param]:
                        params[param] = value
        # except Exception as e:
        #     print(e)
        
    for key, value in params.items():
        if value == 'Not mentioned':
            params[key] = ''
    # print(params)
    # params = {key.lstrip( '- ' ): value for key, value in params.items() if key.startswith( '- ' )} 
    # params.update({key: value for key, value in params.items() if not key.startswith( '- ' )}) 
    # print("params=====",params)
    # print(type(params))
    return params


def extracting_entities_using_gpt(text,filename):
    token_count=num_of_tokens_from_text(text,model='gpt-3.5-turbo')
    logging.info(f"token count: {token_count}")
    if token_count<3000:
        print("entered into ============>if")
        try:
            print("entered into ===========try block inside if")
            time.sleep(1)
            response=small_text(text)
            return response
            # print(response)
        except:
            # try:
            #     print("Exception occurred in small_text method==>try")
            #     time.sleep(1)
            #     logging.info(f'entered into try')
            #     response=text_with_gpt_turbo(text)
            # except:
            time.sleep(2)
            logging.info(f'entered into except')
            try:
                response=long_text(text)
                return response
                # print("response=====",response)
                # print(type(response))
            except:
                logging.info(f"got error for this file  {filename}")
                pass
    else:
        print("entered into ============>else")
        try:
            time.sleep(1)
            response=long_text(text)
            return response
            # print("response=====",response)
            # print(type(response))
            # print(response)
        except:
            # try:
            #     time.sleep(1)
            #     logging.info(f'entered into try')
            #     response=text_with_gpt_turbo(text)
            # except:
            time.sleep(2)
            logging.info(f'entered into except')
            try:
                response=small_text(text)
                return response
            except:
                logging.info(f"got error for this file  {filename}")
                pass

    
def experience_processing(string):
    response = {}
    try:
        years_regex = r"(\d+)\s+(Years|years|year|YEARS)"
        years_match = re.search(years_regex, string)

        if years_match:
            years = int(years_match.group(1))

            # Check if months exist in the string
            if re.search(r"\d+\s+(Months|months|month|MONTH|Month)", string):
                months_regex = r"(\d+)\s+(Months|months|month|MONTH|Month)"
                months_match = re.search(months_regex, string)

                if months_match:
                    months = int(months_match.group(1))
                    experience = str(years) + "." + str(months)
                    response['Experience'] = experience
            else:
                # If there are no months, return just the years
                response['Experience'] = str(years)
        else:
            # if there are no years, return an empty string
            response['Experience'] = ''

    except:
        response['Experience'] = ''
        
    return response['Experience']