import time
import keyboard
from nevisa_file_api import *

# The path of your file (Common audio or video formats are accepted.)
FILE_PATH = 'test.wav'

# 1. Login --------------------------------------
response, auth_token, api_key = login("Your username", "Your password")

# 2. Set Configuration --------------------------------------
set_configuration(auth_token, convert_punctuations=True)

# 3. File Recognition --------------------------------------
task_id, progress_url = file_recognition(auth_token, api_key, FILE_PATH)

# 4. Task Progress --------------------------------------
while True:
    result, response = task_progress(task_id, progress_url)
    print(f"Progress: {response['progress']['percent']} %")
    if(response['state'] != "PROGRESS"):
        break

    # 5. Terminate Task --------------------------------------
    print("Press Esc to terminate the task ...")
    if keyboard.is_pressed('Esc'):
        print("Terminating the task ...")
        result = terminate_task(auth_token, api_key, task_id)
        print(f"file/terminate-task result: {result}")
        break
    time.sleep(3)  # Sleep for 3 seconds

# 6. Final Result --------------------------------------

if response['state'] == "SUCCESS":
    print(f"Final Result: {response['result']['transcription']['text']}")
