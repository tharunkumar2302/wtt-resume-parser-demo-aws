# wtt-resume-parser

## Requirements
* Python 3.8
* Ubuntu 20.00 and above
* MongoDB

## Installation

1. Clone the repo `git clone https://github.com/walkingtree/wtt-resume-parser.git`
2. Create the virtualenv `python3 -m venv .venv`
*  For Ubuntu:
   Activate the environment `source .venv/bin/activate`
*  For Windows:
   Activate the environment  `.venv\Scripts\activate.bat`
3. Install the dependency `pip install -r requirements.txt` Before that you have to 
   install sudo depedencies from requirements.txt file
4. Edit the `.env` file and add the environment variable there

## Usage
1. Import it in your Python project

* ### To start the script:
      python3 start_script.py .env_file(.env_dev or .env_uat or .env_qa)
* ### To stop the script:
      python3 stop_script.py
      
```python
from main import ResumeParser
data = ResumeParser('/path/to/filename').get_extracted_data()
print("data :",data)
```

* ### To start the script:
      nohup python3 main.py .env_file &     ==>(.env_dev or .env_uat or .env_qa)
* ### To stop the script:
      ps aux | grep main.py
      kill <PID>


# To execute the code
nohup python3 flask_api.py .env_dev &


# To stop the code
sudo lsof -i :5000
sudo kill <PID>

# wtt-resume-parser-demo-aws
# wtt-resume-parser-demo-aws
# wtt-resume-parser-demo-aws
