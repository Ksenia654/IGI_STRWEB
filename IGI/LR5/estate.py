from ..models import Estate, Employee, EstateReview

def GetSellingEstates():
    return Estate.objects.filter(owner=None).all()

def GetFilteredEstates(min_cost=None, 
                       max_cost=None, 
                       category=None,
                       free=False):
    estates = Estate.objects
    if min_cost:
        estates = estates.filter(cost__gte=min_cost)
    if max_cost:
        estates = estates.filter(cost__lte=max_cost)
    if category:
        estates = estates.filter(category=category)
    if free:
        estates = estates.filter(owner=None)
    return estates.all()

def GetEstateReviews(
        client=None,
        employee=None,
        estate_id=None):
    reviews = EstateReview.objects
    if client:
        reviews = reviews.filter(client=client)
    if employee:
        reviews = reviews.filter(employee=employee)
    reviews = reviews.filter(estate=estate_id)
    return reviews.all()
    
def IsEstateExists(estate_id):
    return Estate.objects.filter(id=estate_id).exists()

def GetEmployeesForClient(
        estate_id):
    estate = Estate.objects.filter(id=estate_id).last()
    realtors = Employee.objects.filter(category=estate.category)
    return realtors.all()

def CreateEstateReview(
        estate_id,
        client,
        employee):
    estate = Estate.objects.filter(id=estate_id).last()
    estateReview = EstateReview(
        estate=estate,
        client=client,
        realtor=employee
    )
    estateReview.save()

def GetEstateById(estate_id):
    return Estate.objects.filter(id=estate_id).last()