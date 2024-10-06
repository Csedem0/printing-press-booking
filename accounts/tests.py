
# Create your tests here.
# booking/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import PrintingPress, Booking
from django.urls import reverse
from datetime import date

class PrintingPressModelTest(TestCase):
    
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.press = PrintingPress.objects.create(
            owner=self.owner,
            name="Press 1",
            location="123 Street",
            contact_info="123456789"
        )

    def test_printing_press_creation(self):
        self.assertEqual(self.press.name, "Press 1")
        self.assertEqual(self.press.owner.username, "owner")

class BookingModelTest(TestCase):
    
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.customer = User.objects.create_user(username="customer", password="password")
        self.press = PrintingPress.objects.create(
            owner=self.owner,
            name="Press 1",
            location="123 Street",
            contact_info="123456789"
        )
        self.booking = Booking.objects.create(
            customer=self.customer,
            printing_press=self.press,
            date=date.today(),
            description="Sample booking"
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.customer.username, "customer")
        self.assertEqual(self.booking.printing_press.name, "Press 1")
        self.assertEqual(self.booking.status, "Pending")

class BookingViewsTest(TestCase):
    
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.customer = User.objects.create_user(username="customer", password="password")
        self.press = PrintingPress.objects.create(
            owner=self.owner,
            name="Press 1",
            location="123 Street",
            contact_info="123456789"
        )
        self.booking = Booking.objects.create(
            customer=self.customer,
            printing_press=self.press,
            date=date.today(),
            description="Sample booking"
        )

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Press 1")

    def test_make_booking_view(self):
        self.client.login(username="customer", password="password")
        response = self.client.get(reverse('make_booking', args=[self.press.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('make_booking', args=[self.press.id]), {
            'date': date.today(),
            'description': "New booking"
        })
        self.assertEqual(response.status_code, 302)  # Redirect to 'my_bookings'

    def test_my_bookings_view(self):
        self.client.login(username="customer", password="password")
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Press 1")

    def test_manage_bookings_view(self):
        self.client.login(username="owner", password="password")
        response = self.client.get(reverse('manage_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample booking")
