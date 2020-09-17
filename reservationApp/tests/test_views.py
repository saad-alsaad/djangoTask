from django.test import SimpleTestCase, Client, TestCase
from django.urls import reverse, resolve

from reservationApp.models import Restaurant, Country, Table


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.table_details_url = reverse('tableDetails', args=[1])
        self.add_table_url = reverse('addTable')
        self.country = Country.objects.create(country_name='Palestine')
        self.restaurant = Restaurant.objects.create(
            name='restaurant1',
            city='Ramallah',
            address='Ersal ST',
            countryId=self.country
        )
        # self.table = Table.objects.create(
        #     maxNumberOfSeats=10,
        #     tableNumber=1,
        #     restaurantId=self.restaurant
        # )

    def test_login_get(self):
        client = Client()

        response = client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_home_get(self):
        client = Client()

        response = client.get(self.home_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_table_details_get(self):
        client = Client()

        response = client.get(self.table_details_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_add_table_post_new_table(self):
        response = self.client.post(self.add_table_url, {
            'maxNumberOfSeats': 20,
            'tableNumber': 5,
            'restaurantId': self.restaurant.pk
        })

        self.assertEquals(response.status_code, 200)
        # self.assertEquals(self.restaurant.tables.first().tableNumber, 5)

    def test_add_table_post_no_data(self):
        response = self.client.post(self.add_table_url)

        self.assertEquals(response.status_code, 200)
        # check no table has been added