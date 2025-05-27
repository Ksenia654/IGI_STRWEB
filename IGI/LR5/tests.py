from django.test import TestCase

import os
import shutil

from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse
import datetime

from django.conf import settings
from realtorBack.models import User, Client as cl


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.prev_media = settings.MEDIA_ROOT
        cls.user_model = get_user_model()
        cls.user = Client()
        cls.user1 =  cls.user_model.objects.create_superuser(username="User1")
        cls.user.force_login(cls.user1)

    def test_user_register(self):
        form_data = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'testov',
            'email' : 'test@bsuir.by',
            'password1': 'ergergerwg',
            'password2' :'ergergerwg',
            'birth_date' : datetime.date.today()-datetime.timedelta(days=20*365),
            'phone_number': "+375(44)1235455"
        }
        self.user.post(reverse('register_page'), data=form_data)
        self.assertEqual(self.user_model.objects.filter(username=form_data['username']).exists(), True)
        
    def test_login(self):
        form_data = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'testov',
            'email' : 'test@bsuir.by',
            'password1': 'ergergerwg',
            'password2' :'ergergerwg',
            'birth_date' : datetime.date.today()-datetime.timedelta(days=20*365),
            'phone_number': "+375(44)1235455"
        }
        self.user.post(reverse('register_page'), data=form_data)
        self.assertEqual(self.user_model.objects.filter(username=form_data['username']).exists(), True)
        form_data = {
            'username': 'test',
            'password': 'ergergerwg',
        }
        self.assertEqual(self.user.post(reverse('login_page'), data=form_data).status_code, 302)
        
    def test_register(self):
        response = self.user.get(reverse('register_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')
        
    def test_user_login(self):
        form_data = {
            'username': 'test',
            'password' : 'ergergerwg',
        }
        response = self.user.post(reverse('login_page'), data=form_data)
        self.assertEqual(response.status_code, 200)
    
    def test_login2(self):
        form_data = {
            'username': 'test',
            'password' : 'egerf',
        }
        response = self.user.get(reverse('login_page'), data=form_data)
        self.assertEqual(response.status_code, 200)
    
    def test_user_logout(self):
        form_data = {
            'username': 'test',
            'password' : 'ewtrwe',
        }
        response = self.user.post(reverse('login_page'), data=form_data)
        self.assertEqual(response.status_code, 200)

        response = self.user.post(reverse('logout_page'))
        self.assertEqual(response.status_code, 302)

    def test_qa(self):
        response = self.user.get(reverse('qa_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/qa.html')
    
    def test_news(self):
        response = self.user.get(reverse('news_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/news.html')
    
    def test_reviews(self):
        response = self.user.get(reverse('reviews_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/reviews.html')
    
    def test_submit_review(self):
        form_data = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'testov',
            'email' : 'test@bsuir.by',
            'password1': 'ergergerwg',
            'password2' :'ergergerwg',
            'birth_date' : datetime.date.today()-datetime.timedelta(days=20*365),
            'phone_number': "+375(44)1235455"
        }
        self.user.post(reverse('register_page'), data=form_data)
        self.assertEqual(self.user_model.objects.filter(username=form_data['username']).exists(), True)

        response = self.user.get(reverse('submit_review_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/submit_review.html')

        form_data = {
            'grade': 11,
            'description' : 'fdsf',
        }
        response = self.user.post(reverse('submit_review_page'),data=form_data)
        self.assertEqual(response.status_code, 200)

        form_data = {
            'grade': '-1',
            'description' : 'fdsf',
        }
        response = self.user.post(reverse('submit_review_page'),data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_policy(self):
        response = self.user.get(reverse('policy_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/policy.html')
    
    def test_promocodes(self):
        response = self.user.get(reverse('promocodes_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/promocodes.html')

    def test_vacancies(self):
        response = self.user.get(reverse('vacancies_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/vacancies.html')

    def test_main_page(self):
        form_data = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'testov',
            'email' : 'test@bsuir.by',
            'password1': 'ergergerwg',
            'password2' :'ergergerwg',
            'birth_date' : datetime.date.today()-datetime.timedelta(days=20*365),
            'phone_number': "+375(44)1235455"
        } 
        self.user.post(reverse('register_page'), data=form_data)
        self.assertEqual(self.user_model.objects.filter(username=form_data['username']).exists(), True)

        response = self.user.get(reverse('main_page_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/main.html')
    
    def test_contacts(self):
        response = self.user.get(reverse('contacts_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/contacts.html')
        form_data = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'testov',
            'email' : 'test@bsuir.by',
            'password1': 'ergergerwg',
            'password2' :'ergergerwg',
            'birth_date' : datetime.date.today()-datetime.timedelta(days=20*365),
            'phone_number': "+375(44)1235455"
        }
        self.user.post(reverse('register_page'), data=form_data)
        self.assertEqual(self.user_model.objects.filter(username=form_data['username']).exists(), True)

    def test_company_info(self):
        response = self.user.get(reverse('private_info_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'private/user.html')
        form_data = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'testov',
            'email' : 'test@bsuir.by',
            'password1': 'ergergerwg',
            'password2' :'ergergerwg',
            'birth_date' : datetime.date.today()-datetime.timedelta(days=20*365),
            'phone_number': "+375(44)1235455"
        }
        self.user.post(reverse('register_page'), data=form_data)
        self.assertEqual(self.user_model.objects.filter(username=form_data['username']).exists(), True)
        response = self.user.get(reverse('private_info_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/private_info.html')