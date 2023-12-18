import gradio as gr
import time
from nevisa_file_api import *

# 1. Login --------------------------------------
response, auth_token, api_key = login("Your username", "Your password")

# 2. Set Configuration --------------------------------------
set_configuration(auth_token, convert_punctuations=True)


def transcribe(audio):
    # 3. File Recognition --------------------------------------
    task_id, progress_url = file_recognition(auth_token, api_key, audio)

    # 4. Task Progress --------------------------------------
    while True:
        result, response = task_progress(task_id, progress_url)
        print(f"Progress: {response['progress']['percent']} %")
        if (response['state'] != "PROGRESS"):
            break
        time.sleep(3)  # Sleep for 3 seconds

    # 6. Final Result --------------------------------------

    if response['state'] == "SUCCESS":
        print(f"Final Result: {response['result']['transcription']['text']}")
        return response['result']['transcription']['text']


demo = gr.Interface(
    transcribe,
    gr.Audio(type="filepath"),
    "text",
)

demo.launch()
