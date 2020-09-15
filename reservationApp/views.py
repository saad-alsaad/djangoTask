from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, RegisterForm, RestaurantTableForm, ReservationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Table, TableReservation, Restaurant
from .serializers import TableSerializer, TableReservationSerializer, RestaurantSerializer


def index(request):
    return render(request, 'index.html')

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')

    elif request.method == 'POST':
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
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.password == form.confirmPassword:
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
        form = RegisterForm()

    return render(request, 'registration.html', {'form': form})

def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        restaurantInfo = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurantInfo, many=True)
        return render(request, 'home.html', {'data': serializer.data})

class tableDetails(APIView):
    def get(self, request, id):
        if request.user.is_authenticated:
            TableObj = Table.objects.get(pk=id)
            restaurantInfo = Restaurant.objects.get(pk=TableObj.restaurantId.pk)
            form = ReservationForm()
            return render(request, 'tableDetails.html', {'form': form, 'data': TableObj, 'restaurantData': restaurantInfo})
        else:
            return HttpResponseRedirect('/login/')

    def post(self, request, id):
        if request.user.is_authenticated:
            form = ReservationForm(request.POST)

            if form.is_valid():
                TableObj = Table.objects.get(pk=id)
                if form.cleaned_data['numberOfSeats'] <= TableObj.maxNumberOfSeats:
                    res = TableReservation.objects.create(userId=request.user,
                                                    tableId=TableObj,
                                                    NumberOfSeats=form.cleaned_data['numberOfSeats'],
                                                    reservationTime=form.cleaned_data['reservationTime'],
                                                    expiredReservationTime=form.cleaned_data['reservationDateTimeExpiration'])
                    res.save()
                    messages.success(request, 'Reservation Completed')
                else:
                    messages.error(request, 'exceeded maximum number of seats')
            else:
                messages.info(request, 'Invalid Input')

            return render(request, 'tableDetails.html', {'form': form})
        else:
            return render(request, '/login/')

class tablesList(APIView):
    def get(self, request, fid):
        data = []
        if request.user.is_authenticated:
            restaurantTables = Table.objects.filter(restaurantId=fid)
            restaurantInfo = Restaurant.objects.get(pk=fid)
            serializer = TableSerializer(restaurantTables, many=True)
            print(serializer.data)
            for dt in serializer.data:
                if len(dt['tableReservations']) == 0:
                    data.append(dt)

            return render(request, 'restaurantTables.html', {'data': data, 'restaurantData': restaurantInfo })

    def post(self, request):
        pass

class addTable(APIView):
    def get(self, request):
        if request.user.is_authenticated and request.user.groups.filter(name = 'RestaurantAdmins').exists():
            form = RestaurantTableForm()
            restaurantInfo = Restaurant.objects.all()
            return render(request, 'addTable.html', {'form': form, 'restaurantInfo': restaurantInfo})
        else:
            return render(request, 'index.html')

    def post(self, request):
        if request.user.is_authenticated and request.user.groups.filter(name = 'RestaurantAdmins').exists():
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
