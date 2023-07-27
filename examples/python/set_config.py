import requests

LOGIN_API_URL = "https://accounting.persianspeech.com/account/login"
SET_CONFIG_API_URL = "https://accounting.persianspeech.com/nevisa/set_config"

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

# 2. Set Configuration --------------------------------------

json_data = {
    'add_number_separator': False,
    'convert_numbers': True,
    'convert_punctuations': False,
    'show_digits_in_english': True,
    'show_word_confidences': False,
}
headers = {'Authorization': f"Token {auth_token}"}
response = requests.put(SET_CONFIG_API_URL, data=json_data, headers=headers)
result = 'Success' if response.status_code == 200 else 'Failure'
if result == 'Failure':
    exit()
print(f"set_config result: {result}", response.json(), sep='\n')
