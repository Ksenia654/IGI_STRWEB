from ..models import Employee, Contract, EstateReview

def OwnContracts(employee :Employee):
    return Contract.objects.filter(realtor=employee)

def WorkingWith(employee :Employee):
    return EstateReview.objects.filter(realtor=employee).values_list('client').distinct()

def IsEmployee(user):
    return Employee.objects.filter(profile=user).exists()

def GetEmployee(user):
    return Employee.objects.filter(profile=user).last()

def GetEmployeeById(userId):
    return Employee.objects.filter(id=userId).last()

def GetCountEmployeesByCategory(category):
    return len(Employee.objects.filter(category=category).all())