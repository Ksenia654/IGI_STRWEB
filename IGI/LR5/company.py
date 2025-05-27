from ..models import CompanyInfo

def GetCompanyInfo():
    return CompanyInfo.objects.order_by("-published").all()