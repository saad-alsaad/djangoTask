from datetime import datetime

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Table, TableReservation, Restaurant, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    countries = SerializerMethodField()
    def get_countries(self, obj):
        countries = Country.objects.filter(pk=obj.countryId.pk)
        serializer = CountrySerializer(countries, many=True)
        return serializer.data

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'city', 'address', 'countryId', 'countries')


class TableReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableReservation
        fields = ('userId', 'tableId', 'tableId', 'NumberOfSeats', 'reservationTime', 'expiredReservationTime')

class TableSerializer(serializers.ModelSerializer):
    tableReservations = SerializerMethodField()
    def get_tableReservations(self, obj):
        # today_start = datetime.combine(today, time())
        reservations = TableReservation.objects.filter(tableId=obj.pk,expiredReservationTime__lt=datetime.now()).order_by('-expiredReservationTime')
        serializer = TableReservationSerializer(reservations, many=True)
        return serializer.data

    class Meta:
        model = Table
        fields = ('id', 'restaurantId', 'maxNumberOfSeats', 'tableNumber', 'tableReservations')
