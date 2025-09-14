# rcnb/users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.email_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('addresses/', views.address_book, name='address_book'),
    path('addresses/edit/<int:address_id>/', views.edit_address, name='edit_address'),
    path('addresses/delete/<int:address_id>/', views.delete_address, name='delete_address'),
]