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