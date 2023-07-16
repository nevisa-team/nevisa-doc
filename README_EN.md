To use the APIs of Nevisa server, you need to first sign up for the [PersianSpeech](https://persianspeech.com/) website and activate your account using your email or phone number.
After activating and logging into your account, you must activate one of Nevisa’s packages (you can use the one hour free package to start and test the service)

Now you can use following APIs
## 1.Login

```
POST: https://accounting.persianspeech.com/account/login
```
Using this API, you can get your **token** and **api-key** by sending your username, email, or phone number with your password, you will need these two values to use other APIs.

Request:
```
{
  'username_or_phone_or_email': "uuupppeee", 
  'password': "xxxxxx",
}
```
Response (200):
```
{
    'message': "Successfully logged in.",
    'user': {
        'id': "user's UUID",
        'token': "user's auth-token",
        'username': "username",
        'phone': "989123456789",
        'email': "xxxxxx@yyyy.zzz",
        'is_staff': bool,
        'is_telegram_user': bool,
  
        'nevisa_service_account': {
            'current_service_record': {
                'key': "your api-key",
                ...
            },
            ...
        }
  }
}
```
**auth-token:**
```
response.data['user']['token']
```
**api-key:**
```
response.data['user']['nevisa_service_account']['current_service_record']['key']
```
**Note:** The value of the **authentication token** changes every time you log in.

**Note:** if you don't have an active package, the value of the **current_service_record** will be **null**.

------------------

## 2.File Recognition
```
POST: https://api.persianspeech.com/recognize-file
```
Now using your **auth-token** and **api-key** that you got from Login, you can send your audio file (without using change the file format) to this API and you will receive the resulting text of the audio file.

**Note:** your request format for this API must be in the from of: 
**multipart/form-data.**

In otherwise you will get a error.

Request:
```
{
  'auth_token': "user's authentication token",     # from login API
  'api_key': "user's api-key",                     # from login API
  'file': <file>,
}
```
Response (200):
```
{
    'progress_url': "/celery-progress/<task_id>/",
    'task_id': "task_id",
}
```
**Note:** you can send a GET request to **progress_url** to see the progress of the audio to text conversion operation of your uploaded file. For more details, refer to the next API(Task Progress).

------------------

## 3. Task Progress

```
GET: https://api.persianspeech.com/celery-progress/<task_id>/
```

Using this API, you can see the progress of the audio to text conversion operation of your uploaded file by using the progress_url of your task which you got in the File Recognition API.

Also, when the value of the “**state**” in the response becomes **SUCCESS**, you can find the resulting text from the audio file in the “**result**” key.

Response [**Before the Final Result**]:
```
{
    'state': "PROGRESS",
    'complete': false,
    'success': null,
    'progress': {
        'pending": false,
        'current': 65,      # less than total
        'total': 100,
        'percent': 65
    }, 
}
```
Response [**The Final Result**]:
```
{
    'state': "SUCCESS",
    'complete': true,
    'success': true,
    'progress': {
        'pending": false,
        'current': 100, 
        'total': 100,
        'percent': 100
    }, 
    'result': {
        'transcription': {
            'result': [
                {'conf': 1.0, 'end': 2.61, 'start': 0.0, 'word': "word"},
                {...},
                ...
            ],
            'text': "final and complete text"
        },
        'final': true
    },
}
```
**Result:**
```
response.data['result']['transcription']['result'] = A list of all recognized words along with the precise start and end time of each word's utterance in the audio file and the model's confidence level in recognizing each word.

response.data['result']['transcription']['text'] = last text
```

------

## 4. Terminate Task
```
POST: https://api.persianspeech.com/file/terminate-task
```
Using this API, you can cancel your audio conversion operation. For this, you need the “**task_id**” value that you got from the response of the File Recognition API.
Also, for this API, you must place your **auth-token** value in the **header** of your request as below:

```
{'Authorization': "Token <auth-token>"}
```
Request:
```
{
    'auth_token': "user's authentication token",     # from login API
    'api_key': "user's api-key",                     # from login API
    'task_id': "task_id",
}
```
If the task is successfully canceled, the response will include this code: status = 200.




