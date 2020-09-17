from datetime import datetime

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Table, TableReservation, Restaurant, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'city', 'address', 'countryId')


class TableReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableReservation
        fields = ('userId', 'tableId', 'tableId', 'NumberOfSeats', 'reservationTime', 'expiredReservationTime')


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ('id', 'restaurantId', 'maxNumberOfSeats', 'tableNumber')
