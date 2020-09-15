from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('tableDetails/<int:id>/', views.tableDetails.as_view(), name='tableDetails'),
    path('restaurantTables/<int:fid>/', views.tablesList.as_view(), name='tablesList'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('addTable/', views.addTable.as_view(), name='addTable'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
