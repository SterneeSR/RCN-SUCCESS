from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path("check-storage/", views.check_storage),
    path("test-cloudinary/", views.test_cloudinary_upload),
    path('', views.product_list, name='product_list'),
    path('suggest/', views.product_suggest, name='product_suggest'),
    path('popular-searches/', views.popular_searches, name='popular_searches'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]