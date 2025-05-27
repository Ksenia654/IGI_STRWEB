from ..models import Promocode

def ActivePromocodeExists(promo):
    return Promocode.objects.filter(code=promo, is_active=True).exists()

def GetPromocode(promo):
    return Promocode.objects.filter(code=promo).last()

def GetActivePromocodes():
    return Promocode.objects.filter(is_active=True).all()