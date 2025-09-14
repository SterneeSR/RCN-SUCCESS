# rcnb/users/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if the user is trying to access a page that requires an address
            is_checkout_path = request.path.startswith('/orders/checkout/')
            
            # Check if the user has any saved addresses
            has_address = request.user.addresses.exists()

            if not has_address and is_checkout_path:
                # If they have no address and are trying to checkout, redirect them
                # to the address book to add one.
                messages.info(request, "Please add a shipping address before proceeding to checkout.")
                redirect_url = f"{reverse('users:address_book')}?next={request.path}"
                return redirect(redirect_url)

        response = self.get_response(request)
        return response