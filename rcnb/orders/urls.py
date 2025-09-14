# rcnb/orders/urls.py

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),  # Orders list page
    path('checkout/', views.create_order, name='create_order'),
    path('checkout/payment/', views.payment_page, name='payment_page'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
]
