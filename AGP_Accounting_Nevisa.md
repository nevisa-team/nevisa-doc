# AGP_Accounting_Nevisa

# User Account
## Signup (Phone Number)
    POST: /account/signup/phone

Request:

    {
      'username': "username",         # must be unique
      'phone': "989123456789",        # must be unique
      'password': "xxxxxxx",
      'password_confirmation': "xxxxxxx",
    }

Response:

    {
      'message': "Check the verification code sent to your phone.",
      'user': {
        'id': "user's UUID",
        'username': "username",
        'phone': "989123456789",
      }
    }

**NOTE:** Then, in case of success, a **6-digit** **verification code** will be sent to the user’s phone. Then, in the next page user has to enter the verification code and verify his account.
(see: [**Account Signup Verification**](https://www.dropbox.com/scl/fi/e46cuzg2b48lhzmtrpghp/AGP-Accounting_-Nevisa.paper?dl=0&rlkey=iauxqsaezndmpimw1szrm8949#:uid=857330188486620456568120&h2=Account-Signup-Verification))

----------
## Signup (Email)
    POST: /account/signup/email

Request:

    {
      'username': "username",        # must be unique
      'email': "xxxx@yyyy.zzz",      # must be unique
      'password': "xxxxxxx",
      'password_confirmation': "xxxxxxx",
    }

Response (200):

    {
      'message': "Check the verification code sent to your email.",
      'user': {
        'id': "user's UUID",
        'username': "username",
        'email': "xxxx@yyyy.zzz",
      }
    }

**NOTE:** Then, in case of success, a **6-digit** **verification code** will be sent to the user’s email. Then, in the next page user has to enter the verification code and verify his account.
(see: [**Account Signup Verification**](https://www.dropbox.com/scl/fi/e46cuzg2b48lhzmtrpghp/AGP-Accounting_-Nevisa.paper?dl=0&rlkey=iauxqsaezndmpimw1szrm8949#:uid=857330188486620456568120&h2=Account-Signup-Verification))

----------
## Account Signup Verification
    POST: /account/verify_signup

Request:

    {
      'id': "user's UUID",
      'otp': "XXXXXX",
    }

**NOTE:** the otp expiration time is **2 minutes**.
**NOTE:** after **1 minute**, the user can use either [Signup (Phone Number)](https://www.dropbox.com/scl/fi/e46cuzg2b48lhzmtrpghp/AGP-Accounting_-Nevisa.paper?dl=0&rlkey=iauxqsaezndmpimw1szrm8949#:uid=040046239105405080046067&h2=Signup-(Phone-Number)) or [Signup (Email)](https://www.dropbox.com/scl/fi/e46cuzg2b48lhzmtrpghp/AGP-Accounting_-Nevisa.paper?dl=0&rlkey=iauxqsaezndmpimw1szrm8949#:uid=891002082232704583811118&h2=Signup-(Email)) to signup again. (before that 1 minute, he’d receive an error implying the username/phone/email already exists in the database.)

Response (200):

    {
      'message': "Account is successfully verified.",
      'user': {
          'id': "user's UUID",
          'username': "username",
          'phone': "989123456789",
          'email': "xxxxxx@yyyy.zzz",
          'token': "user's auth-token",
      }
    }

**NOTE:** If the verification code is not expired and is valid, the user’s account will be activated.


----------
## Resend Verification Code (Phone Number)
    POST: /account/resend_veification_code/phone

Request:

    {
      'id': "user's UUID",
    }

Response (200):

    {
      'message': "Check the verification code sent to your phone.",
      'user': {
          'id': "user's UUID",
          'username': "username",
          'phone': "989123456789",
      }
    }

**NOTE:** If the verification code is **not expired** and is **valid**, the user’s account will be **activated**.

----------


## Resend Verification Code (Email)
    POST: /account/resend_veification_code/email

Request:

    {
      'id': "user's UUID",
    }

Response (200):

    {
      'message': "Check the verification code sent to your email.",
      'user': {
          'id': "user's UUID",
          'username': "username",
          'email': "xxxxx@yyyy.zzz",
      }
    }

**NOTE:** If the verification code is **not expired** and is **valid**, the user’s account will be **activated**.

----------
## Login
    POST: /account/login

Request:

    {
      'username_or_phone_or_email': "uuupppeee", 
      'password': "xxxxxx",
    }

Response (200):

    {
      'message': "Successfully logged in.",
      'data': {
        'id': "user's UUID",
        'username': "username",
        'phone': "989123456789",
        'email': "xxxxxx@yyyy.zzz",
        'token': "User's auth-token",
      }
    }

**NOTE:** The **authentication token** changes every time the user logs in.

----------
## Forgot Password
    POST: /account/forgot_password

Request:

    {
      'username': "username",
      'phone': "989123456789", 
      'email': "xxxxxx@yyyy.zzz", 
    }

**NOTE:**  there should be **either ‘phone’ or ‘email’** in request data (never put both pf them!)

Response (200):

    {
      'message': "Account is successfully verified. Check your phone/email.",
      'user': {
          'id': "user's UUID",
          'username': "username",
          'phone': "989123456789",
          'email': "xxxxxx@yyyy.zzz", 
      }
    }

**NOTE:** Then, if everything’s OK, a **6-digit** **verification code** will be sent to user’s phone/email.
Then, in the next page user has to enter the verification code and **change his password**.
(see: [Change Forgotten Password](https://www.dropbox.com/scl/fi/e46cuzg2b48lhzmtrpghp/AGP-Accounting_-Nevisa.paper?dl=0&rlkey=iauxqsaezndmpimw1szrm8949#:uid=868178356293783795301399&h2=Change-Forgotten-Password))

----------
## Change Forgotten Password
    POST: /account/change_forgotten_password

Request:

    {
      'id': "user's UUID",
      'otp': "oooooo",
      'password': "xxxxxxxx",
      'password_confirmation': "xxxxxxxx",
    }

Response (200):

    {
      'message': "Password successfully changed.",
      'user': {
          'id': "user's UUID",
          'username': "username",
          'phone': "989123456789",
          'email': "xxxxxx@yyyy.zzz", 
          'token': "User's auth-token",
      }
    }

**NOTE:** Then, if everything’s OK, the password will be changed.

----------


## Logout
    POST: /account/logout


- Header authentication: **required**
    {'Authorization': "Token <auth-token>"}

Request:

    {
      'id': "user's UUID",
    }

Response (200):

    {
      'message': "Logged out successfully.",
    }

**NOTE:** The **authentication token** changes every time the user logs in.

----------
## Retrieve Account
    GET: /account/retrieve


- Header authentication: **required**
    {'Authorization': "Token <auth-token>"}

Response (200):

    {
        'id': "user's UUID",
        'username': "username",
        'phone': "989123456789",
        'email: "xxxxxx@yyyyy.zzz",
      
        'nevisa_service_account': {
            'current_charge': 0,
            'usage_remained': 0,
            'num_service_history': 0,
            'has_service': bool,
            
            'configuration': {
                'insert_punctuation': bool,
            },
            
            'current_service_record': {
                'id': "UUID",
                'start_time': datetime,
                'end_time': datetime,
                'key': "API KEY",
    
                'service': {
                    'id': "UUID",
                    'name': "name",
                    'code': 1,
                    'deadline': 30,
                    'price_per_hour' : 10000,
                    'hour_limit': 30,
                    'max_users': 2,
                    'actual_price': 300000,
                },
            }
        },
    }


----------



# 
# Nevisa
## Retrieve All Services
    GET: /nevisa/get_services

Response (200): returns a **list** of all services (packages) available to purchase

    [
      {
        'id': "UUID",
        'name': "name",
        'code': 1,
        'deadline': datetime,
        'price_per_hour': 1000,
        'hour_limit': 20,
        'max_users': 2,
        'actual_price': 1000,
      },
      {
        'id': "UUID",
        ...
      },
      ...
    ]
----------
## Retrieve Transactions History
    GET: /nevisa/transactions/retrieve_all


- Header authentication: **required**
    {'Authorization': "Token <auth-token>"}

Response (200): returns a **list** of all transactions ordered by their creation date; newest first.

    [
      {
        'user': "user's UUID",
        'amount': "amount",                            # Tomans
        'description': "description",
        'created_at': "creation datetime",
        'verified_at': "verification datetime",        # nullable
        'status': "PENDING / FAILED / SUCCESS",
        'is_test': bool,        # no need to show this field
      },
      {
        'user': "user's UUID",
        ...
      },
      ...
    ]
----------
## Buy Service
    POST: /nevisa/buy_service


- Header authentication: **required**
    {'Authorization': "Token <auth-token>"}

Request:

    {
      'service_id': "service's UUID",
    }

Response (200):

    {
        'message': "The service is successfully bought.",    
    
        'service_record': {
            'id': "UUID",
            'start_time': datetime,
            'end_time': datetime,
            
            'service': {
                'id': "UUID",
                'name': "name",
                'code': 1,
                'deadline': datetime,
                'price_per_hour': 1000,
                'hour_limit': 20,
                'max_users': 2,
                'actual_price': 1000,
            },
        }
    }

**NOTE:** if the user’s **already got an active service** or he **doesn’t have enough charge** in his wallet, a corresponding **error** will be returned.


----------


## Set Configuration
    PUT: /nevisa/set_config


- Header authentication: **required**
    {'Authorization': "Token <auth-token>"}

Request:

    {
      'insert_punctuation': bool,
    }

Response (200):

    {
      'insert_punctuation': bool,
    }


----------


## Check Account
    POST: /nevisa/check_account


- Header authentication: **required**
    {'Authorization': "Token <auth-token>"}

Request:

    {
      'key': "api-key"
    }

Response (200):

    {
        'usage_remained': 10000,       // in milliseconds (ms)
        'configuration': {
            'insert_punctuation': bool,
        },
      }

**NOTE:** The response status code will be **HTTP_401_UNAUTHORIZED** if the token (sent in the header) is not valid; otherwise, the status code will be HTTP_200_OK.

----------
## Use
    POST: /nevisa/use


- Header authentication: **required**
    {'Authorization': "Token <auth-token>"}

Request:

    {
      'key': "api-key",
      'usage_amount': 10000            # in milliseconds (ms)
    }

Response (200):

    {
      'usage_remained': 5000            # in milliseconds (ms)
    }

**NOTE:** The response status code will be **HTTP_401_UNAUTHORIZED** if the token (sent in the header) is not valid; otherwise, if the usage amount is valid, the status code will be HTTP_200_OK.

----------


# Charge
## Buy Charge
    URL: /charge/buy_charge

Authentication token: **required**

Request:

    {
      'amount': 1000,         # in Tomans
    }

Response (200):

    {
      'redirect_url': "url to redirect"         
      # the url is something like "https://www.zarinpal.com/pg/StartPay/..."
    }

**NOTE:** Then,  the user should be redirected to the page where he should pay the price. (Zarinpal) After the payment is done, the user will be redirected to a page where the payment result is shown.

----------


