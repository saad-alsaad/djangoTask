from django.test import Client, TestCase
from reservationApp.forms import ReservationForm


class TestForms(TestCase):

    def test_table_reservation_from_is_valid(self):
        form = ReservationForm(data={
            'numberOfSeats': 7,
            'reservationTime': '2020-09-18 01:37:50',
            'reservationDateTimeExpiration': '2020-09-18 01:37:50'
        })

        self.assertTrue(form.is_valid())

    def test_table_reservation_from_invalid_reservation_time(self):
        form = ReservationForm(data={
            'numberOfSeats': 7,
            'reservationTime': '2020-09-18 31:37:50',
            'reservationDateTimeExpiration': '2020-09-18 01:37:50'
        })

        self.assertFalse(form.is_valid())