from django.urls import path
from . import views

app_name = "home"
urlpatterns = [ 
    
    path("", views.home, name="home"), 
    path("team/", views.team, name="team"),
    path("membership/", views.membership, name="membership"),
    path("contact/", views.contact, name="contact"), 
    path('submit-contact/', views.submit_contact_form, name='submit_contact_form'),
]
