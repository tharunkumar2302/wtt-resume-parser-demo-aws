import schedule
import time
import threading
from app import resume_selection
from logger import logging
# from feedbackDetails import main
from app import textExtractionFromResume
import os
import glob
# from feedbackDetails import feedback_fun
class ResumeParser(object):
    def __init__(self,resume,filepath):
        self.details = {
            'createdAt': None,
            'updatedAt': None,
            'firstName': None,
            'lastName': None,
            'email': None,
            'phone_no': None,
            'current_location': None,
            'present_address': None,
            'date_of_birth': None,
            'marital_status': None,
            'current_designation': None,
            'current_company': None,
            'experience': None,
            'education': None,
            'education_details': None,
            'primary_skill': None,
            'secondary_skill': None,
            'experience_details': None,
            'status': None,
            'uploaded_by': None,
            'source': None,
            'organization': None,
            'createdByUserId': None,
            'modifiedByUserId': None,
            'createdByUserRole': None,
            'modifiedByUserRole': None,
            'current_ctc': None,
            'expected_ctc': None,
            'current_employment_status': None,
            'industry': None,
            'prefered_location': None,
            'ready_to_relocate': None,
            'overseas_experience': None,
            'isActive': None,
            'notice_period': None,
            'having_passport': None,
            'passport_validity': None,
            'visa': None,
            'About': None,
            'is_cv_uploaded':True,
        }
        self.resume = resume
        self.filepath=filepath
        self.get_details()

    def get_extracted_data(self):
        return self.details

    def get_details(self):
        self.details=textExtractionFromResume(self.resume,self.filepath)
        
def resume_parser():
    try:
        logging.info(f"Entered into resume_parser function")
        start_time=time.time()
        status=resume_selection()
        end_time=time.time()
        logging.info(f"Extraction completed")
        logging.info(f"Time taken to process all resumes is ==>{end_time-start_time}")
        return status
    
    except Exception as msg:
        print(msg)
        pass
    

if __name__ =='__main__':
    # resume_parser()
    # schedule.every().monday.do(feedback_fun)
    schedule.every(10).seconds.do(resume_parser)
    while 1:
        schedule.run_pending()
        time.sleep(1)
        

