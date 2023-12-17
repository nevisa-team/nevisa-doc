import requests

LOGIN_API_URL = "https://accounting.persianspeech.com/account/login"
SET_CONFIG_API_URL = "https://accounting.persianspeech.com/nevisa/set_config"
BASE_API_URL = "https://api.persianspeech.com"
RECOGNIZE_FILE_API_URL = 'https://api.persianspeech.com/recognize-file'
TERMINATE_TASK_URL = "https://api.persianspeech.com/file/terminate-task"


# Login --------------------------------------
def login(username, password):
    json_data = {
        'username_or_phone_or_email': username,
        'password': password,
    }

    response = requests.post(LOGIN_API_URL, data=json_data)

    result = 'Success' if response.status_code == 200 else 'Failure'
    
    if result == 'Failure':
        raise Exception("Login Failure")

    auth_token = response.json()['user']['token']
    api_key = response.json()['user']['nevisa_service_account']['current_service_record']['key']
    return response.json(), auth_token, api_key

# File Recognition --------------------------------------
def file_recognition(auth_token, api_key, file_path):
    json_data = {
        "auth_token": auth_token,   # Put your auth-token here
        "api_key": api_key,      # Put your api-key here
    }
    with open(file_path, 'rb') as file:
        file_dict = {"file": file, }

        response = requests.post(RECOGNIZE_FILE_API_URL,
                                data=json_data, files=file_dict)

    result = 'Success' if response.status_code == 200 else 'Failure'
    print(f"recognize-file result: {result}", response.json(), sep='\n')

    if result == 'Failure':
        raise Exception("File Recognition Failure")
    task_id = response.json()['task_id']
    progress_url = response.json()['progress_url']
    return task_id, progress_url

# Task Progress --------------------------------------
def task_progress(task_id, progress_url):
    response = requests.get(BASE_API_URL+progress_url)
    result = 'Success' if response.status_code == 200 else 'Failure'
    return result, response.json()

# Terminate Task --------------------------------------
def terminate_task(auth_token, api_key, task_id):
    json_data = {
        'auth_token': auth_token,     # from login API
        'api_key': api_key,           # from login API
        'task_id': task_id,
    }
    response = requests.post(TERMINATE_TASK_URL, data=json_data)
    result = 'Success' if response.status_code == 200 else 'Failure'
    return result

# Set Configuration --------------------------------------
def set_configuration(auth_token, add_number_separator=False, convert_numbers=True, convert_punctuations=False,show_digits_in_english=True, show_word_confidences=False):
    json_data = {
        'add_number_separator': add_number_separator,
        'convert_numbers': convert_numbers,
        'convert_punctuations': convert_punctuations,
        'show_digits_in_english': show_digits_in_english,
        'show_word_confidences': show_word_confidences,
    }
    headers = {'Authorization': f"Token {auth_token}"}
    response = requests.put(SET_CONFIG_API_URL, data=json_data, headers=headers)
    result = 'Success' if response.status_code == 200 else 'Failure'
    return result, response
