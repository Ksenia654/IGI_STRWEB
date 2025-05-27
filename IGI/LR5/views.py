from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from realtorBack.db.article import GetArticle, GetArticles
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from realtorBack.db.company import *
from realtorBack.views import *
from realtorBack.db.glossary import *
from realtorBack.db.contact import *
from realtorBack.db.vacancy import *
from realtorBack.db.reviews import *
from realtorBack.db.promocode import *
from realtorBack.db.client import *
from realtorBack.db.employee import *
from realtorBack.db.category import *
from realtorBack.db.estate import *
from realtorBack.db.contract import *
from .forms import *
import requests
from realtorBack.views import *

import logging
logger = logging.getLogger('hospital')

class MainView(View):
    template_path = 'general/main.html'

    def get(self, request):
        try:
            art = GetArticle()
        except:
            art = None

        try:
            dog_image = requests.get("https://dog.ceo/api/breeds/image/random").json()['message'] 
        except:
            dog_image = None
        try:
            cat_fact = requests.get("https://catfact.ninja/fact").json()['fact'] 
        except:
            cat_fact = "Cats are great!"

        return render(
            request, 
            self.template_path,
            {
                "articles": art,
                "dog_image": dog_image,
                "cat_fact": cat_fact
            }
        )
    
class CompanyView(View):
    template_path = 'general/company.html'

    def get(self, request):
        try:
            company_info = GetCompanyInfo()
        except:
            company_info = None

        users_stats = GetUsersStats()
        average_price, median_price, mode_price = GetPurchaseStats()
        plot1, plot2 = GetPlots()

        return render(
            request,
            self.template_path,
            {
                "infos": company_info,
                "users_stats": users_stats,
                "average_price": average_price,
                "median_price": median_price,
                "mode_price": mode_price,
                "plot1": plot1,
                "plot2": plot2
            }
        )
    
class NewsView(View):
    template_path='general/news.html'

    def get(self, request):
        try:
            news = GetArticles()
        except:
            news = None

        logger.info("News Page is visited")

        return render(
            request,
            self.template_path,
            {
                "articles": news,
            }
        )
    
class QAView(View):
    template_path='general/qa.html'

    def get(self, request):
        try:
            glossary = GetGlossary()
        except:
            glossary = None

        logger.info("QA Page is visited")

        return render(
            request,
            self.template_path,
            {
                "glossary": glossary
            }
        )
    
class EmployeesView(View):
    template_path='general/contacts.html'

    def get(self, request):
        try:
            employees = GetContacts()
        except:
            employees = None
        
        logger.info("Contacts Page is visited")
        
        return render(
            request,
            self.template_path,
            {
                "employees": employees
            }
        )
    
class PolicyView(View):
    template_path='general/policy.html'

    def get(self, request):
        logger.info("Policy Page is visited")
        return render(request, self.template_path)
    
class VacanciesView(View):
    template_path='general/vacancies.html'

    def get(self, request):
        try:
            vacancies = GetOpenVacancies()
        except:
            vacancies = None

        logger.info("Vacancies Page is visited")

        return render(
            request,
            self.template_path,
            {
                "vacancies": vacancies
            }
        )

def Reviews(request):
    try:
        reviews = GetReviews()
    except:
        reviews = None
    
    logger.info("Reviews Page is visited")
    return render(
        request,
        'general/reviews.html',
        {
            "reviews": reviews
        }
    )
    
class ReviewsView(View, LoginRequiredMixin):
    template_path='private/submit_review.html'
    form=ReviewForm

    def get(self, request):
        form = self.form()

        logger.info("Submit review Page is visited")

        return render(
            request,
            self.template_path,
            {
                "form": form
            }
        )
    
    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            newForm = self.form()
            return render(
                request,
                self.template_path,
                {
                    'form': newForm,
                    'message': "Type a valid data"
                }
            )
        grade = form.cleaned_data['grade']
        comment = form.cleaned_data['comment']

        try:
            CreateReview(GetClientUser(request.user), grade, comment)
            return redirect('reviews_page')
        except:
            newForm = self.form()
            return render(
                request,
                self.template_path,
                {
                    'form': newForm,
                    'message': 'something went wrong'
                }
            )
    
class PromocodeView(View):
    template_path='general/promocodes.html'

    def get(self, request):
        try:
            promos = GetActivePromocodes()
        except:
            promos = None

        logger.info("Promos Page is visited")

        return render(
            request,
            self.template_path,
            {
                "promos": promos
            }
        )
    
class LoginView(View):
    template_path = 'auth/login.html'  
    form = LoginForm

    def get(self, request):
        form = self.form()
        logger.info("Login Page is visited")

        if request.user.is_authenticated:
            return redirect('/')
        return render(
            request,
            self.template_path,
            {
                'form': form,
                "message": "Input form"
            }
        )
    
    def post(self, request):
        form = self.form(request.POST)
        logger.info("Login form is posted")
        if request.user.is_authenticated:
            return redirect('/')
        if not form.is_valid():
            newForm = self.form()
            return render(
                request,
                self.template_path,
                {
                    'form': newForm,
                    'message': "Type a valid data"
                }
            )
        try:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("main_page")
            
            newForm = self.form()
            return render(
                request,
                self.template_path,
                {
                    'form': newForm,
                    'message': 'wrong username or password'
                }
            )
        except:
            return render(
                request, 
                self.template_path,
                {
                    'form': form,
                    "message": "Type a valid data"
                }
            )
        
class RegisterView(View):
    template_name = 'auth/register.html'
    form = RegisterForm
    success_url = reverse_lazy('main_page')

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = self.form()
        logger.info("register Page is visited")
        return render(
            request, 
            self.template_name, 
            { 
                'form': form, 
                "message": "Fill the form"
            }
        )

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        logger.info("register Page is posted")
        if request.user.is_authenticated:
            return redirect('/')
        
        if not form.is_valid():
            newForm = self.form()
            return render(
                request, 
                self.template_name,
                { 
                    'form': newForm, 
                    "message": f"Registration failed. Invalid {form.errors.as_data()}."
                }
            )
        try:
            user = form.save()
            CreateClient(user)

            login(request, user)
            return redirect('main_page')
        except:
            return render(
                request, 
                self.template_name,
                { 
                    'form': form, 
                    "message": "Registration failed. Please try again."
                }
            )
        
def logout_user(request):
    if not request.user.is_authenticated:
        redirect('login_page')

    logout(request)
    return redirect('main_page')

class PrivateInfoView(View):
    template_path='private/user.html'
    login_utl='/login'

    def get(self, request):
        is_employee = IsEmployee(request.user)
        return render(
            request,
            self.template_path,
            {
                "is_employee": is_employee
            }
        )
    
class EstatesView(View):
    template_path='estate/estates.html'
    
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('private_info_page')
        if request.user.is_authenticated and IsEmployee(request.user):
            employee = GetEmployee(request.user)
            estates = GetFilteredEstates(
                category=employee.category,
                free=False
            )
            return render(
                request,
                self.template_path,
                {
                    "estates": estates,
                    "is_employee": True,
                    "is_client": False
                }
            )
        else:
            is_client = False
            if request.user.is_authenticated:
                is_client = True
            min_cost = request.GET.get('min_cost')
            max_cost = request.GET.get('max_cost')
            category = request.GET.get('category')

            estates = GetFilteredEstates(
                min_cost=min_cost, 
                max_cost=max_cost, 
                category=category,
                free=True
            )
            categories = GetCategories()

            return render(
                request,
                self.template_path,
                {
                    "estates": estates,
                    "categories": categories,
                    "is_employee": False,
                    "is_client": is_client
                }
            )

    def post(self, request):
        if request.user.is_superuser:
            return redirect('private_info_page')
        selected_estate=request.POST.get('estate_select')
        return redirect(f'estate/review/{selected_estate}')
    
class EstateReviewView(LoginRequiredMixin, View):
    template_path='estate/reviews.html'

    class EstatesView(View):
        template_path = 'estate/estates.html'

        def get(self, request):
            if request.user.is_authenticated and request.user.is_superuser:
                return redirect('private_info_page')
            if request.user.is_authenticated and IsEmployee(request.user):
                employee = GetEmployee(request.user)
                estates = GetFilteredEstates(
                    category=employee.category,
                    free=False
                )
                return render(
                    request,
                    self.template_path,
                    {
                        "estates": estates,
                        "is_employee": True,
                        "is_client": False
                    }
                )
            else:
                is_client = False
                if request.user.is_authenticated:
                    is_client = True
                min_cost = request.GET.get('min_cost')
                max_cost = request.GET.get('max_cost')
                category = request.GET.get('category')

                estates = GetFilteredEstates(
                    min_cost=min_cost,
                    max_cost=max_cost,
                    category=category,
                    free=True
                )
                categories = GetCategories()

                return render(
                    request,
                    self.template_path,
                    {
                        "estates": estates,
                        "categories": categories,
                        "is_employee": False,
                        "is_client": is_client
                    }
                )

        def post(self, request):
            if request.user.is_superuser:
                return redirect('private_info_page')
            selected_estate = request.POST.get('estate_select')
            return redirect(f'estate/review/{selected_estate}')
    def GetEmployeeReviews(self, user, estate_id):
        try:
            employee = GetEmployee(user)
            reviews = GetEstateReviews(
                employee=employee,
                estate_id=estate_id
            )
        except:
            reviews=None
        return reviews

    def GetClientReviews(self, user, estate_id):
        try:
            client = GetClientUser(user)
            reviews = GetEstateReviews(
                client=client,
                estate_id=estate_id
            )
        except:
            reviews=None
        return reviews

    def get(self, request, estate_id):
        if not IsEstateExists(estate_id):
            return redirect('/')
        if request.user.is_superuser:
            return redirect('private_info_page')
        if IsEmployee(request.user):
            try:
                reviews = self.GetEmployeeReviews(
                    request.user, 
                    estate_id
                )
            except:
                reviews = None

            return render(
                request,
                self.template_path,
                {
                    "estate_id": estate_id,
                    "reviews": reviews,
                    "is_client": False
                }
            )
        else:
            try:
                reviews = self.GetClientReviews(
                    request.user,
                    estate_id
                )
                realtors = GetEmployeesForClient(
                    estate_id
                )
            except:
                reviews = None
                realtors = None
            
            return render(
                request,
                self.template_path,
                {
                    "estate_id": estate_id,
                    "reviews": reviews,
                    "employees": realtors,
                    "is_client": True
                }
            )
        
    def post(self, request, estate_id):
        if not IsEstateExists(estate_id):
            return redirect('/')
        if request.user.is_superuser:
            return redirect('private_info_page')
        
        if IsEmployee(request.user):
            return self.get(request, estate_id)
        selected_realtor=request.POST.get('realtor_select')
        if selected_realtor is None:
            return redirect('/estates')
        try:
            employee = GetEmployeeById(selected_realtor)
            CreateEstateReview(
                estate_id,
                GetClientUser(request.user),
                employee)
            return self.get(request, estate_id)
        except:
            return redirect('/estates')

class BuyEstateView(LoginRequiredMixin, View):
    template_path='estate/buy.html'

    def get(self, request, estate_id):
        print(f"Получен estate_id: {estate_id}")
        if not IsEstateExists(estate_id):
            return redirect('/')

        if request.user.is_superuser:
            return redirect('private_info_page')
    
        if IsEmployee(request.user):
            return redirect('private_info_page')

      #  if IsEstateSold(estate_id):
         #   return redirect('/')
        try:
            realtors = GetEmployeesForClient(
                estate_id
            )
        except Exception as e:
            logger.error(f"Ошибка при получении риэлторов: {e}")
            realtors = None
        
        return render(
            request,
            self.template_path,
            {
                "estate_id": estate_id,
                "realtors": realtors,
            }
        )
    
    def post(self, request, estate_id):
        if not IsEstateExists(estate_id):
            return redirect('/')
        if IsEstateSold(estate_id):
            return redirect('/')
        
        if request.user.is_superuser:
            return redirect('private_info_page')
        
        if not IsEmployee(request.user):
            realtor = request.POST.get('realtor_select')
            promocode = request.POST.get('promocode')
            if not ActivePromocodeExists(promocode):
                BuyEstate(
                    estate_id, 
                    GetEmployeeById(realtor), 
                    GetClientUser(request.user)
                )
            try:
                promo = GetPromocode(promocode)
                estate = GetEstateById(estate_id)
                if promo.category != estate.category:
                    return redirect('/estates')
                BuyEstate(
                    estate_id, 
                    GetEmployeeById(realtor), 
                    GetClientUser(request.user),
                    promo
                )
            except:
                return redirect('/')
            return redirect('private_info_page')
        else:
            return redirect('private_info_page')
        
class ContractsView(View, LoginRequiredMixin):
    template_path='estate/contracts.html'

    def GetContractsEmployee(self, request):
        try:
            contracts = GetContracts(employee=GetEmployee(request.user))
            clients = GetClientsFromContracts(contracts)
            return render(
                request,
                self.template_path,
                {
                    "contracts": contracts,
                    "clients": clients,
                    "is_employee": True
                }
            )
        except:
            return redirect('private_info_page')
        
    def GetContractsClient(self, request):
        try:
            contracts = GetContracts(client=GetClientUser(request.user))
            return render(
                request,
                self.template_path,
                {
                    "contracts": contracts,
                    "is_employee": False
                }
            )
        except:
            return redirect('private_info_page')

    def get(self, request):
        if request.user.is_superuser:
            return redirect('private_info_page')
        
        if IsEmployee(request.user):
            return self.GetContractsEmployee(request)
        else:
            return self.GetContractsClient(request)
        
class EstatesCRUDView(LoginRequiredMixin, View):
    template_path = 'admin/estates_crud.html'

    def get(self, request):
        if not request.user.is_superuser:
            return redirect('main_page')

        estates = GetFilteredEstates(free=True)
        
        return render(
            request,
            self.template_path,
            {
                "estates": estates
            }
        )
    
    def delete(request, estate_id):
        if not request.user.is_superuser:
                return redirect('main_page')
        try:
            category = Estate.objects.get(id=estate_id)
        except:
            redirect('main_page')
        category.delete()
        return redirect('estates_crud_page')
    
    def edit(request, estate_id):
        if not request.user.is_superuser:
                return redirect('main_page')
        
        instance = get_object_or_404(Estate, id=estate_id)
        if request.method == 'POST':
            form = EstateForm(request.POST, instance=instance)
            if form.is_valid():
                obj = form.save()
                obj.save()
            else:
                return render(
                    request, 
                    'admin/estate_edit.html',
                    {
                        'form': form, 
                        "message": f"Error, try again."
                    }
                )
        else:
            form = EstateForm(instance=instance)
            return render(
                request, 
                'admin/estate_edit.html',
                {
                    'form': form, 
                    "message": f"Fill the form."
                }
            )
        
        return redirect('estates_crud_page')
    
    def add(request):
        if not request.user.is_superuser:
                return redirect('main_page')
        
        if request.method == 'POST':
            form = EstateForm(request.POST,)
            if form.is_valid():
                obj = form.save()
                obj.save()
            else:
                return render(
                    request, 
                    'admin/estates_add.html',
                    {
                        'form': form, 
                        "message": f"Error, try again."
                    }
                )
        else:
            form = EstateForm()
            return render(
                request, 
                'admin/estates_add.html',
                {
                    'form': form, 
                    "message": f"Fill the form."
                }
            )
        
        return redirect('estates_crud_page')
    
class CategoriesView(View):
    template_path='estate/categories.html'

    def get(self, request):
        try:
            categories=GetCategories()
        except:
            categories=None
        
        return render(
            request,
            self.template_path,
            {
                "categories": categories
            }
        )