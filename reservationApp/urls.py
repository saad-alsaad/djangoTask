from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.Home.as_view(), name='home'),
    path('tableDetails/<int:id>/', views.TableDetails.as_view(), name='tableDetails'),
    path('restaurantTables/<int:fid>/', views.TablesList.as_view(), name='restaurantTables'),
    path('register/', views.UserRegistration.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.logout_user, name='logoutUser'),
    path('addTable/', views.AddTable.as_view(), name='addTable'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
