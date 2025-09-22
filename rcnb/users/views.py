# rcnb/users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UserUpdateForm, AddressForm
from .models import Address
from django.contrib.auth.hashers import make_password

# Email verification imports
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
import logging

logger = logging.getLogger(__name__)


# ------------------- Register -------------------
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Temporarily store user data in the session
            request.session['unverified_user'] = {
                'email': email,
                'password': make_password(password),  # Store hashed password
            }

            # Create a temporary user object to generate the token
            temp_user = User(username=email, email=email)
            
            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Activate Your Account'
            message = render_to_string('users/email_verification_email.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(email)),
                'token': default_token_generator.make_token(temp_user),
            })

            try:
                send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                return render(request, 'users/email_verification_sent.html')
            except Exception as e:
                logger.error(f"Error sending verification email: {e}")
                messages.error(request, "Could not send verification email. Please try again later.")
                
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


# ------------------- Email Verification -------------------
def verify_email(request, uidb64, token):
    try:
        email = force_str(urlsafe_base64_decode(uidb64))
        temp_user = User(username=email, email=email)
    except (TypeError, ValueError, OverflowError):
        return render(request, 'users/email_verification_invalid.html')

    if default_token_generator.check_token(temp_user, token):
        user_data = request.session.get('unverified_user')
        if not user_data or user_data.get('email') != email:
            messages.error(request, "Verification link is invalid or has expired. Please register again.")
            return redirect('users:register')

        # Create the user now that the email is verified
        user = User.objects.create_user(
            username=user_data['email'],
            email=user_data['email'],
            password=user_data['password'] # This is already hashed
        )
        user.is_active = True
        user.save()
        
        # Clean up session
        del request.session['unverified_user']

        # Log the user in
        login(request, user)
        messages.success(request, 'Your email has been verified and your account is created! You are now logged in.')
        return redirect('products:product_list')
    else:
        return render(request, 'users/email_verification_invalid.html')

# (The rest of your views.py file remains the same)
# ------------------- Email Login -------------------
def email_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    return redirect('products:product_list')
                else:
                    messages.error(request, "Invalid credentials.")
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


# ------------------- Profile Page -------------------
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            # Check if the email has been changed
            if 'email' in user_form.changed_data:
                user = user_form.save(commit=False)
                user.is_active = False
                user.profile.email_verified = False
                user.save()

                # Send verification email for the new address
                current_site = get_current_site(request)
                mail_subject = 'Verify Your New Email Address'
                message = render_to_string('users/email_verification_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

                messages.warning(request, 'A verification link has been sent to your new email address. Please verify your new email to re-activate your account.')
                return redirect('users:login')

            else:
                user_form.save()
                messages.success(request, 'Your profile details have been updated!')
                return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'user_form': user_form})



# ------------------- Address Book -------------------
@login_required
def address_book(request):
    addresses = Address.objects.filter(user=request.user)
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Address added successfully.")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('users:address_book')
    return render(request, 'users/address_book.html', {'addresses': addresses, 'form': form})


@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
            return redirect('users:address_book')
    else:
        form = AddressForm(instance=address)
    return render(request, 'users/address_form.html', {'form': form})


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, "Address deleted successfully.")
        return redirect('users:address_book')
    return render(request, 'users/address_delete_confirm.html', {'address': address})

@login_required
def reset_password(request):
    messages.info(request, "This feature is not yet implemented.")
    return redirect('users:profile')


@login_required
def delete_account(request):
    messages.info(request, "This feature is not yet implemented.")
    return redirect('users:profile')