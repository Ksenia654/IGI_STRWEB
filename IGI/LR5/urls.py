from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('company', CompanyView.as_view(), name='company_info_page'),
    path('news', NewsView.as_view(), name='news_page'),
    path('faq', QAView.as_view(), name='qa_page'),
    path('contacts', EmployeesView.as_view(), name='contacts_page'),
    path('policy', PolicyView.as_view(), name = 'policy_page'),
    path('vacancies', VacanciesView.as_view(), name='vacancies_page'),
    path('reviews', Reviews, name='reviews_page'),
    path('promos', PromocodeView.as_view(), name='promocodes_page'),
    path('login', LoginView.as_view(), name='login_page'),
    path('register', RegisterView.as_view(), name='register_page'),
    path('logout', logout_user, name='logout_page'),
    path('private', PrivateInfoView.as_view(), name='private_info_page'),
    path('submit_review', ReviewsView.as_view(), name='submit_review_page'),
    path('estates', EstatesView.as_view(), name='estates_page'),
    path('contracts', ContractsView.as_view(), name='contracts_page'),
    re_path(r'^estate/review/(?P<estate_id>\d+)', EstateReviewView.as_view(), name='estate_review_page'),
    re_path(r'^estate/buy/(?P<estate_id>\d+)', BuyEstateView.as_view(), name='buy_estate_page'),
    path('estates/manage', EstatesCRUDView.as_view(), name='estates_crud_page'),
    path('estates/add', EstatesCRUDView.add, name='estates_add_page'),
    re_path(r'estates/edit/(?P<estate_id>\d+)', EstatesCRUDView.edit, name='estates_edit_page'),
    re_path(r'estates/delete/(?P<estate_id>\d+)', EstatesCRUDView.delete, name='estates_delete_page'),
    path('estates/categories', CategoriesView.as_view(), name='categories_page')
]
