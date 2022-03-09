import requests


API_URL = 'https://api.persianspeech.com/recognize-file'
FILE_PATH = ''      # Put the path to your file here


json_data = {
    "auth_token": "",   # Put your auth-token here
    "api_key": "",      # Put your api-key here
}
with open(FILE_PATH, 'rb') as file:
    file_dict = { "file": file, }

    resp = requests.post(API_URL, data=json_data, files=file_dict)


result = 'Success' if resp.status_code==200 else 'Failure'
print(f"result: {result}", resp.json(), sep='\n')

