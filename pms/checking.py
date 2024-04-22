# # # # # # # import openai
# # # # # # # from config import API_KEY
# # # # # # # openai.api_key = API_KEY
# # # # # # # MODEL_NAME = 'gpt-3.5-turbo-16k'
# # # # # # # import json
# # # # # # # from langchain_openai.chat_models import ChatOpenAI
# # # # # # # from langchain.chains import LLMChain
# # # # # # # from langchain.prompts import PromptTemplate
# # # # # # # # from langchain_community.llms import OpenAI
# # # # # # # #######
# # # # # # # # from langchain_openai.llm import ChatOpenAI, LLMChain, PromptTemplate
# # # # # # # # def text_with_gpt_turbo(formatted_text):
# # # # # # # #     openai.api_key = API_KEY
# # # # # # # #     # MODEL_NAME = 
# # # # # # # #     llm = ChatOpenAI(model_name=MODEL_NAME, temperature=0, openai_api_key=openai.api_key)
    
# # # # # # # #     # llm = ChatOpenAI(model_name=MODEL_NAME,openai_api_key=API_KEY)
# # # # # # # #     # Few-shot learning prompt
# # # # # # # #     prompt = """You are a recruitment specialist. Given the following resume, you will extract the requested information in JSON format.
# # # # # # # #     {formatted_text}
# # # # # # # #     Please extract the following information using the given names ONLY:
# # # # # # # #     - First Name
# # # # # # # #     - Last Name
# # # # # # # #     - Email ID
# # # # # # # #     - Mobile number
# # # # # # # #     - Location
# # # # # # # #     - Present Address
# # # # # # # #     - Date of Birth
# # # # # # # #     - Marital Status
# # # # # # # #     - Designation:return Latest Designation of a Person else return empty string
# # # # # # # #     - Company:return Latest Company name of a Person else return empty string
# # # # # # # #     - Experience:return the number of years of Experience the person has else return 0
# # # # # # # #     - Education:return Highest degree of a person if present else empty string
# # # # # # # #     - Qualification:return Highest degree of a person if present else empty string
# # # # # # # #     - Education Institute:return the institute/college name where the person studied highest degree if present else empty string
# # # # # # # #     - Marks in percentage:return how much percentage person scored in higest degree if present else empty string
# # # # # # # #     - Specialization:return specialization in higest degree if present else empty string
# # # # # # # #     - Year of passing:return in which year he passed the highest degree if present else empty string
# # # # # # # #     - Primary Skills: return ALL the technical skills provided in the content as a list else return empty string. ALWAYS Include all the technical skills from experience section and any section named like "Technical Skills" in the entire given content.Exclude any text that are mentioned inside the Products Specialization and skills that are prefixed with "Trained on", "having knowledge of", or "Learned".
# # # # # # # #     - Secondary Skills: Extract skills that are prefixed with "Trained on", "having knowledge of", or "Learned". Exclude any skills that are not prefixed with these phrases. Also exclude any skills that are listed as primary skills, mentioned in the projects or experience sections, or mentioned in any other section. If no matching skills are found, return an empty string.
# # # # # # # #     - Job Title:return the title of a job/designation if present else empty string
# # # # # # # #     - Job description:return description of the job if present else empty string
# # # # # # # #     - Company Location:Latest company location of a person if present else empty string
# # # # # # # #     - Industry:return IT or Health or Hardware or Software industry e.t.c... else return empty string
# # # # # # # #     - Headline:return Experience Headline of a person if present else empty string
# # # # # # # #     - Employment type:return Full Time or Part Time of a person
# # # # # # # #     - Date of joining:return joined date of the last company if present else empty string
# # # # # # # #     - Last date:return last date of a company if present else empty string
# # # # # # # #     - Current CTC:return 0 if not present
# # # # # # # #     - Expected CTC:return 0 if not present
# # # # # # # #     - Current Employment Status:return employee status if present else empty string
# # # # # # # #     - Prefered Location:return prefered location of a person if present else empty string
# # # # # # # #     - Ready to relocate:return True if present else False
# # # # # # # #     - Overseas Experience:return True if present else False
# # # # # # # #     - Notice Period:Extract the notice period should be a numerical value along with its unit (weeks,months, days, or years)e.g:5 days or 3 months or 2 weeks e.t.c. return 0 if Immediate joining present in the text else return empty string.
# # # # # # # #     - Having Passport:return True if present else False
# # # # # # # #     - Passport Validity:return the validity of a passport if present else empty string
# # # # # # # #     - Visa:return True if present else False
# # # # # # # #     - About: Generate a Summary of the profile in 2-3 lines
# # # # # # # #     """
# # # # # # # #     prompt_template = PromptTemplate(input_variables=["formatted_text"], template=prompt)
# # # # # # # #     extract_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="response")
# # # # # # # #     resp = extract_chain.run(formatted_text=formatted_text)
# # # # # # # #     print(resp)
    
# # # # # # # #     # Handle 'Not mentioned' and convert to empty string
# # # # # # # #     data = json.loads(resp)
# # # # # # # #     for key, value in data.items():
# # # # # # # #         if isinstance(value, str) and value == 'Not mentioned':
# # # # # # # #             data[key] = ''
    
# # # # # # # #     print(type(data))
# # # # # # # #     return data

# # # # # # # # def small_text(formatted_text):
# # # # # # # #     response = openai.ChatCompletion.create(
# # # # # # # #     model="gpt-3.5-turbo",
# # # # # # # #     messages=[
# # # # # # # #         {"role": "system", "content": """You are a helpful assistant.I am a model trained by OpenAI and I can extract specific information from text. Given the following resume, I will extract the requested information.Please extract the following information using the given names ONLY:
# # # # # # # #                     First Name
# # # # # # # #                     Last Name
# # # # # # # #                     Email ID
# # # # # # # #                     Mobile number
# # # # # # # #                     Location:return where he is living else return empty string
# # # # # # # #                     Present Address:return Full Address of a Person like with House Number and Pincode e.t.c.. else return empty string
# # # # # # # #                     Date of Birth:return date of birth if present else empty string
# # # # # # # #                     Marital Status:return whether he is Married or Not Married if present else empty string
# # # # # # # #                     Designation:return Latest Designation of a Person else return empty string
# # # # # # # #                     Company:return Latest Company name of a Person else return empty string
# # # # # # # #                     Experience:return the number of years of Experience the person has else return 0
# # # # # # # #                     Education:return Highest degree of a person if present else empty string
# # # # # # # #                     Qualification:return Highest degree of a person if present else empty string
# # # # # # # #                     Education Institute:return the institute/college name where the person studied highest degree if present else empty string
# # # # # # # #                     Marks in percentage:return how much percentage person scored in higest degree if present else empty string
# # # # # # # #                     Specialization:return specialization in higest degree if present else empty string
# # # # # # # #                     Year of passing:return in which year he passed the highest degree if present else empty string
# # # # # # # #                     Primary Skills: return ALL the technical skills provided in the content as a list else return empty string. ALWAYS Include all the technical skills from experience section and any section named like "Technical Skills" in the entire given content.Exclude any text that are mentioned inside the Products Specialization and skills that are prefixed with "Trained on", "having knowledge of", or "Learned".
# # # # # # # #                     Secondary Skills: Extract skills that are prefixed with "Trained on", "having knowledge of", or "Learned". Exclude any skills that are not prefixed with these phrases. Also exclude any skills that are listed as primary skills, mentioned in the projects or experience sections, or mentioned in any other section. If no matching skills are found, return an empty string.
# # # # # # # #                     Job Title:return the title of a job/designation if present else empty string
# # # # # # # #                     Job description:return description of the job if present else empty string
# # # # # # # #                     Company Location:Latest company location of a person if present else empty string
# # # # # # # #                     Industry:return IT or Health or Hardware or Software industry e.t.c... else return empty string
# # # # # # # #                     Headline:return Experience Headline of a person if present else empty string
# # # # # # # #                     Employment type:return Full Time or Part Time of a person
# # # # # # # #                     Date of joining:return joined date of a company if present else empty string
# # # # # # # #                     Last date:return last date of a company if present else empty string
# # # # # # # #                     Current CTC:return 0 if not present
# # # # # # # #                     Expected CTC:return 0 if not present
# # # # # # # #                     Current Employment Status:return employee status if present else empty string
# # # # # # # #                     Prefered Location:return prefered location of a person if present else empty string
# # # # # # # #                     Ready to relocate:return True if present else False
# # # # # # # #                     Overseas Experience:return True if present else False
# # # # # # # #                     Notice Period:Extract the notice period should be a numerical value along with its unit (weeks,months, days, or years)e.g:5 days or 3 months or 2 weeks e.t.c. return 0 if Immediate joining present in the text else return empty string.
# # # # # # # #                     Having Passport:return True if present else False
# # # # # # # #                     Passport Validity:return the validity of a passport if present else empty string
# # # # # # # #                     Visa:return True if present else False
# # # # # # # #                     About:return empty string if not present
# # # # # # # #                     """},
# # # # # # # #         {"role": "user", "content": formatted_text},
# # # # # # # #     ],
# # # # # # # #     temperature=0.3,
# # # # # # # #     # max_tokens=2000,
# # # # # # # #     api_key=API_KEY  # Pass the API key here
# # # # # # # #     )

# # # # # # # #     extracted_info = response['choices'][0]['message']['content'].strip()
# # # # # # # #     dictionary = {}
# # # # # # # #     lines = extracted_info.split('\n')
# # # # # # # #     for line in lines:
# # # # # # # #         if line.strip():
# # # # # # # #             key, value = line.split(':')
# # # # # # # #             dictionary[key.strip()] = value.strip()

# # # # # # # #     return dictionary

# # # # # # # # def chunk_text(text, max_chunk_length):
# # # # # # # #     chunks = []
# # # # # # # #     current_chunk = ''
# # # # # # # #     for sentence in text.split('.'):
# # # # # # # #         if len(current_chunk) + len(sentence) + 1 <= max_chunk_length:
# # # # # # # #             current_chunk += sentence + '. '
# # # # # # # #         else:
# # # # # # # #             chunks.append(current_chunk.strip())
# # # # # # # #             current_chunk = sentence + '. '
# # # # # # # #     if current_chunk:
# # # # # # # #         chunks.append(current_chunk.strip())
# # # # # # # #     return chunks

# # # # # # # def long_text(formatted_text):
# # # # # # #     text_chunks = chunk_text(formatted_text, max_chunk_length=1300)
# # # # # # #     # print(text_chunks)
# # # # # # #     params = {
# # # # # # #         "First Name": "",
# # # # # # #         "Last Name": "",
# # # # # # #         "Email ID": "",
# # # # # # #         "Mobile number": "",
# # # # # # #         "Location": "",
# # # # # # #         "Present Address": "",
# # # # # # #         "Date of Birth": "",
# # # # # # #         "Marital Status": "",
# # # # # # #         "Designation": "",
# # # # # # #         "Company": "",
# # # # # # #         "Experience": "",
# # # # # # #         "Education": "",
# # # # # # #         "Qualification": "",
# # # # # # #         "Education Institute": "",
# # # # # # #         "Marks in percentage": "",
# # # # # # #         "Specialization": "",
# # # # # # #         "Year of passing": "",
# # # # # # #         "Primary Skills": "",
# # # # # # #         "Secondary Skills": "",
# # # # # # #         "Job Title": "",
# # # # # # #         "Job description": "",
# # # # # # #         "Company Location": "",
# # # # # # #         "Industry": "",
# # # # # # #         "Headline": "",
# # # # # # #         "Employment type": "",
# # # # # # #         "Date of joining": "",
# # # # # # #         "Last date": "",
# # # # # # #         "Current CTC": "",
# # # # # # #         "Expected CTC": "",
# # # # # # #         "Current Employment Status": "",
# # # # # # #         "Prefered Location": "",
# # # # # # #         "Ready to relocate": "",
# # # # # # #         "Overseas Experience": "",
# # # # # # #         "Notice Period": "",
# # # # # # #         "Having Passport": "",
# # # # # # #         "Passport Validity": "",
# # # # # # #         "Visa": "",
# # # # # # #         "About": ""
# # # # # # #     }
# # # # # # #     for chunk in text_chunks:
# # # # # # #         response = openai.ChatCompletion.create(
# # # # # # #         model="gpt-3.5-turbo-16k",
# # # # # # #         messages=[
# # # # # # #             {"role": "system", "content": """You are a helpful assistant.I am a model trained by OpenAI and I can extract specific information from text. Given the following resume, I will extract the requested information.Please extract the following information using the given names ONLY:
# # # # # # #                         First Name
# # # # # # #                         Last Name
# # # # # # #                         Email ID
# # # # # # #                         Mobile number
# # # # # # #                         Location:return where he is living else return empty string
# # # # # # #                         Present Address:return Full Address of a Person like with House Number and Pincode e.t.c.. else return empty string
# # # # # # #                         Date of Birth:return date of birth if present else empty string
# # # # # # #                         Marital Status:return whether he is Married or Not Married if present else empty string
# # # # # # #                         Designation:return Latest Designation of a Person else return empty string
# # # # # # #                         Company:return Latest Company name of a Person else return empty string
# # # # # # #                         Experience:return the number of years of Experience the person has else return 0
# # # # # # #                         Education:return Highest degree of a person if present else empty string
# # # # # # #                         Qualification:return Highest degree of a person if present else empty string
# # # # # # #                         Education Institute:return the institute/college name where the person studied highest degree if present else empty string
# # # # # # #                         Marks in percentage:return how much percentage person scored in higest degree if present else empty string
# # # # # # #                         Specialization:return specialization in higest degree if present else empty string
# # # # # # #                         Year of passing:return in which year he passed the highest degree if present else empty string
# # # # # # #                         Primary Skills: return ALL the technical skills provided in the content as a list else return empty string. ALWAYS Include all the technical skills from experience section and any section named like "Technical Skills" in the entire given content.Exclude any text that are mentioned inside the Products Specialization and skills that are prefixed with "Trained on", "having knowledge of", or "Learned".
# # # # # # #                         Secondary Skills: Extract skills that are prefixed with "Trained on", "having knowledge of", or "Learned". Exclude any skills that are not prefixed with these phrases. Also exclude any skills that are listed as primary skills, mentioned in the projects or experience sections, or mentioned in any other section. If no matching skills are found, return an empty string.
# # # # # # #                         Job Title:return the title of a job/designation if present else empty string
# # # # # # #                         Job description:return description of the job if present else empty string
# # # # # # #                         Company Location:Latest company location of a person if present else empty string
# # # # # # #                         Industry:return IT or Health or Hardware or Software industry e.t.c... else return empty string
# # # # # # #                         Headline:return Experience Headline of a person if present else empty string
# # # # # # #                         Employment type:return Full Time or Part Time of a person
# # # # # # #                         Date of joining:return joined date of a company if present else empty string
# # # # # # #                         Last date:return last date of a company if present else empty string
# # # # # # #                         Current CTC:return 0 if not present
# # # # # # #                         Expected CTC:return 0 if not present
# # # # # # #                         Current Employment Status:return employee status if present else empty string
# # # # # # #                         Prefered Location:return prefered location of a person if present else empty string
# # # # # # #                         Ready to relocate:return True if present else False
# # # # # # #                         Overseas Experience:return True if present else False
# # # # # # #                         Notice Period:Extract the notice period should be a numerical value along with its unit (weeks,months, days, or years)e.g:5 days or 3 months or 2 weeks e.t.c. return 0 if Immediate joining present in the text else return empty string.
# # # # # # #                         Having Passport:return True if present else False
# # # # # # #                         Passport Validity:return the validity of a passport if present else empty string
# # # # # # #                         Visa:return True if present else False
# # # # # # #                         About:return empty string if not present
# # # # # # #                         """},
# # # # # # #             {"role": "user", "content": chunk},
# # # # # # #         ],
# # # # # # #         temperature=0.3,
# # # # # # #         max_tokens=2000,
# # # # # # #         api_key=API_KEY  # Pass the API key here
# # # # # # #         )

# # # # # # #         extracted_info = response['choices'][0]['message']['content'].strip()

        
# # # # # # #         lines = extracted_info.split("\n")
# # # # # # #         # print("lines====",lines)
        
# # # # # # #         for line in lines:
# # # # # # #             line=line.strip()
# # # # # # #             for param in params:
# # # # # # #                 if line.startswith(param):
# # # # # # #                     value = line.split(":")[-1].strip()
# # # # # # #                     if not params[param]:
# # # # # # #                         params[param] = value
# # # # # # #     for key, value in params.items():
# # # # # # #         if value == 'Not mentioned':
# # # # # # #             params[key] = ''
# # # # # # #     return params









# # # # # # # text="""EGA.SHASHI KUMAR email egashashikumar@gmail.com phone No 9705326296 CAREER OBJECTIVE To work for an organization, where I can utilise and improve my skills and knowledge for the growth of the company as well as myself to get prompted to the higher position. EDUCATIONAL QUALIFICATION QUALIFICATION BOARD/UNIVERSITY INSTITUTION AGGREGATE B.tech (electronics and communication engineering) JNTUH Sri indu college of engineering & technology 7.5(CGPA) Intermediate (M.P.C) Telangana state board of intermediate education Shivani junior college 91.6% SSC Board of secondary education Baby sainik high school 9.5(GPA) PROJECTS Sun tracking solar panel By using embedded c programming with the help of micro controller and LDR. Real time solar tracking system By using arduino  and LDR’s rotating of solar tracking system is performed. TECHNICAL SKILLS Programming language            c and python,html,css. Operating system worked on  windows xp/7/8/10 Tools             Microsoft office CO-CURRICULAR ACTIVITIES Participated in swatch barath  at our home town Participated in robotics workshop conducted in our college ACHIEVEMENTS Won participation certificate in JV Rao talent search examination Won first prize in traffic rules exam Won first prize in chess every time in my school STRENGTHS Learning from failure Positive thinking Self motivator Confident LANGUAGES KNOWN English Telugu Hindi HOBBIES Playing chess Making  videos to upload in  YouTube DECLARATION I hereby declare that the above written particulars are true to the best of my knowledge. PLACEHYDERBAD DATE"""
# # # # # # # response=text_with_gpt_turbo(text)
# # # # # # # # response=long_text(text)

# # # # # # # print(response)




# # # # # # # # # #http://0.0.0.0:5000/job_opening?current_location=Delhi&organization_id=64e87ca35c8c0229aeacc266&primary_skill=Python,Machine Learning,Nodejs&education=MBA&min_experience=1&max_experience=10&notice_period=1.5&status=Published&industry=IT   
# # # # # # # # @app.route('/job_opening', methods=['GET'])
# # # # # # # # def job_opening():
# # # # # # # #     try:
# # # # # # # #         logging.info("Entered into job_opening")

# # # # # # # #         if request.method == 'GET':
# # # # # # # #             try:
# # # # # # # #                 print("try")
# # # # # # # #                 current_location = request.args.getlist('current_location', []) 
# # # # # # # #             except:
# # # # # # # #                 print("except")
# # # # # # # #                 current_location = request.args.get('current_location',[]) 

# # # # # # # #             organization_id = request.args.get('organization_id', "")
# # # # # # # #             try:
# # # # # # # #                 print("try")
# # # # # # # #                 primary_skill = request.args.getlist('primary_skill', [])
# # # # # # # #             except:
# # # # # # # #                 print("except")
# # # # # # # #                 primary_skill = request.args.get('primary_skill', [])
# # # # # # # #             education = request.args.get('education', "")
# # # # # # # #             min_experience = request.args.get('min_experience', "")
# # # # # # # #             max_experience = request.args.get('max_experience', "")
# # # # # # # #             notice_period = request.args.get('notice_period', "")
# # # # # # # #             status = request.args.get('status', "")
# # # # # # # #             industry = request.args.get('industry', "")
# # # # # # # #             print("current_location:",current_location)
# # # # # # # #             print(type(current_location))
# # # # # # # #             print("organization_id:",organization_id)
# # # # # # # #             print("primary_skill:",primary_skill)
# # # # # # # #             print("education:",education)
# # # # # # # #             print("min_experience:",min_experience)
# # # # # # # #             print("max_experience:",max_experience)
# # # # # # # #             print("notice_period:",notice_period)
# # # # # # # #             print("status:",status)
# # # # # # # #             print("industry:",industry)
# # # # # # # #             # current_location=list(current_location)
# # # # # # # #             # primary_skill=list(primary_skill)
# # # # # # # #             # Correct the code to remove extra spaces from the list
# # # # # # # #             # current_location = list(map(str.strip, current_location.split(',')))
# # # # # # # #             # primary_skill = list(map(str.strip, primary_skill.split(',')))
# # # # # # # #             print(type(current_location))
# # # # # # # #             print(type(primary_skill))
            

# # # # # # # #             keyword_query = []
# # # # # # # #             res = {}

# # # # # # # #             if current_location:
# # # # # # # #                 print(current_location)
# # # # # # # #                 print(len(current_location))
# # # # # # # #                 curr_location=current_location.split(",")
# # # # # # # #                 print(curr_location)
# # # # # # # #                 print(len(curr_location))
# # # # # # # #                 print(type(curr_location))
# # # # # # # #                 if len(curr_location)>1:
# # # # # # # #                     location_queries = [{"current_location": {"$regex": location, "$options": "i"}} for location in curr_location]
# # # # # # # #                     keyword_query.extend(location_queries)
# # # # # # # #                 else:
# # # # # # # #                     location_queries = {"current_location": {"$regex": current_location, "$options": "i"}}
# # # # # # # #                     keyword_query.append(location_queries)
              
# # # # # # # #             if primary_skill:
# # # # # # # #                 primary_skill_list=primary_skill.split(",")
# # # # # # # #                 print(primary_skill_list)
# # # # # # # #                 print(type(primary_skill_list))
# # # # # # # #                 if len(primary_skill_list)>1:
# # # # # # # #                     skill_queries = [{"primary_skill": {"$regex": skill, "$options": "i"}} for skill in primary_skill_list]
# # # # # # # #                     keyword_query.extend(skill_queries)
# # # # # # # #                 else:
# # # # # # # #                     skill_queries = {"primary_skill": {"$regex": primary_skill, "$options": "i"}}
# # # # # # # #                     keyword_query.append(skill_queries)
                
               

# # # # # # # #                 # skill_queries = [{"primary_skill": {"$regex": skill, "$options": "i"}} for skill in primary_skill[0].split(",")]
# # # # # # # #                 # keyword_query.extend(skill_queries)
# # # # # # # #             if organization_id:
# # # # # # # #                 res["organization"] = ObjectId(organization_id)
# # # # # # # #             if education:
# # # # # # # #                 keyword_query.append({"education": {"$regex": education, "$options": "i"}})
# # # # # # # #             if status:
# # # # # # # #                 keyword_query.append({"status": {"$regex": status, "$options": "i"}})
# # # # # # # #             if industry:
# # # # # # # #                 keyword_query.append({"industry": {"$regex": industry, "$options": "i"}})

# # # # # # # #             if min_experience or max_experience:
# # # # # # # #                 res["experience"]={"$gte": min_experience, "$lte": max_experience}

# # # # # # # #             if notice_period:
# # # # # # # #                 value = str(notice_period).split()[0]
# # # # # # # #                 keyword_query.append({"notice_period": {"$regex": value, "$options": "i"}})


# # # # # # # #             res["$and"] = keyword_query
# # # # # # # #             print("res :",res)

# # # # # # # #             mycollection = resumeDetailsCollection()
# # # # # # # #             obj=mycollection.find(res)
# # # # # # # #             records=[]
# # # # # # # #             for record in obj:
# # # # # # # #                 records.append(record)
# # # # # # # #             if records:
# # # # # # # #                 records=records[:10]

# # # # # # # #             exact_match = []
# # # # # # # #             for resp in range(len(records)):
# # # # # # # #                 print("resp:",resp)
# # # # # # # #                 # new_response["response"]["results"][0]["matches"]
# # # # # # # #                 exact_match.append(transform_response(records[resp]))

# # # # # # # #             results_dict = {'results': [{'matches': exact_match}]}
# # # # # # # #             results_dict = {'response': results_dict}

# # # # # # # #             json_data = json.dumps(results_dict, cls=CustomJSONEncoder)

            
# # # # # # # #             json_data = json.loads(json_data)
# # # # # # # #             logging.info(f"data: {json_data}")

# # # # # # # #             print("in if condition")
# # # # # # # #             logging.info("in if condition")
# # # # # # # #             # return jsonify(json_data)
# # # # # # # #             print(json_data)
# # # # # # # #             # if results_dict['response']['results'][0]['matches']:
# # # # # # # #             #     print("inside if condition")
# # # # # # # #             return jsonify(json_data)

           

# # # # # # # #     except Exception as e:
# # # # # # # #         print("error:",e)
# # # # # # # #         logging.info("error:",e)


# # # # # # from flask import Flask, jsonify, request,make_response
# # # # # # import pinecone
# # # # # # import openai
# # # # # # # from openai.embeddings_utils import get_embedding
# # # # # # # import jsonpickle
# # # # # # from main import ResumeParser,resume_parser
# # # # # # from flask_cors import CORS
# # # # # # from connection import s3_client,resumeDetailsCollection
# # # # # # from config import AWS_S3_BUCKET_NAME,API_KEY,PINECONE_API_KEY,PINECONE_ENVIRONMENT,EMBEDDING_MODEL,PINECONE_INDEX_NAME
# # # # # # import os
# # # # # # from logger import logging
# # # # # # import json
# # # # # # # from langchain.chat_models import ChatOpenAI
# # # # # # # from langchain_community.chat_models import ChatOpenAI
# # # # # # from langchain_openai import ChatOpenAI
# # # # # # from langchain.chains import LLMChain
# # # # # # from langchain.prompts import PromptTemplate
# # # # # # import re
# # # # # # from bson import ObjectId,Decimal128
# # # # # # from utils import contains_days, contains_month, contains_year, contains_week
# # # # # # from openai import OpenAI
# # # # # # client = OpenAI(api_key=API_KEY)

# # # # # # openai.api_key=API_KEY#'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'
# # # # # # pinecone_api_key = PINECONE_API_KEY#"ad5d67cd-e301-407a-a5f8-f276846d7154"#"c9b87bce-2944-4e8a-bd47-58b730f1063e"
# # # # # # environment = PINECONE_ENVIRONMENT#"us-west4-gcp-free"#"us-west1-gcp-free"
# # # # # # index_name = PINECONE_INDEX_NAME
# # # # # # embedding_model = EMBEDDING_MODEL#"text-embedding-ada-002"

# # # # # # MODEL_NAME="gpt-3.5-turbo"

# # # # # # import json
# # # # # # from bson import ObjectId
# # # # # # from datetime import datetime



# # # # # # class CustomJSONEncoder(json.JSONEncoder):
# # # # # #     def default(self, obj):
# # # # # #         if isinstance(obj, ObjectId):
# # # # # #             return str(obj)  # Convert ObjectId to its string representation
# # # # # #         if isinstance(obj, datetime):
# # # # # #             return obj.isoformat()  # Convert datetime to ISO format
# # # # # #         if isinstance(obj, Decimal128):
# # # # # #             return float(str(obj))
# # # # # #         return super().default(obj)










# # # # # # # try:
# # # # # # # from flask import Flask, jsonify, request,make_response
# # # # # # import json
# # # # # # from connection import s3_client,resumeDetailsCollection

# # # # # # from config import (AWS_SERVICE,AWS_REGION_NAME,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,
# # # # # #                    AWS_S3_BUCKET_NAME,MONGODB_HOST,MONGODB_PORT,MONGODB_DATABASE_NAME,
# # # # # #                    MONGODB_RESUME_DETAILS_COLLECTION_NAME,MONGODB_USER_DETAILS_COLLECTION_NAME,
# # # # # #                    MONGODB_FILTER_WITH_SKILL_COLLECTION_NAME,MONGODB_FEEDBACK_DETAIL_COLLECTION_NAME,
# # # # # #                    MONGODB_FEEDBACK_PROFILEQUEUES_COLLECTION_NAME)#,POSTGRES_HOST,POSTGRES_PORT,
# # # # # #                 #    POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_DATABASE)

# # # # # # import ftplib
# # # # # # from pymongo import MongoClient
# # # # # # import boto3
# # # # # # # import psycopg2

# # # # # # #connecting to MongoDB
# # # # # # def resumeDetailsCollection1():
# # # # # #     conn = MongoClient(str(f"{MONGODB_HOST}"), int(MONGODB_PORT))
# # # # # #     database = conn[f"{MONGODB_DATABASE_NAME}"]
# # # # # #     resume_details_collection = database[f"{MONGODB_RESUME_DETAILS_COLLECTION_NAME}"]
# # # # # #     return resume_details_collection

# # # # # # mycollection = resumeDetailsCollection1()
# # # # # # # res = {'primary_skill': {'$regex': 'Data Science', '$options': 'i'}, 'organization': ObjectId('64941732373c2e0420ae407a')}
# # # # # # obj=mycollection.find({'$or': [{'primary_skill': {'$regex': 'Data Science', '$options': 'i'}}], 'organization': ObjectId('64e87ca35c8c0229aeacc266')})
# # # # # # print(obj)
# # # # # # records=[]
# # # # # # for record in obj:
# # # # # #     records.append(record)
# # # # # # if records:
# # # # # #     records=records[:10]
# # # # # # print(records)














# # # # # # # exact_match = []
# # # # # # # for resp in range(len(records)):
# # # # # # #     print("resp:",resp)
# # # # # # #     # new_response["response"]["results"][0]["matches"]
# # # # # # #     exact_match.append(transform_response(records[resp]))

# # # # # # # results_dict = {'results': [{'matches': exact_match}]}
# # # # # # # results_dict = {'response': results_dict}

# # # # # # # json_data = json.dumps(results_dict, cls=CustomJSONEncoder)


# # # # # # # json_data = json.loads(json_data)
# # # # # # # # logging.info(f"data: {json_data}")

# # # # # # # print("in if condition")
# # # # # # # # logging.info("in if condition")
# # # # # # # # return jsonify(json_data)
# # # # # # # print(json_data)
# # # # # # # if results_dict['response']['results'][0]['matches']:
# # # # # # #     print("inside if condition")
# # # # # # #     print(jsonify(json_data))
# # # # # # # # else:
# # # # # # # #     print("inside else condition")
# # # # # # # #     response=key_word_search_with_len(query,phone_no,experience,organization_id,notice_period)
# # # # # # # #     print(response)
# # # # # # # #     print(jsonify(response))
# # # # # # # # finally:
# # # # # # # #     conn.close()



# # # # # # def estimate_tokens(text,method="max"):
# # # # # #     word_count = text.split(" ").count
# # # # # #     char_count = text.length
# # # # # #     tokens_count_word_est = word_count.to_f / 0.75
# # # # # #     tokens_count_char_est = char_count.to_f / 4.0
# # # # # #     output = 0
   
# # # # # #     if method == 'max':
# # # # # #         output = [tokens_count_word_est,tokens_count_char_est].max
   
# # # # # #     return  output

# # # # # # text=""" EGA.SHASHI KUMAR email egashashikumar@gmail.com phone No 9705326296 CAREER OBJECTIVE To work for an organization, where I can utilise and improve my skills and knowledge for the growth of the company as well as myself to get prompted to the higher position. EDUCATIONAL QUALIFICATION QUALIFICATION BOARD/UNIVERSITY INSTITUTION AGGREGATE B.tech (electronics and communication engineering) JNTUH Sri indu college of engineering & technology 7.5(CGPA) Intermediate (M.P.C) Telangana state board of intermediate education Shivani junior college 91.6% SSC Board of secondary education Baby sainik high school 9.5(GPA) PROJECTS Sun tracking solar panel By using embedded c programming with the help of micro controller and LDR. Real time solar tracking system By using arduino  and LDR’s rotating of solar tracking system is performed. TECHNICAL SKILLS Programming language            c and python,html,css. Operating system worked on  windows xp/7/8/10 Tools             Microsoft office CO-CURRICULAR ACTIVITIES Participated in swatch barath  at our home town Participated in robotics workshop conducted in our college ACHIEVEMENTS Won participation certificate in JV Rao talent search examination Won first prize in traffic rules exam Won first prize in chess every time in my school STRENGTHS Learning from failure Positive thinking Self motivator Confident LANGUAGES KNOWN English Telugu Hindi HOBBIES Playing chess Making  videos to upload in  YouTube DECLARATION I hereby declare that the above written particulars are true to the best of my knowledge. PLACEHYDERBAD DATE """
# # # # # # print(estimate_tokens(text,method="max"))

# # # # # # from openai import Tiktoken
# # # # # # API_KEY = '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'#'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'#'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'#'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'#'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'#'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'

# # # # # # def get_token_length(text):
# # # # # #     # Initialize Tiktoken with your OpenAI API key
# # # # # #     tiktoken = Tiktoken(api_key=API_KEY)

# # # # # #     # Get the token count for the given text
# # # # # #     token_count = tiktoken.count(text)

# # # # # #     return token_count

# # # # # # # Example usage
# # # # # # # text_to_count = "Your text goes here."
# # # # # # text_to_count=""" EGA.SHASHI KUMAR email egashashikumar@gmail.com phone No 9705326296 CAREER OBJECTIVE To work for an organization, where I can utilise and improve my skills and knowledge for the growth of the company as well as myself to get prompted to the higher position. EDUCATIONAL QUALIFICATION QUALIFICATION BOARD/UNIVERSITY INSTITUTION AGGREGATE B.tech (electronics and communication engineering) JNTUH Sri indu college of engineering & technology 7.5(CGPA) Intermediate (M.P.C) Telangana state board of intermediate education Shivani junior college 91.6% SSC Board of secondary education Baby sainik high school 9.5(GPA) PROJECTS Sun tracking solar panel By using embedded c programming with the help of micro controller and LDR. Real time solar tracking system By using arduino  and LDR’s rotating of solar tracking system is performed. TECHNICAL SKILLS Programming language            c and python,html,css. Operating system worked on  windows xp/7/8/10 Tools             Microsoft office CO-CURRICULAR ACTIVITIES Participated in swatch barath  at our home town Participated in robotics workshop conducted in our college ACHIEVEMENTS Won participation certificate in JV Rao talent search examination Won first prize in traffic rules exam Won first prize in chess every time in my school STRENGTHS Learning from failure Positive thinking Self motivator Confident LANGUAGES KNOWN English Telugu Hindi HOBBIES Playing chess Making  videos to upload in  YouTube DECLARATION I hereby declare that the above written particulars are true to the best of my knowledge. PLACEHYDERBAD DATE """

# # # # # # # Replace "YOUR_API_KEY" with your actual OpenAI API key
# # # # # # token_length = get_token_length(text_to_count)

# # # # # # print(f"The token length of the text is: {token_length}")



# # # # # # from tiktoken import count_tokens

# # # # # # def get_token_length(text):
# # # # # #     # Get the token count for the given text
# # # # # #     token_count = count_tokens(text)

# # # # # #     return token_count

# # # # # # # Example usage
# # # # # # # text_to_count = "Your text goes here."
# # # # # # text_to_count=""" EGA.SHASHI KUMAR email egashashikumar@gmail.com phone No 9705326296 CAREER OBJECTIVE To work for an organization, where I can utilise and improve my skills and knowledge for the growth of the company as well as myself to get prompted to the higher position. EDUCATIONAL QUALIFICATION QUALIFICATION BOARD/UNIVERSITY INSTITUTION AGGREGATE B.tech (electronics and communication engineering) JNTUH Sri indu college of engineering & technology 7.5(CGPA) Intermediate (M.P.C) Telangana state board of intermediate education Shivani junior college 91.6% SSC Board of secondary education Baby sainik high school 9.5(GPA) PROJECTS Sun tracking solar panel By using embedded c programming with the help of micro controller and LDR. Real time solar tracking system By using arduino  and LDR’s rotating of solar tracking system is performed. TECHNICAL SKILLS Programming language            c and python,html,css. Operating system worked on  windows xp/7/8/10 Tools             Microsoft office CO-CURRICULAR ACTIVITIES Participated in swatch barath  at our home town Participated in robotics workshop conducted in our college ACHIEVEMENTS Won participation certificate in JV Rao talent search examination Won first prize in traffic rules exam Won first prize in chess every time in my school STRENGTHS Learning from failure Positive thinking Self motivator Confident LANGUAGES KNOWN English Telugu Hindi HOBBIES Playing chess Making  videos to upload in  YouTube DECLARATION I hereby declare that the above written particulars are true to the best of my knowledge. PLACEHYDERBAD DATE """

# # # # # # # Call the function to get the token length
# # # # # # token_length = get_token_length(text_to_count)

# # # # # # print(f"The token length of the text is: {token_length}")

# # # # # # from tiktoken import TokenCounter

# # # # # # def get_token_length(text):
# # # # # #     # Initialize TokenCounter
# # # # # #     token_counter = TokenCounter()

# # # # # #     # Update the counter with the text
# # # # # #     token_counter.update(text)

# # # # # #     # Get the token count
# # # # # #     token_count = token_counter.finalize()

# # # # # #     return token_count

# # # # # # # Example usage
# # # # # # # text_to_count = "Your text goes here."
# # # # # # text_to_count=""" EGA.SHASHI KUMAR email egashashikumar@gmail.com phone No 9705326296 CAREER OBJECTIVE To work for an organization, where I can utilise and improve my skills and knowledge for the growth of the company as well as myself to get prompted to the higher position. EDUCATIONAL QUALIFICATION QUALIFICATION BOARD/UNIVERSITY INSTITUTION AGGREGATE B.tech (electronics and communication engineering) JNTUH Sri indu college of engineering & technology 7.5(CGPA) Intermediate (M.P.C) Telangana state board of intermediate education Shivani junior college 91.6% SSC Board of secondary education Baby sainik high school 9.5(GPA) PROJECTS Sun tracking solar panel By using embedded c programming with the help of micro controller and LDR. Real time solar tracking system By using arduino  and LDR’s rotating of solar tracking system is performed. TECHNICAL SKILLS Programming language            c and python,html,css. Operating system worked on  windows xp/7/8/10 Tools             Microsoft office CO-CURRICULAR ACTIVITIES Participated in swatch barath  at our home town Participated in robotics workshop conducted in our college ACHIEVEMENTS Won participation certificate in JV Rao talent search examination Won first prize in traffic rules exam Won first prize in chess every time in my school STRENGTHS Learning from failure Positive thinking Self motivator Confident LANGUAGES KNOWN English Telugu Hindi HOBBIES Playing chess Making  videos to upload in  YouTube DECLARATION I hereby declare that the above written particulars are true to the best of my knowledge. PLACEHYDERBAD DATE """

# # # # # # # Call the function to get the token length
# # # # # # token_length = get_token_length(text_to_count)

# # # # # # print(f"The token length of the text is: {token_length}")

# # # # # # import tiktoken

# # # # # # def  num_of_tokens_from_text(text:str,model:str)->int:

# # # # # #     """Return the numbers of tokens in the given text"""

# # # # # #     encoding=tiktoken.encoding_for_model(model_name=model)
# # # # # #     num_tokens=len(encoding.encode(text=text))
# # # # # #     return num_tokens
# # # # # # # text_to_count="""resume_text"""
# # # # # # # print(num_of_tokens_from_text(text_to_count,model='gpt-3.5-turbo'))
# # # # # # # text_to_count="""Majji Naveen Kumar Mobile+917028569059                                                                             Emailnaveenmajjimca@gmail.com Professional Summary - Having 14 years of experience in Middleware Administration and Lead for Middleware Technologies like IBM MQ, IBM WAS 6.x,7.x, 8.x, WebLogic 11.x, 12.x, Apache, IHS, Tomcat. Setting up the end-to-end environment from load balancer to application configuring automation system for configuration management. Strong management and administration skills in providing installation, configuration, troubleshooting, backup and recovery in multiple Application and Web Servers highlighting IBM WAS, Oracle WebLogic, IBM WASCE and IBM IHS, Apache, tomcat. Configured Web Sphere resources like JDBC providers, JDBC data sources. Experience in installing, configuring the IBM IHS server and plug-ins. Handling automation issues while application releases in DevOps tools. Deployed applications (WAR and EAR) in various environments like Development and Production on Web Sphere Application Server using automation process. Creation and management of data source and database connection pools. Configured WebSphere global security with LDAP registry. Created users with various roles to access the WebSphere admin console. Experienced in performance tuning by Web Sphere configuration parameters like JVM heap size, web container thread, DB connection pooling etc. Experience in Troubleshooting the WAS by using Logs and Log Analyzer. Experienced in installing and upgrading Fix packs. Experience in Dev/Stage/Prod/DR support and troubleshooting problems related to Web Servers, Web Sphere Application Servers, WebLogic Servers, WebSphere Plug-ins, and Database. Involved in implementing Setups and Decoms with proper RFC in a particular period. Preparing RCA documents for Production issues which are caused to business impact. Creating, enabling and disabling the AppDynamics monitors for app url’s. Handling the high, critical priority issues over the bridge calls and checking logs, end to end configurations. Responsible Production and non-prod environment support, handling critical priority Technical Skills Automation Tools        Ansible and Jenkins. Application Servers  IBM Web Sphere App Server, WebLogic and Tomcat. Messaging   IBM MQ Operating Systems  UNIX, Linux, AIX, Solaris and Windows. Web server   IHS 6.x,7.x,8.x Apache. Database   DB2, ORACLE Tool                                 Service Now, BMC Remedy. Scripts                             Shell Career Profile Working Associate Consultant for HCL from June 2023 to Till Date Worked as customer success manager for Cloudmoyo India Pvt Ltd from Aug 2022 to 31st March2023. Worked as Sr Team Lead for Birlasoft from April 2019 to Aug 2022. Worked Operations Manager for Tech Mahindra from Feb 2009 to March 2019. Worked Software Engineer for Maintech from Oct 2008 to Feb 2009. Education Master of Computer Applications from Bangalore University. Certifications IBM WebSphere Application Server Core Administration 6.1,8.0 Professional Experience Project 1 Current Project Daimler Duration Aug’2022 – 31st March 2023 Responsibilities Responsible for Production and non-prod environment build and configuration for WAS 8.x, Weblogic 12.x, IHS, Tomcat, Apache and IIS Discussing with the client and verifying the architecture diagram and its requirements Understanding the requirements and requesting the virtual machines with Linux or windows team based on requirement. Requesting LB team to create vips and asking virtual machines to add respective vips Requesting Linux or Windows team for respective disk space and memory Gathering virtual machine names and its IP address for respective applications Downloading and installing respective bundles from the respective sites in the virtual machines Requesting network team to open the respective ports Configuring the integration between webserver, application server and database Coordinating with the application team to install the application and its database configuration Coordinating with database team for database configuration Creating CSR and certificates for respective URL's and importing in the respective servers Verifying the applications using http/https and confirming with the customer Hand overing the applications and its servers to the admin team for operational support Skills IBM WAS 8.x, Tomcat, Apache, IHS webserver, IIS and MQ Project 2 Project HomeserveUSA Duration Apr’2019 – Aug’2022 Responsibilities Responsible Production and non-prod environment support, handling critical priority Incidents and implementing changes in scheduled window. Configured JDBC Drivers and data source connection pools on WebSphere application server to connect the J2EE components with oracle and DB2 databases. Supported WebSphere Application Server clustering, load balance, failover/recovery and performance tuning. Ensuring consistent communication between Websphere Clients, Edge Components, Web Server, Application Server(s), and Database. Configured and Enabled the Global Security System for Web Sphere Admin Console Using LDAP User Registry. Deployed applications (WAR and EAR) on Web Sphere using Chef and Jenkins (CICD). Involved in securing the J2EE applications by implementing Self Signed certificates. Tuned the Application server parameters like connection pool, web container thread pool and session management and heap size. Involved in taking Backup and Recovery of Web Sphere repository configurations by using BackupConfig and restoreConfig commands. Handling the high, critical priority issues over the bridge calls and checking logs, end to end configurations. Configuring WebSphere Application Server on multiple platforms for both horizontal and vertical scaling for Work Load Management. Involved SSL certificates renewal activities for web and application servers Handling daily call with the client for daily status reports and process improvements Skills IBM WAS 8.x, Oracle Weblogic 11g, 12c, IHS and SOWS webserver, Project 3 Project IKEA Duration May’2016 – Mar'2019 Responsibilities Responsible Production and non-prod environment support, handling critical priority Incidents and implementing changes in scheduled window. Supporting for Oracle apps like OSB, SOA and BAM Integrations with WebLogic in Prod and Non-Prod environments Creating data source and connection pools using WebLogic console. Worked on EM console for composite and security key operations Installing certificates for public and private keys in WebLogic servers. Involved in build and decommission process. Involved daily scrum call for updating jira task to update progress of the assigned activities. Involved in troubleshooting of critical incidents which are impacting the integrations. Preparing the report for consumption of parameters like CPU, Memory and etc, using OEM tools. Supporting for deployment release activities if any changes or issue while deployment. Skills WebLogic 11g, 12c, Splunk tools, AppDynamics Tool, Jira Digital, Idesk, Ansible. Project 4 Project MOS2-MQ Duration Aug’2008 – May'2016 Responsibilities Running the work request regarding the Queue component creation. Installation/De-installation of IBM MQ Software on the requested servers. Installation/De-installation of Queue Manager on the requested servers. Configured application specific MQ Series Objects such as Queue managers, Queues and channels. Installed the MQ Series iFix packs on Unix Sand boxes. Handling Shell & SQL Scripting Production support (Automation & Enhancements in various report generation) The Midrange Application Support Enterprise Team Efficiently provide Tier II operational for AT&T billing on midrange platform systems Provide Tire II Technical support coverage Problem Management – resolution and documentation Change Management – Plan and implement changes in coordination with internal and external teams Manage midrange application related projects from inception through implementation in conjunction with internal and external teams Proactive monitoring of application and batch performance and processes Install, configure, administer and support middleware software Providing technical support/debugging of live issues Handling daily call with the client for daily status reports and process improvements Personal Details Name   Naveen Kumar Majji Gender  Male Mobile No  7028569059
# # # # # # # [ 2024-01-03 21:37:54,497 ] 1099 root - INFO - filename: Naukri_AartiKanodia[6y_6m]_1703584223887.docx"""

# # # # # # text_to_count="""You are a helpful assistant.I am a model trained by OpenAI and I can extract specific information from text. Given the following resume, I will extract the requested information.Please extract the following information using the given names ONLY:
# # # # # #                         First Name
# # # # # #                         Last Name
# # # # # #                         Email ID
# # # # # #                         Mobile number
# # # # # #                         Location:return where he is living else return empty string
# # # # # #                         Present Address:return Full Address of a Person like with House Number and Pincode e.t.c.. else return empty string
# # # # # #                         Date of Birth:return date of birth if present else empty string
# # # # # #                         Marital Status:return whether he is Married or Not Married if present else empty string
# # # # # #                         Designation:return Latest Designation of a Person else return empty string
# # # # # #                         Company:return Latest Company name of a Person else return empty string
# # # # # #                         Experience:return the number of years of Experience the person has else return 0
# # # # # #                         Education:return Highest degree of a person if present else empty string
# # # # # #                         Qualification:return Highest degree of a person if present else empty string
# # # # # #                         Education Institute:return the institute/college name where the person studied highest degree if present else empty string
# # # # # #                         Marks in percentage:return how much percentage person scored in higest degree if present else empty string
# # # # # #                         Specialization:return specialization in higest degree if present else empty string
# # # # # #                         Year of passing:return in which year he passed the highest degree if present else empty string
# # # # # #                         Primary Skills: return ALL the technical skills provided in the content as a list else return empty string. ALWAYS Include all the technical skills from experience section and any section named like "Technical Skills" in the entire given content.Exclude any text that are mentioned inside the Products Specialization and skills that are prefixed with "Trained on", "having knowledge of", or "Learned".
# # # # # #                         Secondary Skills: Extract skills that are prefixed with "Trained on", "having knowledge of", or "Learned". Exclude any skills that are not prefixed with these phrases. Also exclude any skills that are listed as primary skills, mentioned in the projects or experience sections, or mentioned in any other section. If no matching skills are found, return an empty string.
# # # # # #                         Job Title:return the title of a job/designation if present else empty string
# # # # # #                         Job description:return description of the job if present else empty string
# # # # # #                         Company Location:Latest company location of a person if present else empty string
# # # # # #                         Industry:return IT or Health or Hardware or Software industry e.t.c... else return empty string
# # # # # #                         Headline:return Experience Headline of a person if present else empty string
# # # # # #                         Employment type:return Full Time or Part Time of a person
# # # # # #                         Date of joining:return joined date of a company if present else empty string
# # # # # #                         Last date:return last date of a company if present else empty string
# # # # # #                         Current CTC:return 0 if not present
# # # # # #                         Expected CTC:return 0 if not present
# # # # # #                         Current Employment Status:return employee status if present else empty string
# # # # # #                         Prefered Location:return prefered location of a person if present else empty string
# # # # # #                         Ready to relocate:return True if present else False
# # # # # #                         Overseas Experience:return True if present else False
# # # # # #                         Notice Period:Extract the notice period should be a numerical value along with its unit (weeks,months, days, or years)e.g:5 days or 3 months or 2 weeks e.t.c. return 0 if Immediate joining present in the text else return empty string.
# # # # # #                         Having Passport:return True if present else False
# # # # # #                         Passport Validity:return the validity of a passport if present else empty string
# # # # # #                         Visa:return True if present else False
# # # # # #                         About:Generate a Summary of the profile in 2-3 lines else return empty string if not present"""
# # # # # # print(num_of_tokens_from_text(text_to_count,model='gpt-3.5-turbo'))


# # # # # # import os
# # # # # # from glob import glob
# # # # # # from pdf2image import convert_from_path
# # # # # # from paddleocr import PaddleOCR
# # # # # # import numpy as np
# # # # # # confidence_threshold = 0.1
# # # # # # ocr = PaddleOCR(use_angle_cls=True, lang='en')


# # # # # # # Assuming perform_ocr and get_completion_from_messages are defined elsewhere

# # # # # # # Get a list of all PDF files in the 'content/payroll' folder
# # # # # # pdf_files = glob('Vinay - BDE_1709810841811.pdf')

# # # # # # # Loop through each PDF file
# # # # # # for pdf_file in pdf_files:
# # # # # #     try:
# # # # # #         pad_ocr = []
# # # # # #         print(f"Processing file: {pdf_file}")
# # # # # #         # Convert PDF to images
# # # # # #         PAGES = convert_from_path(pdf_file, dpi=300)

# # # # # #         # Loop through each page of the PDF
# # # # # #         for i, img_page in enumerate(PAGES):
# # # # # #             print("Page number is ", i + 1)
# # # # # #             print(i)
# # # # # #             if i == 0 or i > 0:
# # # # # #                 cropped_image_np = np.array(img_page)
# # # # # #                 result = ocr.ocr(cropped_image_np, cls=True)
# # # # # #                 print(result)
# # # # # #                 for line in result:
# # # # # #                     if line[-1] and line[-1][1] > confidence_threshold:
# # # # # #                         pad_ocr.append(line[-1][0])

# # # # # #                 #for line in result[0]:
# # # # # #                   #if line[-1] and line[-1][1] > confidence_threshold:
# # # # # #                    # pad_ocr.append(line[-1][0])
# # # # # #         pad_ocr = "\n".join(pad_ocr)
# # # # # #         print(pad_ocr)
# # # # # #         # if len(pad_ocr) > 7000:
# # # # # #         #   system_message = no_samples_system_message

# # # # # import os
# # # # # from glob import glob
# # # # # from pdf2image import convert_from_path
# # # # # from paddleocr import PaddleOCR
# # # # # import numpy as np
# # # # # confidence_threshold = 0.1
# # # # # ocr = PaddleOCR(use_angle_cls=True, lang='en')


# # # # # # Assuming perform_ocr and get_completion_from_messages are defined elsewhere

# # # # # # Get a list of all PDF files in the 'content/payroll' folder
# # # # # pdf_file = '/home/walkingtree/Downloads/ShaikRajak[0y_10m].pdf'

# # # # # # Loop through each PDF file
# # # # # # for pdf_file in pdf_files:
# # # # # try:
# # # # #     pad_ocr = []
# # # # #     print(f"Processing file: {pdf_file}")
# # # # #     # Convert PDF to images
# # # # #     PAGES = convert_from_path(pdf_file, dpi=300)

# # # # #     # Loop through each page of the PDF
# # # # #     for i, img_page in enumerate(PAGES):
# # # # #         print("Page number is ", i + 1)
# # # # #         print(i)
# # # # #         if i == 0 or i > 0:
# # # # #             cropped_image_np = np.array(img_page)
# # # # #             result = ocr.ocr(cropped_image_np, cls=True)
# # # # #             print(result)
# # # # #             try:
# # # # #                 for line in result:
# # # # #                     if line[-1] and line[-1][1] > confidence_threshold:
# # # # #                         pad_ocr.append(line[-1][0])
# # # # #             except:
# # # # #                 for line in result[0]:
# # # # #                     if line[-1] and line[-1][1] > confidence_threshold:
# # # # #                         pad_ocr.append(line[-1][0])

# # # # #             #for line in result[0]:
# # # # #                 #if line[-1] and line[-1][1] > confidence_threshold:
# # # # #                 # pad_ocr.append(line[-1][0])
# # # # #     pad_ocr = "\n".join(pad_ocr)
# # # # #     print(pad_ocr)
# # # # #     # if len(pad_ocr) > 7000:
# # # # #     #   system_message = no_samples_system_message

# # # # #     # Run llm (assuming messages is defined)

# # # # # except Exception as e:
# # # # #     print(f"Error processing file {pdf_file}: {str(e)}") 

# # # # import textract


# # # # # filename="/home/walkingtree/Downloads/siyaramBirla.doc"
# # # # filename=""
# # # # textract_data = textract.process(filename)
# # # # text1 = textract_data.decode("utf-8")
# # # # lines = text1.split('\n')
# # # # total_text_with_info=[]
# # # # total_text=[]
# # # # for ele in enumerate(lines):
# # # #     dict = {}
# # # #     dict['text']=ele[1]
# # # #     dict['line_number']=ele[0]
# # # #     total_text_with_info.append(dict)
# # # #     total_text.append(ele[1])


# # # # print(total_text)

# # # from docx import Document

# # # def extract_text_from_doc(doc_filename):
# # #     try:
# # #         doc = Document(doc_filename)
# # #         text = ''
# # #         for paragraph in doc.paragraphs:
# # #             text += paragraph.text + '\n'
# # #         return text
# # #     except Exception as e:
# # #         print(f"Error occurred while extracting text from {doc_filename}: {e}")
# # #         return None

# # # # Usage example:
# # # filename = 'Naukri_DeepnilBanerjee[14y_0m]_1710333339256.doc'
# # # text_from_doc = extract_text_from_doc(filename)
# # # if text_from_doc:
# # #     # Process extracted text as needed
# # #     print(text_from_doc)


# # # from openai import OpenAI
# # # import os
# # # from datetime import datetime
# # # import os
# # # from glob import glob
# # # import numpy as np
# # # import pandas as pd
# # # from PyPDF2 import PdfReader
# # # current_date = datetime.now().strftime("%Y-%m-%d")

# # # #TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")

# # # # Create an OpenAI client with your deepinfra token and endpoint
# # # openai = OpenAI(
# # #     api_key="clOGyGEyCW2w4mp3jnhmdBioWcVZcmOM",
# # #     base_url="https://api.deepinfra.com/v1/openai",
# # # )


# # # delimiter = "####"
# # # system_message = f"""
# # # Today's Date: {current_date}
# # # You are an experienced resume parser. Given the resume delimited by {delimiter}, \
# # # your goal is to analyze and extract the requested attributes. \
# # # Your analysis is going to help us make recruitment decisions for our company, so parse the resume with care to provide us precise and comprehensive information.\
# # # Provide output against all attributes, if not present return empty string.\
# # # Do not provide explanation for your response against the attributes, as your response is going \
# # #     for further processing in automated way.\

# # # Please extract the following information using the given names ONLY:
# # # First Name
# # # Last Name
# # # Email ID: if 2 email ids, provide it comma-separated
# # # Mobile number: comma-separated for 2 numbers
# # # Location: return current city, state
# # # Permanent Address:return Full Address of a Person like with House Number and Pincode e.t.c
# # # Date of Birth:return date of birth in "mm/dd/yyyy"
# # # Marital Status:return whether he is "Married" or "Not Married"
# # # Designation:return Latest Designation of a Person
# # # Company:return Latest Company name of a Person
# # # Experience: return the total(aggregated) years of corporate full-time work experience the candidate has till Today's Date. \
# # #     include work experience acquired before latest education as well. please return just the numerical in years
# # # Education:return latest education of a person
# # # Qualification:return department or major of latest education
# # # Education Institute:return the institute/college name where the person pursued the latest degree
# # # Marks in percentage:return how much percentage person scored in latest education degree
# # # Specialization:return specialization in latest education degree
# # # Year of passing:return in which year person graduated from the latest education degree
# # # **Primary Skills**: Parse entire text first. provide all programming, technical, coding languages, frameworks provided in the text.\
# # #     Provide output as a list. Please Include all the technical skills\
# # #         from experience section or any section named like "Technical Skills" or "Projects" in the \
# # #             entire given content.Exclude any text that are mentioned inside the Products \
# # #                 Specialization and skills that are prefixed with "Trained on", \
# # #                     "having knowledge of", or "Learned".
# # # Secondary Skills: Any other acquired skills which are not mentioned in primary skills or other attributes
# # # Job Title:return the title of current job/designation if present else empty string
# # # Job description:return summarized description of the current job in 3 sentences(max 50 tokens)
# # # Company Location:Current company location of a person
# # # Industry:return IT or Health or Hardware or Software industry e.t.c
# # # Headline:return Experience main header of a person 
# # # Employment type:return Full Time or Part Time of a person
# # # Date of joining:return joined date of a company
# # # Last date:return last date of a company
# # # Current CTC:return 0 if not present
# # # Expected CTC:return 0 if not present
# # # Current Employment Status: check latest employment dates against Today's date, return "working" if employee is presently working, else "not working"
# # # Prefered Location:return prefered location of a person if present
# # # Ready to relocate:return "Yes" if candidate mentions open to relocation else "No" if candidate mentions Not Open to Relocation.
# # # Overseas Experience:return True if overseas working experience present else False
# # # Notice Period: If candidate has specifically provided this information, please return value in number of days
# # # Having Passport:return True if present else False
# # # Passport Validity:return the validity of a passport
# # # Visa:return True if present else False
# # # About:Generate a Summary of the profile in 2-3 lines else return empty string if not present
# # # """

# # # system_message_1 = f"""
# # # Today's Date: {current_date}
# # # As an experienced resume parser, your task is to meticulously analyze a resume and extract specific attributes. The resume will be provided to you segmented by the delimiter "####". 

# # # Here are the step-by-step instructions to guide you through the process:

# # # 1. **Analyze the Resume**: Begin by reading the entire resume thoroughly. Pay close attention to each section and the details provided.

# # # 2. **Extract the Attributes**: For each of the following attributes, locate the relevant information in the resume and extract it. If the information is not present, return an empty string. Do not provide any explanations for your responses as they will be processed automatically.

# # #     - First Name
# # #     - Last Name
# # #     - Email ID: If there are 2 email IDs, provide them separated by a comma.
# # #     - Mobile number: If there are 2 numbers, provide them separated by a comma.
# # #     - Location: Return the current city and infer the state from city.
# # #     - Permanent Address: Full address of the person, including house number and pin code.
# # #     - Date of Birth: Return the date of birth in "mm/dd/yyyy" format.
# # #     - Marital Status: Indicate whether the person is "Married" or "Not Married".
# # #     - Designation: The latest designation of the person.
# # #     - Company: The latest company name of the person.
# # #     - Experience: The total years of corporate full-time work experience the candidate has till today's date. Include work experience acquired before the latest education as well. Please return just the numerical value in years.
# # #     - Education: The latest education of the person.
# # #     - Qualification: The department or major of the latest education.
# # #     - Education Institute: The institute/college name where the person pursued the latest degree.
# # #     - Marks in percentage: The percentage the person scored in their latest education degree.
# # #     - Specialization: The specialization in the latest education degree.
# # #     - Year of passing: The year the person graduated from the latest education degree.
# # #     - Primary Skills: Provide all programming, technical, coding languages, frameworks provided in the text as a list. Include all the technical skills from the experience section or any section named like "Technical Skills" or "Projects" in the entire given content. Exclude any text that is mentioned inside the Products Specialization and skills that are prefixed with "Trained on", "having knowledge of", or "Learned".
# # #     - Secondary Skills: Any other acquired skills which are not mentioned in primary skills or other attributes.
# # #     - Job Title: The title of the current job/designation.
# # #     - Job description: Summarized description of the current job in 3 sentences (max 50 tokens).
# # #     - Company Location: Current company location of the person.
# # #     - Industry: The industry the person is working in (IT, Health, Hardware, Software, etc.).
# # #     - Headline: The experience main header of the person.
# # #     - Employment type: Whether the person is working full time or part time.
# # #     - Date of joining: The date the person joined their current company.
# # #     - Last date: The last date the person worked at their previous company.
# # #     - Current CTC: If not present, return 0.
# # #     - Expected CTC: If not present, return 0.
# # #     - Current Employment Status: Check the latest employment dates against today's date, return "working" if the employee is presently working, else "not working".
# # #     - Preferred Location: The preferred location of the person.
# # #     - Ready to relocate: Return "Yes" if the candidate mentions they are open to relocation, else "No" if they mention they are not open to relocation.
# # #     - Overseas Experience: Return True if overseas working experience is present, else False.
# # #     - Notice Period: If the candidate has specifically provided this information, please return the value in the number of days.
# # #     - Having Passport: Return True if present, else False.
# # #     - Passport Validity: The validity of the passport.
# # #     - Visa: Return True if present, else False.
# # #     - About: Generate a summary of the profile in 2-3 lines.

# # # 3. **Review Your Work**: Once you have extracted all the attributes, review your work to ensure accuracy and completeness. Remember, your analysis will help us make important recruitment decisions, so precision and thoroughness are key.

# # # Good luck with your task! Your expertise in resume parsing is crucial for providing the most precise and comprehensive information possible.
# # # """


# # # pdf_files = glob('/home/walkingtree/Downloads/Sandeep Resume.pdf')

# # # # Loop through each PDF file
# # # for pdf_file in pdf_files:
# # #     try:
# # #         pad_ocr = []
# # #         print(f"Processing file: {pdf_file}")
# # #         # Convert PDF to images
# # #         #print(pdf_file)
# # #         reader = PdfReader(pdf_file)
# # #         #print(len(reader.pages))
# # #         # Loop through each page of the PDF
# # #         for i, page in enumerate(reader.pages):
# # #             print("Page number is ", i + 1)
# # #             text = page.extract_text()
# # #             #print(text)
# # #             pad_ocr.append(text)
# # #         pad_ocr = "\n".join(pad_ocr)

# # #         #print(pad_ocr)
# # #         print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")

# # #         # Run llm (assuming messages is defined)
# # #         user_message = f"""{pad_ocr}"""

# # #         messages =  [
# # #                     {'role':'system',
# # #                     'content': system_message},
# # #                     {'role':'user',
# # #                     'content': f"{delimiter}{user_message}{delimiter}"},
# # #                     ]
# # #         chat_completion = openai.chat.completions.create(
# # #             model="mistralai/Mixtral-8x7B-Instruct-v0.1",
# # #             messages=messages,
# # #             temperature=0.4,
# # #             max_tokens=10000
# # #             )

# # #         print(chat_completion.choices[0].message.content)


# # #         # print(system_message)
# # #         # print(f"{delimiter}{user_message}{delimiter}")
# # #         # response = get_completion_from_messages(messages)
# # #         # pad_ocr = pad_ocr.replace('\n', '\\n')
# # #         # response = response.replace('\n', '\\n')
# # #         # system_msg = system_message.replace('\n', '\\n')
# # #         #print("Lenth of Tokens fed to LLM:{}".format(len(messages)))
# # #         print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
# # #         #print(response)

# # #     except Exception as e:
# # #         print(f"Error processing file {pdf_file}: {str(e)}")


# # # @app.route('/', methods=['POST'])
# # # def get_path():   
# # #     if request.method == 'POST':
# # #         filepath = request.json.get('filename')  # Get the query parameter from the URL
# # #         # data=resume_parser()
# # #         try:
# # #             print("entered into try in get_path")
# # #             mycollection,conn = resumeDetailsCollection()
# # #             obj=mycollection.find({"file_path":str(filepath)})
# # #             records=[]
# # #             for record in obj:
# # #                 records.append(record)
# # #             if not records:
# # #                 print("filepath:",filepath)
# # #                 filename = str(filepath).split("/")[-1]
# # #                 print("filename:",filename)
# # #                 s3_client.download_file(AWS_S3_BUCKET_NAME, filepath, filename)
# # #                 data = ResumeParser(filename,filepath).get_extracted_data()

# # #                 print("Entered before return")
# # #                 try:
# # #                     os.remove(filename)
# # #                 except:
# # #                     pass
# # #                 return jsonify({'response': data})
# # #         finally:
# # #             conn.close()


# # # Assume openai>=1.0.0
# # from openai import OpenAI
# # import os
# # from datetime import datetime
# # import os
# # from glob import glob
# # import numpy as np
# # import pandas as pd
# # from PyPDF2 import PdfReader
# # current_date = datetime.now().strftime("%Y-%m-%d")

# # #TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")

# # # Create an OpenAI client with your deepinfra token and endpoint
# # openai = OpenAI(
# #     api_key="BgJ9naAUL7ILC5zb4Wz4YOLRlmvJPrGN",
# #     base_url="https://api.deepinfra.com/v1/openai",
# # )


# # delimiter = "####"
# # system_message = f"""<s>[INST]
# # Today's Date: {current_date}
# # **Task** - You are an experienced job resume parser. Given the resume delimited by {delimiter}, \
# # your goal is to analyze the resume and extract all attributes till the last "About" attribute.

# # **Important Notes**
# # 1. Provide output against all attributes, if not present return empty string.
# # 2. don't finish generating till you have provided response for the last "About" attribute.
# # 3. No explanation required for your response against the attributes, as your response is going
# # for further processing in an automated way.

# # **Procedure**
# # Please extract the ALL following attributes using the given names ONLY:
# # First Name
# # Last Name
# # Email ID: if 2 email ids, provide comma-separated
# # Mobile number: comma-separated for 2 numbers
# # Location: current city, state
# # Permanent Address:Full Address of a Person like with House Number and Pincode e.t.c
# # Date of Birth:date of birth in "mm/dd/yyyy"
# # Marital Status:"Married" or "Not Married"
# # Designation:Latest Designation of Person
# # Company:Latest Company name of Person
# # Experience: Identify the candidate's corporate experiences in the text and calculate the total years of corporate work experience up to today's date. Only include corporate experience, excluding education, personal projects, or internships. Provide the numerical value in years for the total corporate work experience.
# # Education:return latest education of a person
# # Qualification:department or major of latest education
# # Education Institute:institute/college name where the person pursued the latest degree
# # Marks in percentage:percentage or gpa person scored in latest education degree with unit
# # Specialization:specialization in latest education degree
# # Year of passing:when person graduated from the latest education degree
# # Primary Skills: Parse entire text first. Please provide ALL programming, technical, coding languages, coding/technical frameworks provided in the entire text. Provide your outptut as a list.
# # Secondary Skills: Any other acquired skills which are not mentioned in primary skills or other attributes
# # Job Title:title of current job/designation
# # Job description:summarized description of the current job in 3 sentences(max 50 tokens)
# # Company Location:Current company location of a person
# # Industry:IT or Health or Hardware or Software industry e.t.c
# # Headline: Work Experience main header of a person 
# # Employment type:Full Time or Part Time of a person
# # Date of joining:joined date of a company in mm/yyyy
# # Last date:return last date of a company in dd/mm/yyyy
# # Current CTC:return 0 if not present
# # Expected CTC:return 0 if not present
# # Current Employment Status: check latest employment dates against Today's date, return "working" if employee is presently working, else "not working"
# # Prefered Location:prefered job locations of a person
# # Ready to relocate:"Yes" if candidate is open to relocation else "No" if candidate is Not Open to Relocation.
# # Overseas Experience:True if overseas working experience present else False
# # Notice Period: If candidate has specifically provided this information, please return value in number of days
# # Having Passport:True or False
# # Passport Validity:return the validity of a passport
# # Visa:True or False
# # About:Generate a short summary of the profile in less than 100 tokens else return empty string if not present

# # [/INST]
# # """

# # system_message_1 = f"""
# # Today's Date: {current_date}
# # As an experienced resume parser, your task is to meticulously analyze a resume and extract specific attributes. The resume will be provided to you segmented by the delimiter "####". 

# # Here are the step-by-step instructions to guide you through the process:

# # 1. **Analyze the Resume**: Begin by reading the entire resume thoroughly. Pay close attention to each section and the details provided.

# # 2. **Extract the Attributes**: For each of the following attributes, locate the relevant information in the resume and extract it. If the information is not present, return an empty string. Do not provide any explanations for your responses as they will be processed automatically.

# #     - First Name
# #     - Last Name
# #     - Email ID: If there are 2 email IDs, provide them separated by a comma.
# #     - Mobile number: If there are 2 numbers, provide them separated by a comma.
# #     - Location: Return the current city and infer the state from city.
# #     - Permanent Address: Full address of the person, including house number and pin code.
# #     - Date of Birth: Return the date of birth in "mm/dd/yyyy" format.
# #     - Marital Status: Indicate whether the person is "Married" or "Not Married".
# #     - Designation: The latest designation of the person.
# #     - Company: The latest company name of the person.
# #     - Experience: The total years of corporate full-time work experience the candidate has till today's date. Include work experience acquired before the latest education as well. Please return just the numerical value in years.
# #     - Education: The latest education of the person.
# #     - Qualification: The department or major of the latest education.
# #     - Education Institute: The institute/college name where the person pursued the latest degree.
# #     - Marks in percentage: The percentage the person scored in their latest education degree.
# #     - Specialization: The specialization in the latest education degree.
# #     - Year of passing: The year the person graduated from the latest education degree.
# #     - Primary Skills: Provide all programming, technical, coding languages, frameworks provided in the text as a list. Include all the technical skills from the experience section or any section named like "Technical Skills" or "Projects" in the entire given content. Exclude any text that is mentioned inside the Products Specialization and skills that are prefixed with "Trained on", "having knowledge of", or "Learned".
# #     - Secondary Skills: Any other acquired skills which are not mentioned in primary skills or other attributes.
# #     - Job Title: The title of the current job/designation.
# #     - Job description: Summarized description of the current job in 3 sentences (max 50 tokens).
# #     - Company Location: Current company location of the person.
# #     - Industry: The industry the person is working in (IT, Health, Hardware, Software, etc.).
# #     - Headline: The experience main header of the person.
# #     - Employment type: Whether the person is working full time or part time.
# #     - Date of joining: The date the person joined their current company.
# #     - Last date: The last date the person worked at their previous company.
# #     - Current CTC: If not present, return 0.
# #     - Expected CTC: If not present, return 0.
# #     - Current Employment Status: Check the latest employment dates against today's date, return "working" if the employee is presently working, else "not working".
# #     - Preferred Location: The preferred location of the person.
# #     - Ready to relocate: Return "Yes" if the candidate mentions they are open to relocation, else "No" if they mention they are not open to relocation.
# #     - Overseas Experience: Return True if overseas working experience is present, else False.
# #     - Notice Period: If the candidate has specifically provided this information, please return the value in the number of days.
# #     - Having Passport: Return True if present, else False.
# #     - Passport Validity: The validity of the passport.
# #     - Visa: Return True if present, else False.
# #     - About: Generate a summary of the profile in 2-3 lines.

# # 3. **Review Your Work**: Once you have extracted all the attributes, review your work to ensure accuracy and completeness. Remember, your analysis will help us make important recruitment decisions, so precision and thoroughness are key.

# # Good luck with your task! Your expertise in resume parsing is crucial for providing the most precise and comprehensive information possible.
# # """

# # # system_message = f"""
# # # 1. Today's Date is {current_date}.
# # # 2. As an experienced job resume parser, your task is to analyze the resume delimited by {delimiter} and extract all 38 attributes.
# # # 3. Provide output for all 38 attributes, returning an empty string if the attribute is not present.
# # # 4. No need for explanations in your responses, as they will be used for further automated processing.
# # # 5. Begin by extracting the first 5 attributes (First Name, Last Name, Email ID, Mobile number, Location).
# # # 6. Next, extract attributes 6 to 10 (Permanent Address, Date of Birth, Marital Status, Designation, Company).
# # # 7. Then, move on to attributes 11 to 20 (Experience, Education, Qualification, Education Institute, Marks in percentage, Specialization, Year of passing, Primary Skills, Secondary Skills, Job Title).
# # # 8. After that, extract attributes 21 to 30 (Job description, Company Location, Industry, Headline, Employment type, Date of joining, Last date, Current CTC, Expected CTC, Current Employment Status).
# # # 9. Finally, extract attributes 31 to 38 (Prefered Location, Ready to relocate, Overseas Experience, Notice Period, Having Passport, Passport Validity, Visa, About).
# # # 10. Optimize the prompt by rephrasing sentences for clarity, conciseness, and relevance while preserving the original intent.
# # # """

# # # pdf_files = glob('Dix*.pdf')

# # # # Loop through each PDF file
# # # for pdf_file in pdf_files:
# # #     try:
# # #         pad_ocr = []
# # #         print(f"Processing file: {pdf_file}")
# # #         # Convert PDF to images
# # #         #print(pdf_file)
# # #         reader = PdfReader(pdf_file)
# # #         #print(len(reader.pages))
# # #         # Loop through each page of the PDF
# # #         for i, page in enumerate(reader.pages):
# # #             print("Page number is ", i + 1)
# # #             text = page.extract_text()
# # #             #print(text)
# # #             pad_ocr.append(text)

# # #         pad_ocr = "\n".join(pad_ocr)

# # #         #print(pad_ocr)
# # #         print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")

# #         # Run llm (assuming messages is defined)
# # pad_ocr="""

# # U d a i p u r ,  I n d i a ,  3 1 3 0 0 1v i n o d . p a t i d a r 2 0 0 7 @ g m a i l . c o mM o b i l e + 9 1  9 4 6  1 1 1  9 6 0 8 h t tps:/ / www . link edin. com/in/ vinodpa tidarv i n o d  p a t i d a r F U L L  S T A C K  S E N I O R  E N G I N E E R P R O F E S S I O N A L  S U M M A R Y E x p e r i e n c e d  F u l l  S t a c k  S e n i o r  E n g i n e e r  w i t h  o v e r  1 5 +  y e a r s  o f  e x p e r i e n c e .   D e m o n s t r at e d  l e a d e r s h i p  s k i l l s  a n d  d e d i c at i o n  t o  s o lv i n g  c o m p l e x p r o b l e m s .  A b l e   t o  e ff e c t i v e l y  l e a d  t e a m s  a n d  d e l i v e r  h i g h - q u a l i t y  s o l u t i o n s .  L o o k i n g  t o  l e v e r a g e   e x p e r t i s e  a n d  c o n t r i b u t e  t o  t h e  s u c c e s s  o f  a  d y n a m i c  o r g a n i z at i o n . D e v e l o p e d  w e b,  m o b i l e  a p p s  u s i n g  R e a c t N at i v e ,  R e a c t J S ,  R e d u x ,  P y t h o n  D R F ,   D j a n g o,  P H P ,  P o s t g r e S Q L ,  M y S Q L ,  a n d  N o d e J S  e t c  B u i l d i n g  p e r f o r m a n t  m o b i l e  a p p s  s u p p o r t e d  o n  b o t h  t h e  i O S  a n d  A n d r o i d   p l atf o r m s  u s i n g  R e a c t N at i v e  E x p e r i e n c e  a r c h i t e c t u r e  b u i l d i n g ,  s e r v e r l e s s  w e b,  m o b i l e  a p p l i c at i o n s  u s i n g  A W S   L a m b d a  a n d  A P I  G at e w a y  S t r o n g  e m p h a s i s  o n  O b j e c t - O r i e n t e d  a n d  m o d u l a r  d e s i g n  B u i lt  C a c h i n g  i n f r a s t r u c t u r e  R e d i s  a n d  C l o u d fl a r e  C o m f o r t a b l e  w i t h  d at a b a s e  p e r f o r m a n c e  t u n i n g  u s i n g  M y S Q L ,  a n d  P o s t g r e S Q L   s t o r e d  p r o c e d u r e s ,  t r i g g e r s ,  i n d e xe s ,  a n d  t a b l e  p a r t i t i o n s  e t c  A p a r t  f r o m  t h e  a b o v e  t e c h n o l o g i e s  I  p o s s e s s  c o m m o n  p r o f e s s i o n a l  s k i l l s  s u c h   a s  k n o w l e d g e  o f  G I T ,  J I R A ,  A g i l e  S c r u m ,  a n d  R E S T f u l  W e b S e r v i c e s ,  e t c . E M P L O Y M E N T  H I S T O R Y L e d  a  t e a m  a s  a  F u l l  S t a c k  S e n i o r  E n g i n e e r  at  A r c G at e ,  a  l e a d i n g  I T   c o m p a n y  R e s p o n s i b l e  f o r  m a n a g i n g  p r o j e c t s  a n d  e n s u r i n g  t h e i r  s u c c e s s f u l   c o m p l e t i o n  D e v e l o p e d  a n d  m a i n t a i n e d  M o b i l e  A p p,  F r o n t - e n d  a n d  B a c k - e n d   s y s t e m s  U t i l i z e d  m y  e x p e r t i s e  i n  F u l l  S t a c k  d e v e l o p m e n t  t o  d e l i v e r  h i g h - q u a l i t y   s o f t w a r e  s o l u t i o n s  S k i l l s  -  R e a c t J S ,  P y t h o n  D j a n g o,  D R F ,  N o d e J S ,  R e a c t N at i v e ,  R e d u x ,   R E S T  A P I ,  P H P ,  M Y S Q L ,  P o s t g r e S Q L  e t c .JUL, 2013 - PRESENT F u l l S t a c k  S e n i o r  E n g i n e e r ,  A r c G a t e ,  U d a i p u r ,  I n d i a L e d  a  t e a m  a s  a  S e n i o r  S o f t w a r e  E n g i n e e r i n g  at  H i d d e n  B r a i n s ,  a   l e a d i n g  I T  c o m p a n y  R e s p o n s i b l e  f o r  m a n a g i n g  p r o j e c t s  a n d  e n s u r i n g  t h e i r  s u c c e s s f u l   c o m p l e t i o n  D e v e l o p e d  a n d  m a i n t a i n e d  b a c k - e n d  s y s t e m s  U t i l i z e d  m y  e x p e r t i s e  i n  w e b  a p p l i c at i o n  d e v e l o p m e n t  t o  d e l i v e r  h i g h - q u a l i t y  s o f t w a r e  s o l u t i o n s  S k i l l s  -  P H P ,  C a k e P H P ,  M Y S Q L ,  H T M L ,  C S S ,  o p e n  s o u r c e ,  f r a m e w o r k ,   e t c .S e n i o r  S o f t w a r e  E n g i n e e r ,  H i d d e n B r a i n s  I n f o T e c h  P .  L t d ,  A h m e d a b a dA UG, 2012 - JUL, 2013 A  S e n i o r  S o f t w a r e  E n g i n e e r  at  D o t S q u a r e s ,  a  l e a d i n g  I T  c o m p a n y  R e s p o n s i b l e  f o r  a s s i g n e d  t a s k s  i n  t h e  p r o j e c t  a n d  e n s u r i n g  t h e i r   s u c c e s s f u l  c o m p l e t i o n  D e v e l o p e d  a n d  m a i n t a i n e d  b a c k - e n d  s y s t e m s  U t i l i z e d  m y  e x p e r t i s e  i n  w e b  a p p l i c at i o n  d e v e l o p m e n t  t o  d e l i v e r  h i g h - q u a l i t y  s o f t w a r e  s o l u t i o n s  S k i l l s  -  C o r e  P H P ,  C a k e P H P ,  a n d  k n o w l e d g e  o f  W o r d P r e s s  a n d  o t h e r   o p e n - s o u r c e ,  F r a m e w o r k s ,  P a y m e n t  G at e w a y  i n t e g r at i o n ,  e t c .S e n i o r  S o f t w a r e  E n g i n e e r ,  D o t S q u a r e s  L t d ,  J a i p u r ,  I n d i aAPR, 2011 - JUL, 2012 G i t ,  S V NB a c k - e n d  D e v e l o p m e n tF r o n t - e n d  D e v e l o p m e n tD o c k e rA W SC a k e P H PP H PR E S T  A P IJ a v a S c r i p tR e d u xN o d e J SP o s t g r e S Q L ,  M Y S Q LP y t h o n  D j a n g o ,  D R FR e a c t  N a t i v eR e a c t J SS K I L L S P o s t  G r a d u at e d  w i t h  h o n o r s ,  r e c e i v i n g  a n  A +M S C  i n  C o m p u t e r  S c i e n c e ,  E I I L M  U n i v e r s i t yAPR, 2009 - JUL, 2011 B a c h e l o r  o f  C o m p u t e r  A p p l i c a t i o n ,  M C R P V  B h o p a l U n i v e r s i t yMA Y , 2004 - JUL, 200 7E D U C A T I O NA  W e b  D e v e l o p e r  E n g i n e e r i n g  at  a r r o W e b s ,  a  l e a d i n g  I T  c o m p a n y  R e s p o n s i b l e  f o r  a s s i g n e d  t a s k s  i n  t h e  p r o j e c t  a n d  e n s u r i n g  t h e i r   s u c c e s s f u l  c o m p l e t i o n  D e v e l o p e d  a n d  m a i n t a i n e d  b a c k - e n d  s y s t e m s  i n  P H P ,  M Y S Q L  e t c  U t i l i z e d  m y  e x p e r t i s e  i n  w e b  a p p l i c at i o n  d e v e l o p m e n t  t o  d e l i v e r  h i g h - q u a l i t y  s o f t w a r e  s o l u t i o n s  S k i l l s  -  P H P ,  H T M L ,  C S S ,  J A V A S C R I P T ,  a n d  k n o w l e d g e  o f  W o r d P r e s s   e t c .E M P L O Y M E N T  H I S T O R Y A UG, 200 7  - MAR, 2011 S e n i o r  W e b  D e v e l o p e r ,  a r r o W e b s  ( G e e t i k a  S o f t w a r e ) ,  U d a i p u r ,  I n d i a  A b o u t  -  I t  i s  a  b a n k i n g  a n d  p a y m e n t  p l atf o r m  f o r  s o f t w a r e  t e a m s   b u i l d i n g  t h e  n e x t  g e n e r at i o n  o f  fi n a n c i a l  p r o d u c t s  &  s e r v i c e s  i n   r e g u l at e d  a n d  u n r e g u l at e d  i n d u s t r i e s   F e at u r e s  -  Th e  A P I  p l atf o r m  e n a b l e s  w h i t e - l a b e l  A C H ,  W i r e s ,  S t a b l e c o i n   p a y m e n t  p r o c e s s i n g ,  m o n e y  t r a n s f e r ,  d i g i t a l  w a l l e t s ,  b a n k  a c c o u n t   l i n k i n g ,  a n d  I D  v e r i fi c at i o n  o f  b u s i n e s s e s  ( K Y B )  a n d  i n d i v i d u a l s  ( K YC ) ,   e t c   T e c h n o l o g i e s  -  P Y T H O N  D j a n g o,  R E S T  A P I ,  R e a c t J S ,  N o d e J S ,  P o s t g r e S Q L ,   B o o t s t r a p,  J a v a S c r i p t ,  S A S S ,  A W S ,  D o c k e r ,  e t c   M y  R o l e  -  A s  a  S e n i o r  F u l l  S t a c k  E n g i n e e r ,  D e s i g n e d  t h e  F r o n t - E n d   A r c h i t e c t u r e  a n d  d e v e l o p e d  t h e  R E S T f u I  A P I s ,  d e s i g n e d  t h e  d at a b a s e   s t r u c t u r e ,  w r o t e  a n  i m p l e m e n t at i o n  p l a n ,  a n d  w r o t e  a  U n i t  t e s t  c a s e ,   d e p l o y m e n t ,  a n d  l e d  t h e  t e a m ,  e t c .B ANK ING, DIGIT AL  W ALLET  & A CH P A Y ME NT S API F OR S OFTW ARE TEAMF i n t e c h  -  D o m a i n  A b o u t  -  A n  I n d i a n  n e w s  m e d i a  c o m p a n y  f o c u s i n g  o n  b r o a d c a s t  a n d   d i g i t a l  n e w s  p u b l i c at i o n s  a n d  D i g i t a l  E - P a p e r s .  Th e  c o m p a n y  i s   c o n s i d e r e d  t o  b e  a  l e g a c y  b r a n d  t h at  p i o n e e r e d  i n d e p e n d e n t  n e w s   b r o a d c a s t i n g  i n  I n d i a  e t c   F e at u r e s  -  Th e  W e b  p o r t a l s  i n  H i n d i ,  E n g l i s h ,  E - P a p e r s ,  M o b i l e   A p p l i c at i o n s ,  A P I  p l atf o r m s ,  e t c   T e c h n o l o g i e s  -  R e a c t J S ,  N o d e J S ,  P H P ,  C a k e P H P  F r a m e w o r k ,  R E S T  A P I ,   M y S Q L ,  G o o g l e  S e r v i c e s ,  J a v a S c r i p t ,  Th i r d - p a r t y  S D K  A P I ,  e t c   M y  R o l e  -  A s  a  S e n i o r  S o f t w a r e  E n g i n e e r ,  D e s i g n e d  t h e  F r o n t - E n d   A r c h i t e c t u r e  a n d  c o n s u m e d  t h e  A P I ,  h a n d l e d  t h e  r o u t e s ,  w r o t e  t h e   i m p l e m e n t at i o n  p l a n ,  d e p l o y m e n t  a n d  l e d  t h e  t e a m ,  e t c .NEW S, MEDIA  A GE NC Y , E -P APER, VIDE OS, TV .N e w s ,  M e d i a  -  D o m a i n  A b o u t  -  A n  I n d i a n  s t o c k  m a r k e t ,  e q u i t y  m a r k e t ,  o r  s h a r e  m a r k e t ,   a g g r e g at i o n  o f  b u y e r s  a n d  s e l l e r s  o f  s t o c k s ,  b u y ,  s e l l ,  r e p r e s e n t  t h e   o w n e r s h i p  o f  l i v e  s h a r e s  p o r tf o l i o s ,  e t c   F e at u r e s  -  Th e  W e b  c o n s o l e  o f  t h e  s h a r e  m a r k e t  p r i c e  c h a r t s ,  u p  a n d   d o w n  t h e  s t o c k  p r i c e s ,  l i v e  b u y ,  s e l l ,  p o r tf o l i o  m a n a g e m e n t ,  e t c   T e c h n o l o g i e s  -  R e a c t J S ,  N o d e J S ,  P H P ,  C a k e P H P  F r a m e w o r k ,  R E S T  A P I ,   M y S Q L ,  G o o g l e  S e r v i c e s ,  J a v a S c r i p t ,  Th i r d - p a r t y  S D K  A P I ,  e t c   M y  R o l e  -  A s  a  S e n i o r  S o f t w a r e  E n g i n e e r ,  D e s i g n e d  t h e  F r o n t - E n d   t e r m i n a l  A r c h i t e c t u r e  a n d  c o n s u m e d  t h e  s e r v i c e  p r o v i d e r  A P I ,  h a n d l e d   t h e  m i l l i o n s  o f  c o n c u r r e n t  u s e r s  a n d  m a n y  m o r e  a p p  f e at u r e   e n h a n c e m e n t s ,  w r o t e  t h e  i m p l e m e n t at i o n  p l a n ,  d e p l o y m e n t  a n d  l e d   t h e  t e a m ,  e t c .S T OCK  MAR KET , E QUITY  MAR KET , OR SHARE MAR KET , BUY ERS AND SELLERS OF  S T OCK S.S t o c k  M a r k e t  -  D o m a i nP O R T F O L I OJ i r a S c r u m S V NS K I L L S E n g l i s h H i n d iL A N G U A G E S L i n k e d I n h t t p s : / / w w w . l i n k e d i n . c o m / i n / v i n o d p a t i d a r /   S t a c k  O v e r fl o w h t t p s : / / s t a c k o v e r fl o w . c o m / u s e r s / 1 6 4 5 1 4 5 / v i n o d - p a t i d a rL I N K S I  l o v e  r e a d i n g   b o o k s  a n d  n a t u r e   p h o t o g r a p h y ,   t r a v e l i n g ,  e t c .H O B B I E S
# # """

# # # """
# # # |Divya Maka                                         |Global Business Services   | |Email id makadivya@yahoo.com                      |                           | |Phone Number 9989701184                           |                           | |Education                                                                       | | |Qualifications    |BTech in IT                                                 | |                  |                                                            | |                  |Auroras Engineering college, India, 2010                    | |                  |                                                            | |                  |                                                            | |                  |                                                            | |Languages         |English                                              | |                  |Fluent                                               | |                  |                                                     | |Professional experience                                                        | |Profile           |-12.1 years of IT industry experience encompassing a wide   | |                  |range of skill sets, roles and industry verticals.          | |                  |- Extensive experience with analysis, design, development,  | |                  |customizations, implementation and maintenance using Oracle | |                  |Applications R12 over varied versions and releases.         | |                  |- Worked as onsite client coordinator in South Africa for 3 | |                  |months for a short-term development                         | |                  |- My principle skills are Oracle APPS (Technical) and PLSQL.| |                  |- I have worked on financial module PA, AP, HRMS, PO, and AR| |                  |and have knowledge on OM modules of ERP.                    | |                  |- Possess functional knowledge on O2C, P2P Cycles.          | |                  |- Also I have worked extensively in technical areas using   | |                  |different tools like TOAD, SQL Developer, PL-SQL  Developer,| |                  |Web adi, SQL*PLUS, XML Gateway,  Oracle Forms, Oracle       | |                  
# # # |Reports, Unix (Sql loader),Alerts, Publisher reports,       | |                  |Interfaces and Conversions.                                 | |                  |- Exposure to R12, worked on upgrading objects from 11.5.10 | |                  |to R 12.1.3.                                                | |                  |- Worked on MD70, MD120, CV40 documentations as part of     | |                  |project.                                                    | |                  |- Have knowledge on Python basics.                          | |Key Skills        |ERP  Oracle Applications R12 (E-Business Suite)            | |                  |                                                            | |                  |Oracle Technologies Oracle Reports, XML/BI Publisher,      | |                  |Workflow, Interface, Conversion, XML Gateway, RICE          | |                  |development                                                 | |                  |                                                            | |                  |Development Tools PL/SQL Developer, SQL Developer,         | |                  |JDeveloper, SQL Plus, Oracle Dev Suite 10g (Reports, Forms),| |                  |Oracle Workflow Builder, Oracle XML Publisher Builder       | |                  |                                                            | |                  |Functional Modules Purchase Order (PO), Accounts Payable   | |                  |(AP), Account Receivables (AR) ,Project Accounting (PA),    | |                  |HRMS,  Knowledge on OM modules                              | |                  |                                                            | |                  |RDBMS  Oracle 10g, 11g, 12c                                | |                  |                                                            | |                  |Languages PL/SQL,  Oracle SQL, XML                         | |                  |                                                            | |                  |Operating Systems Windows XP, Unix                         | |                  |                                                            | |                  |Processes IBM’s QMS (Quality Management System)            | |                  |                                                            | |                  |- Version Management  PVCS, Ace Management tool            | |                  |                                                            | |Key Courses and   |Python(Basics)                                              | |Training          |                                                            | |               
# # #    |                                                            | |Career History    |01/2015 - To date                                           | |                  |IBM India Pvt Limited, India                                | |                  |Application Developer                                       | |                  |Oracle eBS Technical Consultant with experience in Finance  | |                  |modules                                                     | |                  |                                                            | |                  |07/2013 - 01/2015                                           | |                  |Tata Consultancy Services, India                            | |                  |Systems Engineer                                            | |                  |Team Developer                                              | |                  |                                                            | |                  |08/2010 - 06/2013                                           | |                  |Hitachi Consulting, India                                   | |                  |Associate Consultant                                        | |                  |Team Developer                                              | |                  |                                                            | |                  |                                                            | |                  |                                                            | |Assignment History|12/2020 – 09/2022                                           | |                  |21 months                                                   | |                  |                                                            | |                  |NOV                                                         | |                  |-                                                           | |                  |Project Description NOV Inc., formerly National Oilwell    | |                  |Varco, is an American multinational corporation based in    | |                  |Houston, Texas. It is a worldwide provider of equipment and | |                  |components used in oil and gas drilling and production      | |                  |operations, oilfield services, and supply chain integration | |                  |services to the upstream oil and gas industry.              | |                  |                                                            | |                  |Contribution Working on Support and Enhancements.          | |                  |I am working on few Integrations. Also working on support   | |                  |Issues.                                                     | |                  |                                                            | |                  |Enhancements worked till date                               | |                  |Worked on TPH supplier integration and also enhanced it by  | |                  |adding bank creation and updating, branch creation/updating | |                  |logic. Working on resolving the issues raised by TPH for    | |                  |both the streams CAPS and RIGS.                             | |                  |Worked on complex report Genealogy report resolving         | |                  |performance issue on same and enhanced the report by adding | |                  |new columns based on logic to derive the same.              | |                  |Worked on enhancing TPH supplier by creating customer for   | |                  |Brazil OU for CAPS                                          | |                  |Working on resolving Employee Hub issues in CAPS.           | |                  |Worked in IAR Mass Transfer Program by enhancing it to send | |                  |bulk notifications at a time                                | |                  |Analysing commingled program and enhanced the code wherever | |                  |it is required.                                             | |                  |Developed India localization logic for Basware Invoices for | |                  |IN org.                                                     | |                  |Worked on complex report Job work Inventory movement report | |                  |Working on Basware AP Invoice Integration                   | |                  |Working on SAFT enhancement(NOV 1359 Standard Audit File Tax| |                  |Report)                                                     | |                  |                                                            | |                  |12/2020 – 09/2022                                           | |                  |21 months                                                   | |                  |                                                            | |                  |Aurobindo Pharma                                            | |                  |-                                                           | |                  |Project Description Aurobindo Pharma Limited is a          | |                  |pharmaceutical manufacturing company headquartered in HITEC | |                  |City, Hyderabad, India. The company manufactures generic    | |                  |pharmaceuticals and active pharmaceutical ingredients.      | |                  |Need to Implement WMS module for China. As Aurobindo is     | |                  |using Gemini application which is not applicable to Chinese | |                  |language.                                                   | |                  |                                                            | |                  |                                                            | |                  |Contribution Development of custom objects, forms and      | |                  |reports.                                                    | |                  |I have worked on few Integrations. Process of understanding | |                  |the Items category and calculating the quantity based on    | |                  |client driven calculations and applying the same in Oracle  | |                  |WMS system. Development of forms for Vehicle tracking       | |                  |system. Also audit reports in order to know the status of   | |                  |Item.                                                       | |                  |                                                            | |                  |08/2020 - 11/2020                                           | |                  |4 months                                                    | |                  |Poundland                                                   | |                  |-                                                           | |                  |Project Description Poundland have numerous finance systems| |                  |in operation across the Group (Poundland and Dealz),  which | |                  |are outdated and not able to cope with today’s business     | |                  |requirements. Implementing a new solution would allow them  | |                  |to standardise & consolidate practices across the group and | |                  |integrate to the                                            | |                  |stock system, delivering one version of the truth across the| |                  |Group                                                       | |                  |                                                            | |                  |                                                            | |                  |Contribution Implementing Oracle Cloud ERP for             | |                  |Pepkor/Poundland/Dealz/Pepco                                | |                  |Pepkor/Poundland refers to finance part of ERP              | |                  |I have worked on Integration PLSQL , where data from legacy | |                  |is pushed to SOA supported database , do validations        | |                  |according to the business requirement and push the data to  | |                  |conf and fbdi tables; where SOA then picks the data from    | |                  |these tables and generated fbdi files. These files will be  | |                  |loaded to Oracle Cloud and creates the transactions.        | |                  |                                                            | |                  |05/2016 - 05/2019                                           | |                  |37 months                                                   | |                  |MTN Spring                                                  | |                  |-                                                           | |                  |Project Description Mobile Telephone Networks (Pty) Ltd,   | |                  |headquartered in Johannesburg, South Africa is one of the   | |                  |largest mobile telecoms companies in Africa and the Middle  | |                  |East with more than 200 million subscribers.                | |                  |My role in this project is to work on tickets which are     | |                  |assigned to me.                                             | |                  |As a Team Developer 
# # #    I was responsible for analysis, design, | |                  |development, testing, maintenance and bug fixing of Oracle  | |                  |Application ERP solutions. I also played the below mentioned| |                  |roles.                                                      | |                  |                                                            | |                  |Position Team developer                                    | |                  |Contribution -Work on tickets and enhancements which are   | |                  |assigned to me.                                             | |                  |-Work on the below developments assigned to be as part of   | |                  |project requirement.                                        | |                  |1. MTN Extra time enhancement to work for credit memo       | |                  |integration with SAAE.                                      | |                  |2. Standard Bank EBU development to reconcile statements and| |                  |create receipts respectively in cash management.            | |                  |3. General Ledger Inventory Drill down report development to| |                  |know credit and debit information for given period and for  | |                  |given GL account. It displays journal category, source,     | |                  |Accounting flex field, purchase order and sales order issue | |                  |details.                                                    | |                  |4. Projects – Budget Requester Discoverer Report enhancement| |                  |to add new fields such as CPB, cocam code, Task details,    | |                  |Item details.                                               | |                  |Worked on SAAE enhancement, Secured Airtime Acquisition     | |                  |Engine, SAAE Integration works for customers who sell our   | |                  |virtual Items(Airtime & Data) both retail & Wholesale.      | |                  |Customers work on credit Limit. SAAE collects data from     | |                  |billing system. Post to ERP on daily basis where material   | |                  |transaction accounts need to be swapped for miscellaneous   | |                  |receipt and miscellaneous issue.                            | |                  |5. Worked on Invoice Workflow changes enhancement where . In| |                  |invoice Approval notification , the notification URL should | |                  |be changed based on Invoice Source.                         | |                  |If Invoice source is Web Centre the URL should be directed  | |                  |to the URL provided by Web Centre                           | |                  |6. Auto Requisition Remedy development Automation of       | |                  |requisition creation between Remedy and Oracle ERP.         | |                  |Suppliers will capture their quote for the Network Group    | |                  |roll out, in Remedy, once this has been approved by the     | |                  |Project manager in Remedy, the quote will then be interfaced| |                  |to Oracle ERP of which a Requisition will be generated.     | |                  |This requisition will be created with a status of ‘In       | |                  |Process’ and will directly be submitted into the approval   | |                  |Workflow for approval, thereby eliminating the need for any | |                  |manual requisition creation.                                | |                  |7. Quick Receipts enhancement, We have enhanced the existing| |                  |functionality of receiving goods, by developing new logic of| |                  |fetching locator dynamically based on project number , task | |                  |number and vendor. We are creating locator virtually and    | |                  |then receiving goods. Even if Purchase order is not having  | |                  |project or task we are still going to receive goods by using| |                  |NONE as locator                                             | |                  |8. BTS Invoice Processing WCC is a replacement to Image Now| |                  |System.                                                     | |                  |WCC OCR (Optical Character Recognition) Reads the Images and| |                  |will send us the XML information of the BTS Invoices by     | |                  |calling our web service.                                    | |                  |It is a https call to ERP from WCC. The xml data is         | |                  |validated and Invoice is created in Oracle payables module. | |                  |In this change                                              | |                  |1) We have created New Views                                | |                  |2) Also created Payment Template to pay the Invoices using  | |                  |this functionality                                          | |                  |9. Host 2 Host Automation Integration with Standard bank   | |                  |where we send the payment file to bank on regular basis     | |                  |whenever the client raises payments, we then receive interim| |                  |and final files from bank. Based on the interim and final   | |                  |file status MTN will release payment to bank. Then we       | |                  |receive statement for which we create receipts.             | |                  |10. B2B PR Integration We receive quotes from suppliers,   | |                  |create requisitions for those quotes based on business      | |                  |validations and send the response back to suppliers with    
# # #    | |                  |requisition number and other details.                       | |                  |                                                            | |                  |-Worked in Unit Testing on these objects and provide unit   | |                  |test case documents to functional team.                     | |                  |                                                            | |                  |                                                            | |                  |01/2016 - 04/2016                                           | |                  |4 months                                                    | |                  |Motorola Solutions                                          | |                  |-                                                           | |                  |Project Description MSI was a $10B business that was in the| |                  |process of a corporate IT transformation to consolidate     | |                  |their ERPs and move to single instance of Oracle eBS R12.   | |                  |The majority of the completed transformation effort (called | |                  |Trilogy) has been divested with the sale of the Enterprise  | |                  |business to Zebra.                                          | |                  |( Motorola has a history of starting projects; bring them   | |                  |life, but never completing them. As a result of it, it      | |                  |currently operates in 2 instances of Oracle eBS in R12      | |                  |(Trilogy and OMAR, supporting the Order Management to       | |                  |Receivables cycle), 3 instances of Oracle 11i (supporting   | |                  |functions in EMEA, North America and Israel), and an        | |                  |instance in Oracle 10.7 Character Mode (supporting regulated| |                  |government business). The remaining IT environment          | |                  |supporting the Government business is old, complex and      | |                  |costly.  Furthermore, the current IT environment is managed | |                  |by multiple vendors, including TCS, CSC, and Deloitte.      | |                  |                                                            | |                  |Position -                                                 | |                  |Contribution My role in this project is to work on         | |                  |interfaces which are assigned to me.                        | |                  |Worked in Unit Testing on these objects and provide unit    | |                  |test case documents to functional team.                     | |                  |Developing Detail Design Document                           | |                  |Developed pl/sql interface related to check on hand quantity| |                  |from Service contracts module                               | |                  |Developing reports in XML Publisher                         | |                  |                                                            | |                  |                                                            | |                  |01/2015 - 12/2015                                           | |                  |12 months                                                   | |                  |IFFCO                                                       | |                  |-                                                           | |                  |Project Description Indian Farmers Fertilizer Cooperative  | |                  |Limited, also known as IFFCO, is the world’s largest        | |                  |fertilizer cooperative federation based in India which is   | |                  |registered as a Multistate Cooperative Society.             | |                  |Position -                                                 | |                  |Contribution ( Provide continuous support to the client’s  | |                  |production environment so that none of the production issues| |                  |violates SLA.                                               | |                  |( Analyze the production issue and provide solutions which  | |                  |may be a code fix, setup issue or data issue.               | |                  |( Direct communication with the business users with         | |                  |resolution of the issue post thorough analysis.             | |                  |( My role in this project is to resolve tickets which are   | |                  |assigned to me.                                             | |                  |( Worked in Unit Testing on these objects and provide unit  | |                  |test case documents to functional team.                     | |                  |                                                            | |                  |                                                            | |                  |01/2014 - 12/2014                                           | |                  |12 months                                                   | |                  |STC VIVA                                                    | |                  |-                                                           | |                  |Project Description Viva is a telecommunications company   | |                  |based in Bahrain. It is owned by Saudi Telecom Company      | |                  |Group.                                                      | |                  |This project is an implementation to Oracle R12.VIVA has    | |                  |engaged TCS as a partner to implement their EBS Suite       | |                  |environment R12.1.3.                                        | |                  |                                                            | |                  |Position -                                                 | |                  |Contribution ( My role in this project is to do develop the| |                  |objects.                                                    | |                  |( Developed interfaces and a XML Publisher reports.         | |                  |( Developed the MD70,MD120 documents for the objects        | |                  |handled.                                                    | |                  |( Worked in Unit Testing on these objects and provide unit  | |                  |test case documents to functional team.                     | |                  |( Understand MD60 which is the business requirement provided| |                  |by the functional analyst.                                  | |                  |( Prepare the MD70 which is the technical design document to| |                  |ensure that the solution and design is aligned with the     | |                  |requirement.                                                | |                  |( Design and develop multiple components like Interface,    | |                  |Conversion, Reports etc as mentioned in the MD60 and in line| |                  |with the design in MD70.                                    | |                  |( Participate in unit testing for the developed components. | |                  |( Participate in the integration testing and extend support | |                  |during the user acceptance test phase.                      | |                  |( Communicate activities/progress to project managers and   | |                  |technical lead.                                             | |                  |                                                            | |                  |                                                            | |                  |07/2013 - 12/2013                                           | |                  |6 months                                                    | |                  |Cigna Building Financial Foundations                        | |                  |-                                                           | |                  |Project Description Cigna is a global health service       | |                  |company dedicated to helping people improve their health,   | |                  |well-being and sense of security. This project is an        | |                  |implementation to Oracle R12.                               | |                  |Cigna has engaged TCS as a partner to implement their EBS   | |                  |Suite environment R12.1.3.                                  | |                  |                                                            | |                  |Position -                                                 | |                  |Contribution ( Developed 5 interfaces and a RDF report.    | |                  |( Developed the MD70 documents for the objects handled.     | |                  |( Worked in Unit Testing on these objects and provide unit  | |                  |test case documents to functional team.                     | |                  |                                                            | |                  |                                                            | |                  |03/2013 - 06/2013                                           | |                  |4 months                                                    | |                  |CHP_US_R12 UPGRADE                                          | |                  |-                                                           | |                  
# # #    |Project Description CHP has engaged Hitachi Consulting as a| |                  |partner to upgrade their EBS Suite environment from version | |                  |11i to R12.1.3.My role in this project is to do impact      | |                  |analysis of the objects and upgrade and migrate the custom  | |                  |objects                                                     | |                  |Position -                                                 | |                  |Contribution ( Worked in upgrading and migrating customs   | |                  |objects (SQL scripts, Pl/SQL scripts, RDF) from 11i to R12  | |                  |based on impact analysis.                                   | |                  |( Developed TAC (Technical Analysis of Changes) documents on| |                  |upgraded objects.                                           | |                  |( Worked in Unit Testing on these objects and prepare TE    | |                  |50(Unit Test Case) document on migrated objects and provide | |                  |to functional team.                                         | |                  |                                                            | |                  |                                                            | |                  |09/2012 - 01/2013                                           | |                  |5 months                                                    | |                  |PPGEurope UK _R12 Trial Migr1                               | |                  |-                                                           | |                  |Project Description PPG is a US based Company which        | |                  |manufactures paints, optical fibers etc. Established in     | |                  |1883, PPG makes protective and decorative coatings,         | |                  |sealants, adhesives, metal pre-treatment products, flat     | |                  |glass, fabricated glass products, continuous-strand fiber   | |                  |glass products, and industrial and specialty chemicals      | |                  |including photo chromic ophthalmic lenses, optical monomers,| |                  |silica’s and fine chemicals.                                | |                  |Position -                                                 | |                  |Contribution ( Worked in Unit Testing on these objects and | |                  |provide unit test case documents to functional team.        | |                  |( Development, Pl/SQL Packages.                             | |                  |( User Guide and Technical Documents preparation (MD70).    | |                  |                                                            | |                  |                                                            | |                  |01/2012 - 08/2012                                           | |                  |8 months                                                    | |                  |PPG Global AMS                                              | |                  |-                                                           | |                  |Project Description PPG is a US based Company which        | |                  |manufactures paints, optical fibers etc. We had to run the  | |                  |Invoice Print Programs and convert the generated PS files to| |                  |Pdf for the given batch source and date range and archiving | |                  |them to store electronically.                               | |                  |Position -                                                 | |                  |Contribution ( Development, Pl/SQL Packages and Shell      | |                  |script.                                                     | |                  |( User Guide and Technical Documents preparation (MD70).    | |                  |( Worked on Account Receivables Module.                     | |                  |                                                            | |                  |                                                            | |                  |03/2011 - 12/2011                                           | |                  |10 months                                                   | |                  |PPG CCDS Oracle Implementation project                      | |                  |-                                                           | |                  |Project Description Established in 1883, PPG Industries is | |                  |a leading diversified manufacturer that supplies its        | |                  |products and services around the world. PPG makes protective| |                  |and decorative coatings, sealants, adhesives, metal         | |                  |pre-treatment products, flat glass, fabricated glass        | |                  |products, continuous-strand fiber glass products, and       | |                  |industrial and specialty chemicals including photo chromic  | |                  |ophthalmic lenses, optical monomers, silica’s and fine      | |                  |chemicals. The project ‘CCDS to Oracle’ mission is to       | |                  |replace existing CCDS mainframe system with a more current, | |                  |flexible, and cost effective system. Make improvements to   | |                  |current business processes where possible. This project     | |                  |involved Data Migrations and Reports as part of Rollout     | |                  |Activities across Account Payables and Cash Management      | |                  |modules of Oracle Apps 11i                                  | |                  |Position -                                                 | |                  |Contribution ( Development, Enhancements and Customization | |                  |of reports, Pl/SQL Packages, Interfaces and Conversions.    | |                  |( Technical Documents preparation (MD70, CV 40).            | |                  |( Registered Custom Programs in applications defining       | |                  |Executables, Concurrent Programs, and Request Groups.       | |                  |( Worked on extraction scripts as part of project           | |                  |                                                            | |                  |                                                            | |                  |11/2010 - 03/2011                                           | |                  |5 months                                                    | |                  |Sherwin Williams                                            | |                  |-                                                           | |                  |Project Description The Sherwin-Williams Company (NYSE    | |                  |SHW) is an American Fortune 500 company in the general      | |                  |building materials industry. The company primarily engages  | |                  |in the manufacture, distribution, and sale of paints,       | |                  |coatings and related products to professional, industrial,  | |                  |commercial, and retail customers primarily in North and     | |                  |South America. The company is mostly known through its      | |                  |Sherwin-Williams Paints line.                               | |                  |This project involved Data Migrations and Reports as part of| |                  |Rollout Activities across Financials area of Oracle         | |                  |Applications for Vietnam and Singapore Sites                | |                  |                                                            | |                  |Position -                                                 | |                  |Contribution ( Development, Enhancements and Customization | |                  |of reports and Pl/SQL Packages.                             | |                  |( Technical Documents preparation (MD70, MD120).            | |                  |( Registered Custom Programs in applications defining       | |                  |Executables, Concurrent Programs, and Request Groups.       | |                  |( Worked on extraction scripts as part of project           | |                  |                                                            | |                  |                                                            | |Prior Experience  |01/2016 - 04/2016                                           | |                  |4 months                                                    | |                  |Motorola                                                    | |                  |Motorola                                                    | |                  |Project Description • MSI was a $10B business that was in  | |                  |the process of a corporate IT transformation to consolidate | |                  |their ERPs and move to single instance of Oracle eBS R12.   | |                  |The majority of the completed transformation effort (called | |                  |Trilogy) has been divested with the sale of the Enterprise  | |                  |business to Zebra.                                          | |                  |• Motorola has a history of starting projects; bring them   | |                  |life, but never completing them. As a result of it, it      | |                  |currently operates in 2 instances of Oracle eBS in R12      | |                  |(Trilogy and OMAR, supporting the Order Management to       | |                  |Receivables cycle), 3 instances of Oracle 11i (supporting   | |                  |functions in EMEA, North America and Israel), and an        | |                  |instance in Oracle 10.7 Character Mode (supporting regulated| |                  |government business). The remaining IT environment          | |                  
# # #    |supporting the Government business is old, complex and      | |                  |costly.  Furthermore, the current IT environment is managed | |                  |by multiple vendors, including TCS, CSC, and Deloitte.      | |                  |• My role in this project is to work on interfaces which are| |                  |assigned to me.                                             | |                  |Contribution • Work on Interfaces which are assigned to me.| |                  |Worked in Unit Testing on these objects and provide unit    | |                  |test case documents to functional team.                     | |                  |                                                            | |                  |                                                            | |                  |01/2015 - 12/2015                                           | |                  |12 months                                                   | |                  |IFFCO                                                       | |                  |IFFCO AMS                                                   | |                  |Project Description • Indian Farmers Fertilizer Cooperative| |                  |Limited, also known as IFFCO, is the world’s largest        | |                  |fertilizer cooperative federation based in India which is   | |                  |registered as a Multistate Cooperative Society.             | |                  |• My role in this project is to resolve tickets which are   | |                  |assigned to me.                                             | |                  |Contribution • Resolve tickets which are assigned to me.   | |                  |Worked in Unit Testing on these objects and provide unit    | |                  |test case documents to functional team.                     | |                  |                                                            | |                  |                                                            | |                  |01/2014 - 12/2014                                           | |                  |12 months                                                   | |                  |VIVA                                                        | |                  |STC VIVA                                                    | |                  |Project Description Viva is a telecommunications company   | |                  |based in Bahrain. It is owned by Saudi Telecom Company      | |                  |Group.                                                      | |                  |This project is an implementation to Oracle R12.            | |                  |VIVA has engaged TCS as a partner to implement their EBS    | |                  |Suite environment R12.1.3.                                  | |                  |My role in this project is to do develop the objects.       | |                  |                                                            | |                  |                                                            | |                  |Contribution Developed interfaces and a XML Publisher      | |                  |reports.                                                    | |                  |Developed the MD70,MD120 documents for the objects handled. | |                  |Worked in Unit Testing on these objects and provide unit    | |                  |test case documents to functional team.                     | |                  |                                                            | |                  |                                                            | |                  |07/2013 - 12/2013                                           | |                  |6 months                                                    | |                  |Cigna                                                       | |                  |Cigna Building Financial Foundations                        | |                  |Project Description Cigna is a global health service       | |                  |company dedicated to helping people improve their health,   | |                  |well-being and sense of security. This project is an        | |                  |implementation to Oracle R12.                               | |                  |Cigna has engaged TCS as a partner to implement their EBS   | |                  |Suite environment R12.1.3.                                  | |                  |My role in this project is to do develop the objects.       | |                  |                                                            | |                  |Contribution Developed 5 interfaces and a RDF report.      | |                  |Developed the MD70 documents for the objects handled.       | |                  |Worked in Unit Testing on these objects and provide unit    | |                  |test case documents to functional team.                     | |                  |                                                            | |                  |                                                            | |                  |03/2013 - 06/2013                                           | |                  |4 months                                                    | |                  |CHP                                                         | |                  |CHP_US_R12 UPGRADE                                          | |                  |Project Description CHP has engaged Hitachi Consulting as a| |                  |partner to upgrade their EBS Suite environment from version | |                  |11i to R12.1.3.My role in this project is to do impact      | |                  |analysis of the objects and upgrade and migrate the custom  | |                  |objects.                                                    | |                  |Contribution Worked in upgrading and migrating customs     | |                  |objects (SQL scripts, Pl/SQL scripts, RDF) from 11i to R12  | |                  |based on impact analysis.                                   | |                  |Developed TAC (Technical Analysis of Changes) documents on  | |                  |upgraded objects.                                           | |                  |Worked in Unit Testing on these objects and prepare TE      | |                  |50(Unit Test Case) document on migrated objects and provide | |                  |to functional team.                                         | |                  |                                                            | |                  |                                                            | |                  |                                                            | |                  |09/2012 - 01/2013                                           | |                  |5 months                                                    | |                  |PPG                                                         | |                  |PPG Europe UK _R12 Trial Migr1                              | |                  |Project Description PPG is a US based Company which        | |                  |manufactures paints, optical fibers etc. Established in     | |                  |1883, PPG makes protective and decorative coatings,         | |                  |sealants, adhesives, metal pre-treatment products, flat     | |                  |glass, fabricated glass products, continuous-strand fiber   | |                  |glass products, and industrial and specialty chemicals      | |                  |including photo chromic ophthalmic lenses, optical monomers,| |                  |silica’s and fine chemicals.                                | |                  |Contribution Development, Pl/SQL Packages.                 | |                  |User Guide and Technical Documents preparation (MD70).      | |                  |                                                            | |                  |                                                            | |                  |01/2012 - 08/2012                                           | |                  |8 months                                                    | |                  |PPG                                                         | |                  |PPG Global AMS                                              | |                  |Project Description PPG is a US based Company which        | |                  |manufactures paints, optical fibers etc. We had to run the  | |                  |Invoice Print Programs and convert the generated PS files to| |                  |Pdf for the given batch source and date range and archiving | |                  |them to store electronically.                               | |                  |Contribution Development, Pl/SQL Packages and Shell script.| |                  |User Guide and Technical Documents preparation (MD70).      | |                  |Worked on Account Receivables Module.                       | |                  |Registered Custom Programs in applications defining         | |                  |Executables, Concurrent Programs, and Request Groups.       | |                  |                                                            | |                  |                                                            | |                  |03/2011 - 12/2011                                           | |                  |10 months                                                   | |                  |PPG                                                         | |                  |PPG CCDS Oracle Implementation project                      | |                  |Project Description Established in 1883, PPG Industries is | |                  |a leading diversified manufacturer that supplies its        | |                  |products and services around the world. PPG makes protective| |                  |and decorative coatings, sealants, adhesives, metal         | |                  |pre-treatment products, flat glass, fabricated glass        | |                  |products, continuous-strand fiber glass products, and       | |                  |industrial and specialty chemicals including photo chromic  | |                  |ophthalmic lenses, optical monomers, silica’s and fine      | |                  |chemicals. The project ‘CCDS to Oracle’ mission is to       | |                  |replace existing CCDS mainframe system with a more current, | |                  |flexible, and cost effective system. Make improvements to   | |                  |current business processes where possible. This project     | |                  |involved Data Migrations and Reports as part of Rollout     | |                  |Activities across Account Payables and Cash Management      | |                  |modules of Oracle Apps 11i.                                 | |                  |Contribution Development, Enhancements and Customization of| |                  |reports, Pl/SQL Packages, Interfaces and Conversions.       | |                  |Technical Documents preparation (MD70, CV 40).              | |                  |Registered Custom Programs in applications defining         | |                  |Executables, Concurrent Programs, and Request Groups.       | |                  |Worked on extraction scripts as part of project             | |                  |                                                            | |                  |                                                            | |                  |11/2010 - 03/2011                                           | |                  |5 months                                                    | |                  |Sherwin Williams                                            | |                  |Sherwin Williams (Singapore) project                        | |                  |Project Description The Sherwin-Williams Company (NYSE    | |                  |SHW) is an AmericanFortune 500 company in the general       | |                  |building materials industry. The company primarily engages  | |                  |in the manufacture, distribution, and sale of paints,       | |                  |coatings and related products to professional, industrial,  | |                  |commercial, and retail customers primarily in North and     | |                  |South America. The company is mostly known through its      | |                  |Sherwin-Williams Paints line.                               | |                  |This project involved Data Migrations and Reports as part of| |                  |Rollout Activities across Financials area of Oracle         | |                  |Applications for Vietnam and Singapore Sites.               | |                  |                                                            | |                  |Contribution Development, Enhancements and Customization of| |                  |reports and Pl/SQL Packages.                                | |                  |Technical Documents preparation (MD70, MD120).              | |                  |Registered Custom Programs in applications defining         | |                  |Executables, Concurrent Programs, and Request Groups.       | |                  |Worked on extraction scripts as part of project  
# # # """
# # # # Ajay Kushvah Contact info +91 7417758111   ajay.kushvah@walkingtree.tech OBJECTIVE 3+ year of experienced quality engineering professional highly skilled overseeing the entire production while conducting product inspection as part of ensuring optimum quality. Proficient in understanding customer requirements and developing the entire quality control process by adhering to technical specifications. WORK EXPERIENCE Associate Software Engineer Walking Tree Technologies 15/09/2021 - 30/06/2022 Worked as SDET  for insurance domain- Indonesian/Goa Client. 21/07/2022- 20/09/2022 Worked as QA for insurance domain- Indonesian/Goa Client. 20/09/2022 - present Prepared the documentation and demo of the zap security tool. Working on IVYTech automation framework. Achievements / Taks Manual testing of Api using Postman. Api automation using restAssured and TestNG. Web automation using selenium and JAVA. Involving in Test planning, Requirement anaylsis, Test cases creation, designing manual and automation test plan/ Test cases, executed the test cases. Involving in End to End testing of features including in functional, non-functional, API and automation testing. Developing BDD script with cucumber and writing step defination using Gherkin based feature. Experienced in Agile and waterfall methodology. Experience in defect tracking tools like Jira and Redmine. Thorough experience in implementing RestAssured, TestNG, selenium webDriver, Intellij, Eclipse, Git/GitHub, Jenkins, REST with Postman, Slack, Winsap, ArgoCD. Having sound knowledge of My SQL and SQL. EDUCATION Hi-tech institute of technology, Ghaziabad — M.C.A(2022 -2024) pursuing Uttam institute of technology, Agra — B.C.A(2019 -2022) percentage- 83.0% St.Joseph, Agra — 12th( 2017 - 2019) percentage- 68.4% St.Vincent, Agra— 10th(2015 - 2017) percentage- 76.5% LANGUAGES English / Hindi SKILLS JAVA ,                        RestAssured Selenium             Cucumber TestNG                 Git/Github Mysql Manual Testing, Postman                        Jira Maven                  API Testing Slack Having knowledge of  Winsap    JEST                           SDLC Trained on Automation Testing, , Agile/ Waterfall Methodology Domain Insurance PROJECTS API Automation POC —2022 POSTMAN/ RestAssured(Both) with cucumber BDD framework API Testing using JEST Design the automation framework from scratch PROFESSIONAL PROFILES Linkedin Github HackerRank

# # # Resume Name Srikanth  +91-9059740302  srikanth40302@gmail.com Professional Experience Over 14+ of professional experience which includes 7+ years in to Non-IT (US Home Loans/Mortgage) and over 7 years in to IT (Data Warehousing experience using Ab Initio, Unix, SQL). Primarily involved in support projects of various banks of U.S.A. Good exposure with the client interaction as part of the business requirement. Managed team and their performance, publish reports, conduct meetings. Conducted trainings for new associates as per the project requirement. Publish status to the clients and management on weekly and monthly dashboard calls. Extensively used ETL methodologies for supporting data extraction, transformations and loading processing, in a corporate-wide-ETL Solution using Ab Initio. Excellent communication analytical skills, ability to work independently and good team player. Experience in data requirement gathering, client interaction, development, testing and support. Passion to learn and upskill and provide quality work, technical capability and good work ethics. Career History Company #1 Currently working at L&T Infotech from Oct’2021 till date. Client Name      Citi Bank Technologies Used    Ab Initio, SQL Server, UNIX. Period                  Oct’2021 to till date Role                     Senior Data Engineer. Description Citi bank is the primary U.S. banking subsidiary of Citigroup. The project, Global Liquidity reporting system deals with generation of regulatory reports that is needed by the regulators to evaluate a bank’s operations and its overall health, there by determining the status compliance with applicable regulatory provisions. Roles & Responsibilities . GLRS product support team is part of Global Liquidity reporting system ETL (Abinitio) support project. Handle a team of 4 associates to meet production support activities. As part of L3 support team we are responsible for maintaining the application’s data flow and Processing end to end data to the downstream process. Data quality issues are monitored and send the required observations to the upstream processes. Validation of the data and the required input would be provided to the users. Communicating with the clients/users to resolve the data quality issues. There are multiple products for which the regulatory data is received and liquidity report is produced. This report would be submitted to Local banking authorities to access the bank’s liquidity. We primarily use Abinitio for ETL processing with Control center and Autosys as scheduling tools. Data is loaded into Oracle DB which would reflect on Tableau and IFW (Internal tool) to the user for further analysis. Monitoring of the application data and control centre jobs, dataflow and its status. Scheduling the jobs as per the client requirements and report if there is any delays Advising the users to trigger the reports as on when we receive the required data. Hourly and daily checks are done to make sure that the applications are up and running and also to make sure the data is available. Company #2 worked at Cognizant Technology Solutions from June’2013 to till Oct’2021. Project #1 Client Name      TD Bank Technologies Used    Ab Initio, SQL Server, UNIX. Period                  Apr’ 2018 to Oct’2021 Role                     ETL Developer. Description TD bank is an American national bank. The project deals with generation of regulatory reports that is needed by the regulators to evaluate a bank’s operations and its overall health, there by determining the status compliance with applicable regulatory provisions. Roles & Responsibilities . Participating in daily and weekly meetings to provide the process status. Monitoring the daily jobs and notifying team members about the delays as part of support team. Creating Incidents if there are any delays or data quality issues that we receive from the downstream process and assign it to responsible teams. Following up with the team on the open issues and make sure they are closed within timelines. Collating of the open issues and provide the status to the management for reporting. Closing of the resolved issues in the incident application once we get the confirmation from the user. Feed delays and process status are reported to the clients on daily basis at end of the day. Review data quality issues and data missing issues that are raised from the downstream process and provide clarification to them and route them to upstream process for further research. Helping users to pull reports and help clear any reports that are in struck/pending status. Reviewing the code and running the same in Graphical Development Environment (GDE) to check for any failures and status. Monitoring of extraction, transformation and loading of the data from the legacy systems using Ab Initio to Oracle DB. Developed a good understanding of existing business requirements and also questioned requirements when needed. Project #2 Client Name       Key Bank Title       SVoC (Single view of customer) Technologies Used    Ab Initio, UNIX. Period                  May’ 2017 to Mar’ 2018 Role                     ETL Developer. Description Key Bank, the primary subsidiary of KeyCorp, is a regional bank headquartered in Cleveland and is the only major bank based in Cleveland. Key Bank is 29th on the list of largest banks in the United States. Key's customer base spans retail, small business, corporate, and investment clients. Now we are implementing SVoC (Single view of customer). Here we are integrating the various modules data like CC (Credit Card) CASL (Current, Savings and Loan Accounts) ,SVoC is very useful for the frontend application level and Customer also can use all products under One application. Roles & Responsibilities Involved in designing and developing of graphs in Ab Initio. Developed graphs using Graphical Development Environment (GDE) with various Ab Initio components. Ab Initio graphs were developed using various components such as Sort, Lookup, Filter by Expression, Sort to facilitate loading from source to Target. The components used depend upon the various business requirements. Developed adhoc graphs to serve the instant requests from the business. Participating ETL design phase and creating ETL Design Specs for mappings. Developed graphs to extract data needed from the source databases by using input and output files. Support has been provided to the users and worked on data quality issues. Project #3 Client Name      Mr. Cooper Home Loans Period                  June’ 2013 to Apr’ 2017 Role                     Subject Matter Expert. Roles & Responsibilities Handled a team of 7 members and conducting trainings on the process when a new update rolls out. Publishing performance reports to the team and conducting one to one discussions with them on monthly basis. Responsible for conducting the training of new joiners in conjunction with L&D team train and coach the new joiners. Providing status to the clients on weekly and monthly dashboard calls. Responsible for identifying the under-performing employee's basis the benchmarks and areas of development. Providing feedback and motivating them. Claim filing team is the one of the post sale processes. Receives Inventory from Onshore. We gather all the necessary documents/invoices and information that is required to file the expenses reports, update the amounts paid in reconciler. Filing includes Initial, Supplemental and Final claims in LPS and Vendors cape systems. Taking the responsibility of each & every claim till it is fully paid by the Investor. A resubmission of the claim is done based on the Investors comments in the claim filing system. Consolidating and sharing the utilization reports and monthly business review reports to the higher management to know the current status of the process. Company #3      Bank of America Client Name      FNMA- Federal National Mortgage Association Period                  Dec’ 2009 to May’ 2013 Role                     Senior Team Member. Roles & Responsibilities Taking the responsibility of each & every claim till it is fully paid by the investor. Following up with the attorneys & Taxing Authorities for the adequate information to make sure the claim is fully paid. Preparing data consolidation to ensure the associates data is correct. Spoc for preparing and publishing the ageing reports to control the inflow and to prevent any TAT miss. Acting as transport spoc for the team (Rostering daily pickup/drop facility). Preparation and balancing of claim worksheet and dump these expenses in claim filing system. Ensure to contact correct vendors for any missing supporting documentation. Conducting weekly meet with all the team members. Actively participated in client interaction during weekly calls and maintain good rapport with onshore team.
# # # ARRAKRISHNAMRAJU EMAIL       krishnamrajuerra@gmail.com MOBILE   +91-8019455504 A highly skilled and well-seasoned IT professional with over 5.1 years of experience in the areas of service and support, Implementation, Administration on WebSphere MQ and WebSphere IIB. Professional Summary Having experience in installing & configuring MQ Series on various environments like Linux. Created and modified MQ objects such as Queue Managers, channels and queues. Implementing Distribution Communication Clustering Communication over different platforms. Enabled WebSphere MQ Triggering on the queues like Channel Triggering and Application Triggering. Experience in configuring and monitoring MQ Listeners, Command Servers, Channel Initiators, Trigger Monitors & Dead Letter Queues. Good knowledge on MQ Authentication concepts like ACL and OAM. Having experience in Granting and Revoking permissions to users as well as groups. Deploying the bar files as per the application requirements. Created Channels to connect from WMQ Client to WMQ Server. IBM WebSphere MQ Series related troubleshooting and Bug Fixing. Handling Incident tickets and Service tickets on the ticketing tools. Configured the cluster mechanism on for workload balancing. Having experience on reload and restart execution group, as well as start and stop the message flows in IIB. Hands on experience in up gradation & migration in various platforms like LINUX. Raising an incident and service request to the application teams, as per our requirements. Configured and implemented Distributed Queuing on Client/Server architectures. Hands on experience on Problem determination, Trouble shooting, backup and recovery. Having knowledge on SSL related concepts for WebSphere MQ. Worked with 24x7 Production control support and on-call support. ACADEMIC BACKGROUND Master of Computer Application from KAKATHIYA UNIVARSITY Technical Skills Integration Tools      IBM Web Sphere MQ  V 7.5, V 8.2, V 9.2 Operating Systems   Linux and Unix Work experience Currently working with Accenture  as WebSphere MQ Administrator from  October 2020- Till date. Worked with TCS as Middleware Administrator from June 2018- August 2020. Project#2 Client                    Santander Banking Group Duration              November 2020 – Till date Organization      Accenture Location              Hyderabad Description  The Santander Group is a Spanish banking group centred on Banco                    Santander, S.A. and is the largest bank in the Eurozone by market value. It is one of the largest banks in the world in terms of market capitalization. It originated in Santander, Cantabria, Spain. The group has expanded in recent years through a number of acquisitions, with operations across Europe, Latin America, North America and Asia. Many subsidiaries have been rebranded under the Santander name. In April 2013, Santander was ranked as 43rd in the Forbes Global 200 list of the world’s largest companies. Responsibilities Installation of WMQ on Linux and working with IIB. Creating and Configuring MQ objects like Queue managers, local queues, remote queues, transmission queues, dead letter queues, channels, listeners. Worked on Distribution setup and cluster environment. Enabled WebSphere MQ Triggering on the queues like Channel Triggering and Application Triggering. Experience in configuring and monitoring MQ Listeners, Command Servers, Channel Initiators, Trigger Monitors, MQ Log files & Dead Letter Queues. Implemented Workload balancing. Experience in deploying barflies into execution groups. Good experience on creation and deletion of broker. Experience on starting and stopping message flows. Worked on SSL setup. Implementing Distribution Communication and Clustering Communication over different platforms. Having experience in granting and revoking the Permissions to users. Project#1 Client                    First Horizon National Corp Duration               June 2018 – August 2020 Organization       TCS Location               Hyderabad Description First Horizon National Corp is a bank holding company providing regional banking, capital markets, national specialty lending, mortgage banking and corporate-banking services through First Tennessee Bank NA and other subsidiaries. Based in Memphis, Tennessee, the company has 200 business locations in 15 states as well as in Hong Kong and Tokyo. The company embraced local banking and adopted a go-it-slow approach after retreating from a national push into mortgage lending several years ago. Responsibilities  Installation of Web Sphere MQ on Linux. Creating and configured MQ objects like Queue managers, local queues, remote queues, transmission queues, dead letter, channels,      listeners. Participation in distribution setup. Setup triggering for both channels and applications. Configured repository Queue managers in cluster environment. Set MQ clustering for workload balancing and simplify the administrative tasks. IBM MQ Series related troubleshooting and Bug Fixing. Experience on Web Sphere Message Broker Administration. Implemented SSL for SDR & RCVR channels to provide security. Good experience on creation and deletion of Broker. Raising an incident and service request to the application teams, as per our requirements. Configured cluster environments. Monitoring queues, channels and listeners. Experience in deploying barflies into execution groups. Provided 24x7 support on rotation basis for MQ for application issues. Supported MQ and Linux during off hour rotation. (Arra KrishnamRaju)
# # # KANKANALA RAMESH REDDY kankanala.rameshreddy@gmail.com Contact No+91-8008273607 Profile Having 4 years of experience in WebSphere MQ/MB Administrator Production support and Administration in fields. Experience Summary Having Good hands-on experience in Administration and Configuration of WebSphere MQ v 7.0 and v 7.5.1,v 8.0, v 8.1, v 8.5 , v 9.1.0.5, v 9.2 on different environments like Windows, Linux , AIX. Create the necessary IBM Web Sphere MQ objects to support an application. Supported several Queue Managers and servers of different platforms. Good experience with MQSeries Distributed Queuing, Clustering with workload sharing and implementing Security. Co-ordinate with Application team to resolve problem. Experience in configure and monitor MQ Listeners, Command Servers, Channel initiators, Trigger Monitors, MQ Log files & Dead Letter Queues. Good experience in Problem determination, troubleshooting, Queue Manager backup & recovery. Windows patching activities with Wintel team Involving with DR activities Raised PMR with IBM. Extensively working on broker related Stop & start flows, reload EG groups from commands. Deploy BAR files through toolkit and from command prompt Hands on experience in creation of execution groups. Hands on experience in BAR file deployments. Hands on experience in start and stop of message flow and reload of execution groups. Hands on experience in start and stop of Brokers and queue managers. Technical Skills Operating Systems Windows, UNIX (Linux, Solaris). Middleware IBM Web Sphere MQ Series Administration. IBM Message Broker Administration. Tools and Utilities MQ Explorer on Windows and Linux Client Tools Putty, WinSCP, RFHUtil Ticketing Tool Service now Education Qualifications Completed Engineering from JNTUH University with aggregate of 68.4% in may 2018. Completed Intermediate Public Examination from Alphores Junior College with aggregate of 87% in 2014. Completed Secondary School  from Valmeeki Vidyalayam High School with 7.8 GPA in 2012. Professional Experience Working as an MQ Administrator in Tech Mahindra from DEC 2019 to till date. Project-2 Client                AGN (Allianz Global Network) Role                 MQ Admin Duration           JUNE 2022 to Till Date. Environment  IBM MQSeries 7.X, 8.0, 8.1, 8.5, 9.1.0.5, 9.2 Linux. Project Description Allianz Global Network (AGN) is one of the core Allianz IT global initiatives. It is designed to consolidate, standardize, upgrade, and optimize the IT data and voice network services and thereby improve the working environment of the more than 150,000 Allianz employees worldwide. In simple terms, it is providing the basic plumbing for many of the other initiatives. At present, a wide variety of local networks are used which are not always interconnected or even compatible. Implementing a standardized global network will create the necessary IT platform for worldwide cooperation within Allianz. This will open the door for high quality, end-to-end reliable data, and voice services, such as internet telephony or video conferencing, on a global scale. Roles &Responsibilities Configured MQ Series queue managers, clusters, and queue manager objectsi.e., queues, channels etc. Installation and configuration of WebSphere MQ V7.X. Established communication between MQCLIENT and MQSERVER. Working with Security team in granting the permissions for WMQ. Configured WebSphere MQ Queue Managers, Queues, and Channels etc. Extensive experience on configuration and monitoring the MQ Listeners, channel initiators, Trigger Monitors, MQ Log files and Dead Letter Queues. Performing the Daily bases Build verification test cases and maintaining the performance-based issues. Change Management for the scheduled Applications on production. Prepare the design document for the current and future design. Administered the Message Broker artifacts like Message Flows, Message Set and Execution Groups. Deploying the Message Flows, Messages Sets and Execution Groups to Brokers in Different Environments (Test and Production). Monitoring of the queues and channels that needs to be up 24X7 for critical business critical applications and supporting clients. Active participant in monitoring the middleware and Perform daily on call tasks (checking error logs, fail over queues, System Logs, backed out messages) to maintain a healthy system. Handling and Troubleshooting of undelivered Messages by working with dead letter queues. PROJECT #1 Client      Sun Corp Group Role      MQ Admin Duration   DEC 2019 to MAY 2022 Environment   IBM MQSeries 8& 9x. Linux. Project Description The Sun Corp Group is one of the major financial service providers of Queens Land, Australia. Insurance and banking are the major services provided by the Sun Corp group. The Sun City project is a combined project of the Sun Corp Group and the Citi Bank, which aims at overcoming the credit card service, issues between the partners. Roles & Responsibilities Implemented distributed queuing client/server architectures and configured MQ. Configured MQ Series queue managers, clusters and queue manager objective, queues, channels etc. Gathering Requirements from the application teams. Configured WebSphere MQ Queue Managers, Queues, and Channels etc. Configuring the cluster mechanism for workload balancing and integrity of messages. Created MQ objects on local and remote MQ servers. Enabled Triggering on MQ Queues. Created Channels to connect from WebSphere MQ Client to WebSphere MQ Server. Involved in MQ Backup and Recovery process. Installation and configuration of WebSphere MQ V6.X, V7.X Extensive experience on configuration and monitoring the MQ Listeners, channel initiators, Trigger Monitors, MQ Log files and Dead Letter Queues. Worked with 24x7 Production control support. Handling and Troubleshooting of undelivered Messages by working with dead letter queues.
# # # Baji                                        Email-bajibaba441@gmail.com Ph +91  9390976990 SUMMARY OF EXPERIENCE - Over all 4.3 years of experience in the IT Industry on middleware Technologieson development, implementation and maintenance of  WebSphere MQ AND MB. Experince in Administration of  IBM Websphere MQ 7.0x,8.0x, and 9.0x and IIB onRed Hat Linux   and Windows XP/2003 environment. Experienced in Installation and configuration of MQ Client / MQ Server in different environments and MQ System Administration. Install of MQ and Message Broker and configuring WebSphere MQ in development and test environments. Ability to administer the message objects associated with all WebSphere MQ objects such as Queues, Process Definitions, Channels and Listeners. Active participant in monitoring the middleware and Perform daily on call tasks (checking error logs, Fail over queues, System Logs, Backed out messages) to maintain a healthy system. Hands on experience in MQ series triggering, Channel Initiator, SSL certificates, Dead letter queue configuration and distributed queuing. Experienced in setting up WebSphere MQ distributed queuing environment. Experienced in setting MQ clustering Environment. Working on critical and major alerts of the production servers Daily health check of the production servers. Experienced in setting up application triggering in WebSphere MQ. Experienced in monitoring and defining MQ objects in Mainframe environment. Having Good skills of Troubleshooting on WebSphere MQ  7.5,7.0 and 6.0. Supported hundreds of Queue Managers and several serverson different platforms. Participated in Change Management/Incident management meetings and Client meetings. Very fast in adapting to a changing work environment and very good in working in high pressure and tight deadline requirements. TECHNICAL SKILLS Middleware technologies      IBM MQSeries V7.0x, &8.0 and 9.0x AND IIB 10V. Operating Systems  Windows, RHEL,Putty & Winscp. Incident  Management  Tool       Service Now . Monitoring tool    MQExplorer. Alerting tool                                    Qpasa . EDUCATION Graduation from Narasaraopet institute of pharmaceutical sciences , Narasaraopet in 2019. WORK EXPERIENCE Currently Working in TCS , Chennai  from  April  2019 to till now PROJECT SUMMARY PROJECT- Project                    Virgin atlantic airways. Role     Middleware Adminisrator. Tools                       Service Now Ticketing Tool. Duration                April 2019 to till now. About client- Virgin Atlantic Airways Ltd (Virgin Atlantic), a subsidiary of Virgin Group Ltd, is a British airlines company that provides domestic, international flight, and other services. It also offers holiday packages and cargo services. Virgin Atlantic uses a mixed fleet of Boeing and Airbus for carrying passengers across North America, Africa, the Middle East and Asia, and the Caribbean. The company’s cargo business connects manufacturers, consumers, and retailers across 100 countries. It also offers daily services to China, Africa, the Caribbean, Australia and Hong Kong. The company offers holiday packages to 46 destinations. Virgin Atlantic is headquartered in Crawley, West Sussex, the UK. Roles & Responsibilities- Installation of Web Sphere MQ, 7.0,8.0 and 9.2. on different Environments like, Linux, and Windows Systems. Creation and Management of MQ objects such as Queues, Channels, Process definitions, Listeners. Performed administrative tasks using MQSC commands. Setting up of trigger definitions (both for channels and application queues). Setting up of Distributed Queuing and management. Creating new Queue Managers on UNIX and Windows systems with appropriate logging and file system sizing parameters. Backing up of queue managers, logs and its object definitions and performing recovery. Involved in packaging and deploying BAR files. Recreation of damaged MQ objects using commands. Fixing channel problems such as uncommitted messages, channel retry issues, sequence number mismatch issues. Provide On-Call support in case of critical issues in Production Environment, which will be handled over a bridge/conference line with an SLA of 4 hours. Participated in design/development/Infrastructure build meetings. Install and Configure MQ on new servers per request by applications. Enabled Triggering on the Queues for monitoring and automation. Fixing issues based on MQ return codes such as Queue full, authority issues, data format etc., Co-ordination with application teams in designing applications to use MQ. Closely worked with developers in Environment design & Architecture, configuration, deployments & troubleshooting of MQ issues. Taking ownership on any issues with Message Broker on PRODUCTION and NON PRODUCTION Servers. 24x7 support, best practice trouble shooting, monitoring, capacity planning and maintenance. Using MQSC Commands performed administration tasks. Active participant in monitoring the middleware and Perform daily on call tasks (checking error logs, Fail over queues, System Logs, Backed out messages) to maintain a healthy system. Used to take MQ Backup & Recovery process in regular time intervals. Successfully migrated MQ7.0 to MQ 7.5 in almost 200 hostes across all platforms.
# # # """
# # user_message = f"""{pad_ocr}"""

# # messages =  [
# #             {'role':'system',
# #             'content': system_message},
# #             {'role':'user',
# #             'content': f"{delimiter}{user_message}{delimiter}"},
# #             ]
# # chat_completion = openai.chat.completions.create(
# #     model="mistralai/Mixtral-8x7B-Instruct-v0.1",
# #     messages=messages,
# #     temperature=0.0,
# #     max_tokens=None,
# #     top_p = 1,
# #     frequency_penalty=0
    
    
    

# #     )
# # #print(chat_completion)
# # print(chat_completion.choices[0].message.content)


# # # print(system_message)
# # # print(f"{delimiter}{user_message}{delimiter}")
# # # response = get_completion_from_messages(messages)
# # # pad_ocr = pad_ocr.replace('\n', '\\n')
# # # response = response.replace('\n', '\\n')
# # # system_msg = system_message.replace('\n', '\\n')
# # #print("Lenth of Tokens fed to LLM:{}".format(len(messages)))
# # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
# #         #print(response)

# #     # except Exception as e:
# #     #     print(f"Error processing file {pdf_file}: {str(e)}")


# # Assume openai>=1.0.0
# from openai import OpenAI
# import os
# from datetime import datetime
# import os
# from glob import glob
# import numpy as np
# import pandas as pd
# from PyPDF2 import PdfReader
# from groq import Groq
# current_date = datetime.now().strftime("%Y-%m-%d")

# import textract
# from docx import Document

# def extract_text_from_doc(doc_filename):
#     # try:
#     doc = Document(doc_filename)
#     text = ''
#     for paragraph in doc.paragraphs:
#         text += paragraph.text + '\n'
#     return text

# def extract_text_from_docx(docx_file_path):
#     try:
#         # Extract text from the DOCX file
#         text = textract.process(docx_file_path)
#         # Decode the extracted text (assuming UTF-8 encoding)
#         text = text.decode('utf-8')
#         print("Text extraction successful!")
#         return text
#     except:
#         text = extract_text_from_doc(docx_file_path)
#         #print(f"Error occurred: {e}")
#         return text

# # Example usage:
# docx_file_path = r"/home/walkingtree/Downloads/Naukri_divya[12y_0m].doc"
# extracted_text = extract_text_from_docx(docx_file_path)
# if extracted_text:
#     print(extracted_text)



# #TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")

# # Create an OpenAI client with your deepinfra token and endpoint
# client = Groq(
#     api_key="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",
# )


# delimiter = "####"
# system_message = f"""<s>[INST]
# Today's Date: {current_date}
# **Task** - You are an experienced and very helpful job resume parser. Given the resume text delimited by {delimiter}, \
# your goal is to analyze the resume and extract all given attributes.

# **Procedure**
# 1. Rearrange the entire resume first for better resume attribute extraction. 
# 2. All the below attributes are crucial, please provide output for as many attributes possible.
# 3. Rearrange and filter the text further for better resume attribute extraction.
# 4. Provide "N/A" when corresponding attribute info is not provided.
# 5. Please extract ALL the following attributes using the given names ONLY, ensure consistent format :-
# First Name:
# Last Name:
# Email ID: provide email id separated by commas
# Mobile number: comma-separated for 2 numbers
# Location: current city, state
# Permanent Address:Full Address with all info
# Date of Birth:date of birth in mm/dd/yyyy
# Marital Status:"Married" or "Not Married"
# Designation:Latest Designation of Person
# Company:Latest Company name of Person
# Experience: Parse the entire text. Please list the candidate's professional experiences within corporate environments. Determine the total years of corporate work experience as of today's data : {current_date}, excluding education, personal projects, or internships. Share the numerical value representing the total corporate work experience.
# Education:return latest education of a person
# Qualification:department or major of latest education
# Education Institute:where the person pursued the latest degree
# Marks in percentage:percentage or gpa person scored in latest education degree with unit
# Specialization:
# Year of passing:from the latest education degree
# Primary Skills: Begin by thoroughly parsing the entire resume. Please provide comprehensive list of skills by extracting all programming languages, every technical skills, all coding languages, every coding/technical frameworks candidate has worked with in the text. Please provide your findings in the form of a detailed list.
# Secondary Skills: Any other acquired skills which are not mentioned in primary skills or other attributes
# Job Title:title of current job/designation
# Job description:summarized description of the current job in 3 sentences(max 50 tokens)
# Company Location:Current company location of a person
# Industry:IT or Health or Hardware or Software industry e.t.c
# Headline: Resume Main Experience Headline of the Person
# Employment type:Full Time or Part Time of a person
# Date of joining:joining date in latest company in "dd/mm/yyyy"
# Last date: extract last working date of latest work experience and return in "mm/yyyy" 
# Current CTC:return 0 if not present
# Expected CTC:return 0 if not present
# Current Employment Status: check Last employment date against Today's date, or check current working status mentioned in the text, return "working" if employee is presently working, else "not working"
# Prefered Location:prefered job locations of a person
# Ready to relocate:"Yes" if candidate is open to relocation else "No" if candidate is Not Open to Relocation.
# Overseas Experience:Do person work experience span multiple countries? Please indicate with a simple True or False.
# Notice Period: If candidate has specifically provided this information, please return value in number of days
# Having Passport:Do person have a valid passport? Please indicate with a simple True or False.
# Passport Validity:return the validity of a passport
# Visa:True or False
# About:Absolutely Mandatory field. Generate a short summary of the profile in less than 50 tokens

# 6. Make an effort again to extract info for all attributes marked as "N/A", if you cannot, mark as "N/A". Thank YOU.
# [/INST]
# """

# # pdf_files = glob('Dix*.pdf')

# # # Loop through each PDF file
# # for pdf_file in pdf_files:
# #     try:
# #         pad_ocr = []
# #         print(f"Processing file: {pdf_file}")
# #         # Convert PDF to images
# #         #print(pdf_file)
# #         reader = PdfReader(pdf_file)
# #         #print(len(reader.pages))
# #         # Loop through each page of the PDF
# #         for i, page in enumerate(reader.pages):
# #             print("Page number is ", i + 1)
# #             text = page.extract_text()
# #             #print(text)
# #             pad_ocr.append(text)

# #         pad_ocr = "\n".join(pad_ocr)

#         #print(pad_ocr)


# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
# # pad_ocr = extracted_text
# # pad_ocr = " ".join(pad_ocr)
# # print(pad_ocr)
# # Run llm (assuming messages is defined)
# user_message = f"""{extracted_text}"""

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
# #print(chat_completion)
# print(chat_completion.choices[0].message.content)


# # print(system_message)
# # print(f"{delimiter}{user_message}{delimiter}")
# # response = get_completion_from_messages(messages)
# # pad_ocr = pad_ocr.replace('\n', '\\n')
# # response = response.replace('\n', '\\n')
# # system_msg = system_message.replace('\n', '\\n')
# #print("Lenth of Tokens fed to LLM:{}".format(len(messages)))
# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
# #print(response)

#     # except Exception as e:
#     #     print(f"Error processing file {pdf_file}: {str(e)}")


from openai import OpenAI
import os
from datetime import datetime
import os
from glob import glob
import numpy as np
import pandas as pd
from PyPDF2 import PdfReader
from groq import Groq
import json
current_date = datetime.now().strftime("%Y-%m-%d")

# def string_to_dict(s):
#     try:
#         # Try parsing as JSON
#         return json.loads(s)
#     except json.JSONDecodeError:
#         # If parsing fails, it means it's not in JSON format
#         # Split the string by commas and colon to get key-value pairs
#         pairs = [pair.split(':') for pair in s.split(',')]

#         # Strip whitespace and remove quotes
#         pairs = [(key.strip().strip('"'), value.strip().strip('"')) for key, value in pairs]

#         # Check for empty or whitespace-only values
#         for i, (key, value) in enumerate(pairs):
#             if value == "['']" or value.isspace():
#                 pairs[i] = (key, ' ')

#         # Convert to dictionary
#         return dict(pairs)

# def string_to_dict(s):
#     try:
#         # Try parsing as JSON
#         return json.loads(s)
#     except json.JSONDecodeError:
#         # If parsing fails, it means it's not in JSON format
#         # Split the string by commas (remove trailing comma if present)
#         pairs = [pair.strip() for pair in s.rstrip(',').split(',')]

#         # Split each pair by the first occurrence of colon (if present)
#         pairs = [(key.strip().strip('"'), value.strip().strip('"')) if ':' in pair else (key.strip().strip('"'), '') for key, value in (pair.split(':', 1) for pair in pairs)]

#         # Check for empty or whitespace-only values
#         for i, (key, value) in enumerate(pairs):
#             if value == "['']" or value.isspace():
#                 pairs[i] = (key, ' ')

        # Convert to dictionary
        # return dict(pairs)

# def string_to_dict(s):
#     try:
#         pairs = s.split(',')
#         pairs = [pair.split(':', 1) for pair in pairs]
#         return {key.strip().strip('"'): value.strip().strip('"') if value else '' for key, value in pairs}
#     except Exception as e:
#         print("Error occurred:", e)


# client = Groq(
#     api_key="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",
# )

# delimiter = "####"
# system_message = f"""<s>[INST]
# Today's Date: {current_date}
# You are a corporate recruitment specialist. Given an input text or query delimited by {delimiter}, please extract the below requested information JSON format.
#     Please extract the following information in a consistent format using the given names ONLY:
#     - firstName:extract First Name from text if present else return an empty string e.g:""
#     - lastName:extract Last Name from text if present else return an empty string  e.g:"" 
#     - phone_no:extract Mobile number from text if present else return an empty string  e.g:""
#     - current_location: return all locations where person could be living else return an empty list  e.g:[] 
#     - primary_skill: return all the skills mentioned else return an empty list  e.g:[]
#     - current_company: return all the company name from text else return an empty list e.g:[]
#     - current_designation: return all the designation name from text else return an empty list e.g:[]
#     - notice_period: return the notice period information from the text if provided, else emty string . Specify whether it's '$lt,' '$gt,' or just a certain number of months ,return in the format to filter in the MongoDB.
#     - experience: Extract the years of experience information from the text in json. If the experience is in months, do not return any number. If the experience is specified in years, return the number of years in the format to filter in MongoDB, including whether it is $lt (less than), $gt (greater than), or just a certain number of years.
#     if multiple Locations or Primary Skills or Company add in single json.
#     Example JSON if text present: 
#         "firstName": firstName in the format of string,
#         "lastName": lastName in the format of string,
#         "phone_no": phone_no in the format of string,
#         "current_location": current_location in the format of list of strings e.g ["Hyderabad", "Bangalore, "Chennai"],
#         "primary_skill": primary_skill in the format of list of strings e.g ["Python","Java","Html","css"],
#         "current_company":current_company in the format of list of strings e.g ["TCS","Infosys","Microsoft","Google","Walking Tree Technologies"]
#         "current_designation": current_designation in the format of list of strings e.g ["Software Engineer","Data Scientist","Data Engineer","Devops Engineer"]
#         "notice_period":'$eq 4' or '$lt 2' or '$gt 1' or 2 or '$eq 6.5' or '$lt 1.5' or '$gt 10.5' or 2.5
#         "experience":'$eq 3' or '$lt 6' or '$gt 8' or 6 or '$eq 10.5' or '$lt 7.5' or '$gt 5.5' or 1.5 ensure in JSON format.e.g:{"gt":4} or {"lt":7.9} or {"eq":6}

#     **Please provide only output, no explanation needed.**    

#     """

# user_message = """
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

# messages =  [
#                 {'role':'system',
#                 'content': system_message},
#                 {'role':'user',
#                 'content': f"{delimiter}{user_message}{delimiter}" + """\nAdhere to all instructions and extract all attributes accurately providing clean formatting...Thank you.. [/INST]"""},
#                 ]


# chat_completion = client.chat.completions.create(
#     model="mixtral-8x7b-32768",
#     messages=messages,
#     temperature=0.0,
#     max_tokens=None,
#     top_p = 1,
#     frequency_penalty=0.0            
#     )
# response=chat_completion.choices[0].message.content
# if 'Note:' in response:
#     response=response[:response.find("Note:")]

# print("The assistant suggests: ", response)
# json_dict = json.loads(response)

# print(json_dict)
# # # print(eval(response))
# # # print(json_dict)
# print(type(json_dict))
# # # if response.get("current_company", ' ') == ['']:
# # #     current_company=''
# # # else:
# # #     current_company=response.get("current_company", ' ')
# # # print("current_company==========================>",current_company)



# print(json_dict.get("experience", ""))
# print(type(json_dict.get("experience", "")))
