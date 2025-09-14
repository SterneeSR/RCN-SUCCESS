from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ContactMessage


# Create your views here.

def home(request):
    return render(request, "home/home.html")

def team(request):
    return render(request, "home/team.html")

def contact(request):
    return render(request, "home/contact.html")

def membership(request):
    return render(request, "home/membership.html")

def submit_contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Basic validation
        if not all([name, email, message]):
            return JsonResponse({'success': False, 'message': 'All required fields must be filled.'})

        ContactMessage.objects.create(
            name=name,
            contact_number=contact_number,
            email=email,
            message=message
        )
        return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})