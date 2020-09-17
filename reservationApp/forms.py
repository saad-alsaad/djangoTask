from datetime import datetime

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control', 'placeholder' : 'Enter Your Username'}
    ))

    password = forms.CharField(label='password', max_length=255, widget=forms.PasswordInput(attrs={
        'class' : 'form-control', 'placeholder' : 'Enter Your Password'}
    ))


class RegisterForm(forms.Form):

    first_name = forms.CharField(label='First Name', max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control', 'placeholder' : 'Enter Your First Name'}
    ))

    last_name = forms.CharField(label='Last Name', max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control', 'placeholder' : 'Enter Your Last Name'}
    ))

    username = forms.CharField(label='username', max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control', 'placeholder' : 'Enter Your username'}
    ))

    email = forms.CharField(label='Email', max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control', 'type' : 'email', 'placeholder' : 'Enter Your email'}
    ))

    # country = forms.CharField(label='Country', max_length=10, widget=forms.ComboField(fields=['Palestine']))

    password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(attrs={
        'class' : 'form-control', 'placeholder' : 'Enter Your Password'}
    ))

    confirmPassword = forms.CharField(label='Confirm Password', max_length=255, widget=forms.PasswordInput(attrs={
        'class' : 'form-control', 'placeholder' : 'Password Confirmation'}
    ))


class ReservationForm(forms.Form):
    numberOfSeats = forms.IntegerField(label='Max Number Of Seats', min_value=1, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Number Of Seats'}))

    reservationTime = forms.DateTimeField(label='reservationTime', initial=datetime.now(), widget=forms.DateTimeInput(attrs={'type': 'datetime'}))
    reservationDateTimeExpiration = forms.DateTimeField(label='Date Time Reservation expiration', initial=datetime.now(), widget=forms.DateTimeInput(attrs={'type': 'datetime'}))


class RestaurantTableForm(forms.Form):
    maxNumberOfSeats = forms.IntegerField(label='Max Number Of Seats', max_value=100000, min_value=1, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Maximum Number Of Seats'}))
    tableNumber = forms.IntegerField(label='Table Number', max_value=100000, min_value=1, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Table Number'}))