# Nevisa Server

# File Protocol
## File Recognition
    POST: /recognize-file


- Header authentication: **required**
    {'Authorization': "Token <auth-token>"}

**NOTE:** the request must be in **multipart/form-data** format

Request:

    {
      'auth_token': "user's authentication token",     # take it from accounting
      'api_key': "user's api-key",                     # take it from accounting
      'file': <file>,
    }

Response (200):

    {
        'progress_url': "/celery-progress/<task_id>/",
        'task_id': "task_id",
    }

**NOTE:** send a GET request to the progress_url to see the progression of your speech-to-text conversion task. (you can see the result in detail in )


----------


## Task Progress
    GET: /celery-progress/<task_id>/

Response [**Before the Final Result**]:

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

Response [**The Final Result**]:

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


**NOTE:** send a GET request to the progress_url to see the progression of your speech-to-text conversion task. (you can see the result in detail in )


----------


## Terminate Task
    POST: /file/terminate-task


- Header authentication: **required**
    {'Authorization': "Token <auth-token>"}

**NOTE:** the request must be in **multipart/form-data** format

Request:

    {
      'auth_token': "user's authentication token",     # take it from accounting
      'api_key': "user's api-key",                     # take it from accounting
      'task_id': "task_id",
    }

**NOTE:** if the task does not belong to the user, a **401 error** will be returned. otherwise, response will contain a **200** status code.
