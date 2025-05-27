from ..models import Article

def GetArticle():
    return Article.objects.order_by("-published").first()

def GetArticles():
    return Article.objects.order_by("-published").all()