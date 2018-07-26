from django.test import TestCase
from .models import Hotel
from django.contrib.auth import get_user_model
# Create your tests here.

class HotelModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')
        self.hotel = Hotel.objects.create(name='1-hotel', description='1-body',
                                          owner=self.user, slug='1-hotel')

    def test_get_absolute_url(self):
        #user = get_user_model().objects.create(username='some_user')
        hotel = Hotel.objects.create(name="My tour",owner=self.user,slug='my-tour')
        self.assertIsNotNone(hotel.get_absolute_url())
    

    def test_title_in_hotel(self):
        response = self.client.get(self.hotel.get_absolute_url())
        self.assertContains(response, self.hotel.name)
    
    def test_body_in_entry(self):
        response = self.client.get(self.hotel.get_absolute_url())
        self.assertContains(response, self.hotel.description)

    def test_invalid_url(self):
        
        response = self.client.get("/0000/00/00/0-invalid/")
        self.assertEqual(response.status_code, 404) #200

