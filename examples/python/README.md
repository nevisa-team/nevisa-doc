## Requirements
```
pip install requests, keyboard
```
## File Path
مسیر فایل صوتی ورودی
```
FILE_PATH = 'test.mp4'
```
## username & password

نام کاربری و گذرواژه خود را در این بخش وارد کنید
```
login("Your username", "Your password")
```

برای استفاده از API های سرور نویسا باید ابتدا در وبسایت [پرشین‌اسپیچ](https://persianspeech.com) ثبت‌نام کرده و حساب کاربری خود را با استفاده از ایمیل یا شماره تلفن خود فعال کنید.

پس از فعالسازی و ورود به حساب کاربری خود، باید حتما یکی از بسته‌های نویسا را برای خود فعال کنید. (می‌توانید برای شروع و تست از بسته‌ی یک ساعته‌ی رایگان استفاده کنید.)

## Test Nevisa
اکنون می‌توانید سرویس نویسا را تست کنید.

```
python nevisa_test.py
```

از API های نویسا به شکل زیر می توانید در برنامه خود استفاده کنید.

## 1. Login
    POST: https://accounting.persianspeech.com/account/login

با استفاده از این API می‌توانید با ارسال نام‌کاربری، ایمیل، یا تلفن خود به همراه رمز عبور حساب کاربری خود، token و api-key خود را دریافت کنید. شما برای استفاده از API های دیگر به این دو مقدار نیاز خواهید داشت.

Request:

    {
      'username_or_phone_or_email': "uuupppeee", 
      'password': "xxxxxx",
    }

Response (200):

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
    
**auth-token:**

    response.data['user']['token']

**api-key:**

    response.data['user']['nevisa_service_account']['current_service_record']['key']

**توجه:** مقدار **authentication token** با هر بار لاگین کردن تغییر می‌کند.

**توجه:** در صورتی که بسته‌ی فعال نداشته باشید، مقدار **current_service_record** برابر **null** خواهد بود.

----------

## 2. File Recognition
    POST: https://api.persianspeech.com/recognize-file

حال با استفاده از auth-token و api-key خود که از Login دریافت کردید، می‌توانید فایل صوتی خود را (بدون نیاز به تبدیل فرمت فایل) به این API فرستاده و در پاسخ متن حاصل از تبدیل فایل صوتی را دریافت کنید.

**توجه:** فرمت request شما برای این API باید حتما به صورت **multipart/form-data** باشد. در غیر این صورت با خطا مواجه خواهید شد.

Request:

    {
      'auth_token': "user's authentication token",     # from login API
      'api_key': "user's api-key",                     # from login API
      'file': <file>,
    }

Response (200):

    {
        'progress_url': "/celery-progress/<task_id>/",
        'task_id': "task_id",
    }

**نکته:** می‌توانید با ارسال یک درخواست GET به progress_url میزان پیشرفت یا progress عملیات تبدیل صوت به متن فایل ارسال شده‌ی خود را مشاهده نمایید. برای جزئیات بیشتر به API بعدی (Task Progress) رجوع کنید.


----------


## 3. Task Progress
    GET: https://api.persianspeech.com/celery-progress/<task_id>/
    
با استفاه از این API می‌توانید با استفاده از progress_url مربوط به task خود که در File Recognition API دریافت کردید، میزان پیشرفت با progress عملیات تبدیل صوت به متن فایل ارسال شده‌ی خود را مشاهده کنید.

همچنین هرگاه مقدار state در پاسخ برابر  SUCCESS شد، می‌توانید متن حاصل از تبدیل فایل صوتی خود را در کلید result پیدا کنید.

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

**result:**
    
    response.data['result']['transcription']['result'] = لیستی از تمام کلمات تشخیص داده شده به همراه زمان دقیق شروع و پایان بیان هر کلمه در فایل صوتی و میزان اطمینان مدل از تشخیص هر کلمه

    response.data['result']['transcription']['text'] = متن نهایی


----------


## 4. Terminate Task
    POST: https://api.persianspeech.com/file/terminate-task

با استفاده از این API می‌توانید عملیات تبدیل صوتی خود را لغو کنید. برای این کار نیاز به مقدار task_id دارید که از پاسخ File Recognition API دریافت کردید.

همچنین، برای این API باید مقدار auth-token خود را به شکل زیر در **header** درخواست خود قرار دهید:

    {'Authorization': "Token <auth-token>"}

Request:

    {
        'auth_token': "user's authentication token",     # from login API
        'api_key': "user's api-key",                     # from login API
        'task_id': "task_id",
    }

در صورتی که تسک با موفقیت لغو شود، پاسخ شامل کد status = 200 خواهد بود.
