from ..models import Client, Contract, EstateReview, Estate

def GetBoughtEstate(client):
    return Contract.objects.filter(client=client).values_list('estate').distinct()

def BuyEstate(estate_id, 
                realtor, 
                client, 
                activated_promo=None):
    estate = Estate.objects.filter(id=estate_id).last()
    contract = Contract(
        realtor=realtor,
        client=client,
        estate=estate,
        activated_promo=activated_promo,
    )
    estate.owner=client
    estate.save()
    contract.save()

def ReviewEstate(client,
                    realtor,
                    estate,
                    description):
    review = EstateReview.objects.create(
        client=client,
        realtor=realtor,
        estate=estate,
        description=description
    )
    review.save()

def IsClient(user):
    return Client.objects.filter(profile=user).exists()

def GetClientUser(user):
    return Client.objects.filter(profile=user).last()

def CreateClient(user):
    client = Client()
    client.profile = user
    client.save()
    return client

def IsEstateSold(estate_id):
    estate = Estate.objects.filter(id=estate_id).last()
    return Contract.objects.filter(estate=estate).exists()