from ..models import Vacancy

def GetOpenVacancies():
    return Vacancy.objects.filter(is_open=True).order_by("published_date").all()