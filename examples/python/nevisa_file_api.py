import requests
import time
import keyboard

LOGIN_API_URL = "https://accounting.persianspeech.com/account/login"
BASE_API_URL = "https://api.persianspeech.com"
RECOGNIZE_FILE_API_URL = 'https://api.persianspeech.com/recognize-file'
TERMINATE_TASK_URL = "https://api.persianspeech.com/file/terminate-task"

# The path of your file (Common audio or video formats are accepted.)
FILE_PATH = 'test.mp4'

# 1. Login --------------------------------------

json_data = {
    'username_or_phone_or_email': "",   # Your username
    'password': "",                     # Your password
}

response = requests.post(LOGIN_API_URL, data=json_data)

result = 'Success' if response.status_code == 200 else 'Failure'
print(f"login result: {result}", response.json(), sep='\n')

if result == 'Failure':
    exit()

auth_token = response.json()['user']['token']
api_key = response.json(
)['user']['nevisa_service_account']['current_service_record']['key']

# 2. File Recognition --------------------------------------

json_data = {
    "auth_token": auth_token,   # Put your auth-token here
    "api_key": api_key,      # Put your api-key here
}
with open(FILE_PATH, 'rb') as file:
    file_dict = {"file": file, }

    response = requests.post(RECOGNIZE_FILE_API_URL,
                             data=json_data, files=file_dict)

result = 'Success' if response.status_code == 200 else 'Failure'
print(f"recognize-file result: {result}", response.json(), sep='\n')

if result == 'Failure':
    exit()

# 3. Task Progress --------------------------------------

task_id = response.json()['task_id']
progress_url = response.json()['progress_url']
response = requests.get(BASE_API_URL+progress_url)

while (response.json()['state'] == "PROGRESS"):
    response = requests.get(BASE_API_URL+progress_url)
    print(f"Progress: {response.json()['progress']['percent']} %")
    time.sleep(3)  # Sleep for 3 seconds

# 4. Terminate Task --------------------------------------

    print("Press Esc to terminate the task ...")
    if keyboard.is_pressed('Esc'):
        print("Terminating the task ...")
        json_data = {
            'auth_token': auth_token,     # from login API
            'api_key': api_key,           # from login API
            'task_id': task_id,
        }
        resp = requests.post(TERMINATE_TASK_URL, data=json_data)
        result = 'Success' if response.status_code == 200 else 'Failure'
        print(
            f"file/terminate-task result: {result}", response.json(), sep='\n')
        break

# 5. Final Result --------------------------------------

if response.json()['state'] == "SUCCESS":
    print(
        f"Final Result: {response.json()['result']['transcription']['text']}")
