import random

def get_email_from_user_name(user_name):
    user_name = user_name.replace(" ", "")
    user_name+=str((random.randint(1000,9999)))+"@quanta.in"
    return user_name
    