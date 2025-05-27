from ..models import User

def UserExists(username,
                password):
    return User.objects.filter(
        username=username,
        password=password
    ).exists()

def GetUser(username,
                password):
    return User.objects.filter(
        username=username,
        password=password
    ).last()

def GetUsers():
    return User.objects.exclude(birth_date__isnull=True)