from accounts.models import *

def get_all_user():
    return User.objects.all()