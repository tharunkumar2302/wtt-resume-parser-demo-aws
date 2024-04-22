

from groq import Groq
import json
from datetime import datetime
current_date = datetime.now().strftime("%Y-%m-%d")


client = Groq(
    api_key="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",
)

delimiter = "####"
system_message = f"""<s>[INST]
Today's Date: {current_date}
You are a corporate recruitment specialist. Given an input text or query delimited by {delimiter}, please extract the below requested information JSON format.
    Please extract the following information in a consistent format using the given names ONLY:
    - firstName:extract First Name from text if present else return an empty string e.g:""
    - lastName:extract Last Name from text if present else return an empty string  e.g:"" 
    - phone_no:extract Mobile number from text if present else return an empty string  e.g:""
    - current_location: return all locations where person could be living else return an empty list  e.g:[] 
    - primary_skill: return all the skills mentioned else return an empty list  e.g:[]
    - current_company: return all the company name from text else return an empty list e.g:[]
    - current_designation: return all the designation name from text else return an empty list e.g:[]
    - notice_period: return the notice period information from the text if provided, else emty string . Specify whether it's '$lt,' '$gt,' or just a certain number of months ,return in the format to filter in the MongoDB.
    - experience: Extract the years of experience information from the text in json. If the experience is in months, do not return any number. If the experience is specified in years, return the number of years in the format to filter in MongoDB, including whether it is $lt (less than), $gt (greater than), or just a certain number of years.
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
        "experience":'$eq 3' or '$lt 6' or '$gt 8' or 6 or '$eq 10.5' or '$lt 7.5' or '$gt 5.5' or 1.5 ensure in JSON format.e.g:{"gt":4} or {"lt":7.9} or {"eq":6}

    **Please provide only output, no explanation needed.**    

    """



def extract_content(input_string):
    # Find the index of the first '{'
    start_index = input_string.find('{')
    
    # Find the index of the last '}'
    end_index = input_string.rfind('}')
    
    # Extract the content between the first '{' and last '}'
    extracted_content = input_string[start_index:end_index+1]
    print("extracted_content=====",extracted_content)
    print(type(extracted_content))
    
    return extracted_content

# user_message = 
# """
# Job Description

# This is a remote position.

# Data Scientist

# Responsibilities
# • Understand data needs by interfacing with fellow data scientists, data engineers, and business partners
# • Architect, build, and launch efficient & reliable new data models and pipelines in partnership with Data Engineering
# • Design, define, and implement metrics and dimensions to enable analysis and predictive modeling
# • Become a data expert in your business domain and own data quality
# • Build tools for auditing, error logging, and validating data tables
# • Build and improve data tooling in partnership with internal Data Platform teams
# • Define logging needs in partnership with Data Engineering
# • Design and develop dashboards to enable self-serve data consumption

# Minimum Requirements
# • 5+years of relevant industry experience.
# • Bachelors and/or Master's degree in CS/EE, or equivalent experience.
# • Working with data at the petabyte scale.
# • Experience designing and deploying high performance systems with reliable monitoring and logging practices.
# • Effectively work across team boundaries to establish overarching data architecture, and provide guidance to individual teams.
# • Working knowledge of relational databases and query authoring (SQL).
# • Strong programming skills (Python, R preferred).
# • Versatility to communicate clearly with both technical and non-technical audiences.
# • Data analytical and data engineering experience is a plus (HIVE and Spark preferred)
# • Excellent communication skills, both written and verbal
# """

def nlp_using_groq(user_message):
    try:
        messages =  [
                    {'role':'system',
                    'content': system_message},
                    {'role':'user',
                    'content': f"{delimiter}{user_message}{delimiter}" + """\nAdhere to all instructions and extract all attributes accurately providing clean formatting...Thank you.. [/INST]"""},
                    ]

        chat_completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages,
            temperature=0.0,
            max_tokens=None,
            top_p = 1,
            frequency_penalty=0.0            
            )
        response=chat_completion.choices[0].message.content

        if 'Note:' in response:
            response=response[:response.find("Note:")]

        print("The assistant suggests: ", response)
        response=extract_content(response)
        print("response=====>",response)
        # json_dict = json.loads(response)

        # json_string = json.dumps(response)
        json_string = response.replace("\\", "")

        # print("json_string=====>",json_string)

        json_dict = json.loads(json_string)
        print("json_dict=====>",json_dict)
        
        # keys_to_modify = [key for key in json_dict.keys() if "\_" in key]
        # # Iterate over the keys_to_modify list
        # for key in keys_to_modify:
        #     # Replace the underscores in the key with an empty string
        #     new_key = key.replace("\_", "_")
        #     # Update the value in the dictionary with the new key
        #     json_dict[new_key] = json_dict.pop(key)

        # print(json_dict)
        # print(type(json_dict))
        return json_dict
    except Exception as e:
        print(e)
        return None