from ..models import Contract, Client

def GetContracts(
        employee=None,
        client=None):
    contract = Contract.objects

    if employee:
        contract = contract.filter(realtor=employee)
    if client:
        contract = contract.filter(client=client)
    return contract.all()

def GetClientsFromContracts(contracts):
    return Client.objects.filter(id__in=contracts.values_list('client'))

def GetAllContracts():
    return Contract.objects.all()

def GetContractsByCategory(category):
    return Contract.objects.filter(estate__category=category).all()