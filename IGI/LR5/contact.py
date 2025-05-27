from ..models import Employee

def GetContacts():
    return Employee.objects.all()