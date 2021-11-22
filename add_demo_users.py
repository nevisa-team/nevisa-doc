### NOTE: You should import this file in accounting shell: 
#     go to accounting path, 
#     source the venv, 
#     enter: 'python3 manage.py shell', 
#     then import this file (add_demo_users),
#     then just call the function: 
#           add_users(n=1, initial_charge=100000, pwd='123') with the arguments you want. Done!
###########################################################

from django.contrib.auth import get_user_model


def add_users(n=1, initial_charge=100000, pwd='123'):
    User = get_user_model()

    for i in range(n):
        user = User.objects.create_user(
            username=f"demo_user_{i + 1}",
            password=pwd,
            is_active=True,
        )
        user.wallet.add_charge(initial_charge * 10)
        print(f"# USER {user.username} WAS CREATED SUCCESSFULLY.")
