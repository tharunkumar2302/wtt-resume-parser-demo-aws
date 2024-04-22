import json
import requests
import urllib.parse
import os


def lambda_handler(event, context):
    # TODO implement
    print(event)
    try:
        for i in event['Records']:
            s3_event = json.loads(i['body'])
            if 'Event' in s3_event and s3_event['Event'] == 's3:TestEvent':
                print("Test Event")
            else:
                for j in s3_event['Records']:
                    
                    # Define the API endpoint URL
                    
                    #url = "http://18.188.66.128:5000/"
                    url = os.environ['devurl']
                    # Prepare the data to be sent in the request body
                    # Condition for dev bucket folder
                    if os.environ['devbck'] in j['s3']['object']['key']:
                        url = os.environ['devurl']
                        
                    # Condition for Demo bucket folder
                    if os.environ['demobck'] in j['s3']['object']['key']:
                        url = os.environ['demourl']
                        
                    # Condition for UAT bucket folder
                    #if os.environ['uatbck'] in j['s3']['object']['key']:
                    #    url = ''
                    
                    print("URL=>",url)
                    print("Bucket Name",j['s3']['object']['key'])
                    
                    if url:    
                        
                        data = {"filename":urllib.parse.unquote_plus(urllib.parse.unquote(j['s3']['object']['key']))}
                        
                        data = json.dumps(data)
                        print(data)
                        headers = {
                            "Content-Type": "application/json"
                        }
                        
                        # Send the POST request with the data
                        response = requests.post(url, data=data, headers=headers)
                        print("Response code => ",response.status_code)
                        # Check the response status code
                        if response.status_code == 200:
                            # Request successful
                            print("Data sent successfully!")
                            print("Bucket Name : {} ".format(j['s3']['bucket']['name']))
                            print("Object Name : {} ".format(j['s3']['object']['key']))
                                
                        else:
                            # Request failed
                            print(response)
                            print("Failed to send data. Status code:", response.status_code)
                    else:
                        print('Please upload file into a uploadedfiles folder so that file will move')
                        
    except Exception as exception:
        print(exception)


# import time


# import json
# import requests
# import urllib.parse
# import os

# # Function to load the list of processed files
# def load_processed_files():
#     try:
#         with open('processed_files.txt', 'r') as file:
#             return file.read().splitlines()
#     except FileNotFoundError:
#         return []

# # Function to save the list of processed files
# def save_processed_files(processed_files):
#     with open('processed_files.txt', 'w') as file:
#         file.write('\n'.join(processed_files))

# # Function to load the list of files currently being processed
# def load_files_in_process():
#     try:
#         with open('files_in_process.txt', 'r') as file:
#             return file.read().splitlines()
#     except FileNotFoundError:
#         return []

# # Function to save the list of files currently being processed
# def save_files_in_process(files_in_process):
#     with open('files_in_process.txt', 'w') as file:
#         file.write('\n'.join(files_in_process))

# def lambda_handler(event, context):
#     # Load the list of processed files and files currently being processed
#     processed_files = load_processed_files()
#     files_in_process = load_files_in_process()
    
#     # TODO implement
#     print(event)
#     try:
#         for i in event['Records']:
#             s3_event = json.loads(i['body'])
#             if 'Event' in s3_event and s3_event['Event'] == 's3:TestEvent':
#                 print("Test Event")
#             else:
#                 for j in s3_event['Records']:
#                     # Check if the file is already in process
#                     if j['s3']['object']['key'] in files_in_process:
#                         print(f"File {j['s3']['object']['key']} is already in process. Skipping...")
#                         continue

#                     # Check if the file has already been processed
#                     if j['s3']['object']['key'] in processed_files:
#                         print(f"File {j['s3']['object']['key']} has already been processed. Skipping...")
#                         continue

#                     # Define the API endpoint URL
#                     url = os.environ['devurl']
                    
#                     # Prepare the data to be sent in the request body
#                     if os.environ['devbck'] in j['s3']['object']['key']:
#                         url = os.environ['devurl']
#                     if os.environ['demobck'] in j['s3']['object']['key']:
#                         url = os.environ['demourl']

#                     print("URL=>",url)
#                     print("Bucket Name",j['s3']['object']['key'])
                    
#                     if url:    
#                         data = {"filename":urllib.parse.unquote_plus(urllib.parse.unquote(j['s3']['object']['key']))}
#                         data = json.dumps(data)
#                         print(data)
#                         headers = {
#                             "Content-Type": "application/json"
#                         }
                        
#                         # Mark the file as in process
#                         files_in_process.append(j['s3']['object']['key'])
#                         save_files_in_process(files_in_process)
                        
#                         # Send the POST request with the data
#                         response = requests.post(url, data=data, headers=headers)
#                         print("Response code => ",response.status_code)
                        
#                         # Check the response status code
#                         if response.status_code == 200:
#                             # Request successful
#                             print("Data sent successfully!")
#                             print("Bucket Name : {} ".format(j['s3']['bucket']['name']))
#                             print("Object Name : {} ".format(j['s3']['object']['key']))
                            
#                             # Add the file to the list of processed files
#                             processed_files.append(j['s3']['object']['key'])
#                             save_processed_files(processed_files)
                            
#                             # Remove the file from the list of files in process
#                             files_in_process.remove(j['s3']['object']['key'])
#                             save_files_in_process(files_in_process)
#                         else:
#                             # Request failed
#                             print(response)
#                             print("Failed to send data. Status code:", response.status_code)
#                             # Remove the file from the list of files in process
#                             files_in_process.remove(j['s3']['object']['key'])
#                             save_files_in_process(files_in_process)
#                     else:
#                         print('Please upload file into a uploadedfiles folder so that file will move')
                        
#     except Exception as exception:
#         print(exception)
