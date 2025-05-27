from ..models import Review

def GetReviews():
    return Review.objects.all()

def CreateReview(client, 
                 grade, 
                 comment):
    review = Review()
    review.client = client
    review.grade = grade
    review.comment = comment
    review.save()
    return review
