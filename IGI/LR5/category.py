from ..models import Contract
from ..models import EstateCategory

def GetCategories():
    return EstateCategory.objects.all()