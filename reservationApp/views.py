from datetime import datetime, date, timedelta
from time import time

from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import now
from django.views import View
from .forms import LoginForm, RegisterForm, RestaurantTableForm, ReservationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Table, TableReservation, Restaurant, Country
from .serializers import TableSerializer, TableReservationSerializer, RestaurantSerializer
from secrets import compare_digest


class UserLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/home/')
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                messages.info(request, 'Wrong username or password')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})


class UserRegistration(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/home/')
        form = RegisterForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            if compare_digest(form.password, form.confirmPassword):
                if User.objects.filter(username=form.username).exists():
                    messages.info(request, 'username already exists')
                elif User.objects.filter(username=form.username).exists():
                    messages.info(request, 'email already exists')
                else:
                    user = User.objects.create_user(username=form.cleaned_data['username'],
                                                    password=form.cleaned_data['password'],
                                                    email=form.cleaned_data['email'],
                                                    first_name=form.cleaned_data['first_name'],
                                                    last_name=form.cleaned_data['last_name'])
                    user.save()
            else:
                messages.info(request, 'Password not matched')

            return HttpResponseRedirect('/home/')
        else:
            messages.error(request, 'Invalid Input')
            return render(request, 'registration.html', {'form': form})


class Home(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        else:
            restaurant_info = Restaurant.objects.all()
            serializer = RestaurantSerializer(restaurant_info, many=True)
            for dt in serializer.data:
                country = Country.objects.filter(pk=dt['countryId'])
                print(dt['name'])
                print(country[0].country_name)
                dt['country_name'] = country[0].country_name

            return render(request, 'home.html', {'data': serializer.data})

    def post(self):
        pass


class TableDetails(APIView):
    def get(self, request, id):
        if request.user.is_authenticated:
            table_obj = Table.objects.get(pk=id)
            restaurant_info = Restaurant.objects.get(pk=table_obj.restaurantId.pk)
            form = ReservationForm()
            return render(request, 'tableDetails.html',
                          {'form': form, 'data': table_obj, 'restaurantData': restaurant_info})
        else:
            return HttpResponseRedirect('/login/')

    def post(self, request, id):
        if request.user.is_authenticated:
            form = ReservationForm(request.POST)
            table_obj = Table.objects.get(pk=id)
            restaurant_info = Restaurant.objects.get(pk=table_obj.restaurantId.pk)
            if form.is_valid():
                if form.cleaned_data['numberOfSeats'] <= table_obj.maxNumberOfSeats:
                    res = TableReservation.objects.create(userId=request.user,
                                                          tableId=table_obj,
                                                          NumberOfSeats=form.cleaned_data['numberOfSeats'],
                                                          reservationTime=form.cleaned_data['reservationTime'],
                                                          expiredReservationTime=form.cleaned_data[
                                                              'reservationDateTimeExpiration'])
                    res.save()
                    messages.success(request, 'Reservation Completed')
                else:
                    messages.error(request, 'exceeded maximum number of seats')
            else:
                messages.info(request, 'Invalid Input')

            return render(request, 'tableDetails.html', {'form': form, 'data': table_obj,
                                                         'restaurantData': restaurant_info})
        else:
            return render(request, '/login/')


class TablesList(APIView):
    def get(self, request, fid):
        data = []
        if request.user.is_authenticated:
            restaurant_tables = Table.objects.filter(restaurantId=fid)
            restaurant_info = Restaurant.objects.get(pk=fid)
            serializer = TableSerializer(restaurant_tables, many=True)
            for dt in serializer.data:
                reservations = TableReservation.objects.filter(tableId=dt['id'],
                                                               expiredReservationTime__lt=datetime.now()).order_by(
                                                                '-expiredReservationTime')
                if reservations.count() == 0:
                    data.append(dt)

            return render(request, 'restaurantTables.html', {'data': data, 'restaurantData': restaurant_info})

    def post(self, request):
        pass


class AddTable(APIView):
    def get(self, request):
        if request.user.is_authenticated and request.user.groups.filter(name='RestaurantAdmins').exists():
            form = RestaurantTableForm()
            restaurant_info = Restaurant.objects.all()
            return render(request, 'addTable.html', {'form': form, 'restaurantInfo': restaurant_info})
        else:
            return render(request, 'index.html')

    def post(self, request):
        if request.user.is_authenticated and request.user.groups.filter(name='RestaurantAdmins').exists():
            form = RestaurantTableForm(request.POST)
            serializer = TableSerializer(data=form.data)
            if serializer.is_valid():
                serializer.save()
                messages.success(request, 'Completed')
            else:
                messages.info(request, 'Failed to save serializer')
            return render(request, 'addTable.html', {'form': form})
        else:
            return render(request, 'index.html')


def index(request):
    return render(request, 'index.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
