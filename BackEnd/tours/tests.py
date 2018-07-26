from django.test import TestCase
from .models import Tour
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your tests here.

class TourModelTest(TestCase):

    #"""  models test"""
    def test_string_representation(self):
        tour= Tour(name="My Tour name",slug='this test slug',created=timezone.now())
        self.assertEqual(str(tour), tour.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Tour._meta.verbose_name_plural), "تورها") #tours


    #""" views and template test"""
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.user = get_user_model().objects.create(username='')
    
    
    # def test_one_Tour(self):
    #     Tour.objects.create(name='1-name', slug='1-slug', description='this is test ' ,price=121.35)
    #     response = self.client.get('/')
    #     self.assertContains(response, '1-name')
    #     self.assertContains(response, '1-slug')
    #     self.assertContains(response, 'this is test')
    #     self.assertContains(response, 121.35)
    
    def test_get_absolute_url(self):
        #user = get_user_model().objects.create(username='some_user')
        tour = Tour.objects.create(name="My tour")
        self.assertIsNotNone(entry.get_absolute_url())




