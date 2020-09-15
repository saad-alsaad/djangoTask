from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    country_name = models.CharField(max_length=255)

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    countryId = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class Table(models.Model):
    restaurantId = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    maxNumberOfSeats = models.IntegerField()
    tableNumber = models.IntegerField()

class TableReservation(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    tableId = models.ForeignKey(Table, on_delete=models.CASCADE)
    NumberOfSeats = models.IntegerField()
    reservationTime = models.DateTimeField()
    expiredReservationTime = models.DateTimeField()