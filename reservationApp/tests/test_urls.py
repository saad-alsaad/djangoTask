from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reservationApp.views import Home, TablesList, TableDetails


class TestUrls(SimpleTestCase):

    def test_home_page(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, Home)

    def test_table_details_page(self):
        url = reverse('tableDetails', args=[1])
        self.assertEqual(resolve(url).func.view_class, TableDetails)

    def test_restaurant_tables_page(self):
        url = reverse('restaurantTables', args=[1])
        self.assertEqual(resolve(url).func.view_class, TablesList)