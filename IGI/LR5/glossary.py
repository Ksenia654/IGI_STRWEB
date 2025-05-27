from ..models import Glossary

def GetGlossary():
    return Glossary.objects.order_by("-published").all()