### NOTE: You should import this file in accounting shell: 
#     go to accounting path, 
#     source the venv, 
#     enter: 'python3 manage.py shell', 
#     then just import this file. Done!
###########################################################

from django.contrib.auth import get_user_model

n = int(input(">> Enter the number of demo users:"))
initial_charge = int(input(">> Enter the initial charge (in Tomans):"))
pwd = input(">> Enter the password:")

User = get_user_model()

for i in range(n):
    user = User.objects.create_user(
        username=f"demo_user_{i + 1}",
        password=pwd,
        is_active=True,
    )
    user.wallet.add_charge(initial_charge * 10)
    print(f"# USER {user.username} WAS CREATED SUCCESSFULLY.")
