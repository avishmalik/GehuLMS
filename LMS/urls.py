from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path('leaves/searchLeavesData',views.bluecollar,name = 'searchLeavesData'),
    path('dashboard/dashboard_index',views.hod,name ='dashboard/dashboard_index'),
    path('login/',views.login_view,name = 'login_view'),
    path('logout/',views.logout_view,name='logout'),
    path('user/change-password/',views.changepassword,name='changepassword'),
    path('create-user/',views.register_user_view,name='register'),
]