from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UserUpdateForm, AddressForm, PasswordResetRequestForm, SetNewPasswordForm
from django.contrib.auth.forms import PasswordResetForm
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
from asgiref.sync import sync_to_async
from django.core.signing import Signer, BadSignature, SignatureExpired
from django.urls import reverse

signer = Signer()
logger = logging.getLogger(__name__)

from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.urls import reverse


# ------------------- Custom Logout View -------------------

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('users:login')


# ------------------- Helper Functions for Async Operations -------------------
@sync_to_async
def aget_current_site(request):
    return get_current_site(request)

@sync_to_async
def arender_to_string(template_name, context):
    return render_to_string(template_name, context)

@sync_to_async
def asend_mail(subject, message, from_email, recipient_list, html_message=None):
    """
    Sends an email. If html_message is provided, it will be sent as an HTML email.
    """
    send_mail(
        subject,
        message,  # Plain text message
        from_email,
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    )

@sync_to_async
def acreate_user(username, email, password):
    first_name, last_name = username.split(" ", 1) if " " in username else (username, "")
    return User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)

@sync_to_async
def alogin(request, user):
    login(request, user)

@sync_to_async
def aget_user(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

@sync_to_async
def aauthenticate(request, username, password):
    return authenticate(request, username=username, password=password)

@sync_to_async
def aget_user_from_session(request):
    return request.session.get('unverified_user')

@sync_to_async
def aclear_session(request):
    if 'unverified_user' in request.session:
        del request.session['unverified_user']
        
@sync_to_async
def set_session(request, key, value):
    request.session[key] = value


# ------------------- Register -------------------

async def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if await sync_to_async(form.is_valid)():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']


            # Temporarily store user data in the session
            user_data = {
                'email': email,
                'password': password, 
                'username': username
            }
            await set_session(request, 'unverified_user', user_data)

            # Create a temporary, inactive user to generate a token
            user = User(username=email, email=email)
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            verification_link = request.build_absolute_uri(reverse('users:verify_email', kwargs={'uidb64': uidb64, 'token': token}))

            mail_subject = 'Activate Your Account'
            html_message = await arender_to_string('users/email_verification_email.html', {
                'verification_link': verification_link,
            })
            plain_message = f"Please verify your email by clicking on this link: {verification_link}"


            try:
                await asend_mail(mail_subject, plain_message, settings.DEFAULT_FROM_EMAIL, [email], html_message=html_message)
                return await sync_to_async(render)(request, 'users/email_verification_sent.html')
            except Exception as e:
                logger.error(f"Error sending verification email: {e}")
                messages.error(request, "Could not send verification email. Please try again later.")
    else:
        form = RegisterForm()
    return await sync_to_async(render)(request, 'users/register.html', {'form': form})


# ------------------- Email Verification -------------------

async def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user_data = await aget_user_from_session(request)

        if not user_data:
            messages.error(request, "Verification session expired. Please register again.")
            return redirect('users:register')

        temp_user = User(pk=uid, username=user_data['email'], email=user_data['email'])

        if default_token_generator.check_token(temp_user, token):
            user = await acreate_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            user.is_active = True
            await sync_to_async(user.save)()
            await aclear_session(request)
            await alogin(request, user)
            messages.success(request, 'Your email has been verified and your account is created! You are now logged in.')
            return redirect('products:product_list')
        else:
            return await sync_to_async(render)(request, 'users/email_verification_invalid.html')

    except (TypeError, ValueError, OverflowError, BadSignature, SignatureExpired):
        return await sync_to_async(render)(request, 'users/email_verification_invalid.html')


# ------------------- Email Login -------------------

async def email_login(request):
    if request.method == 'POST':
        form = await sync_to_async(LoginForm)(request.POST)
        if await sync_to_async(form.is_valid)():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user_obj = await aget_user(email)
            if user_obj:
                user = await aauthenticate(request, username=user_obj.username, password=password)
                if user:
                    await alogin(request, user)
                    return redirect('products:product_list')
                else:
                    messages.error(request, "Invalid credentials.")
            else:
                messages.error(request, "User does not exist.")
    else:
        form = LoginForm()
    return await sync_to_async(render)(request, 'users/login.html', {'form': form})



# ------------------- Profile Page -------------------

@login_required
async def profile(request):
    user = await sync_to_async(lambda: request.user)()
    
    if request.method == 'POST':
        user_form = await sync_to_async(lambda: UserUpdateForm(request.POST, instance=user))()
        if await sync_to_async(user_form.is_valid)():
            if 'email' in user_form.changed_data:
                user = await sync_to_async(user_form.save)(commit=False)
                user.is_active = False
                await sync_to_async(user.save)()

                current_site = await aget_current_site(request)
                mail_subject = 'Verify Your New Email Address'
                message = await arender_to_string('users/email_verification_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                await asend_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

                messages.warning(request, 'A verification link has been sent to your new email address.')
                return redirect('users:login')
            else:
                await sync_to_async(user_form.save)()
                messages.success(request, 'Your profile details have been updated!')
                return redirect('users:profile')
    else:
        user_form = await sync_to_async(lambda: UserUpdateForm(instance=user))()
    return await sync_to_async(render)(request, 'users/profile.html', {'user_form': user_form})


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
    return render(request, 'users/edit_address.html', {'form': form, 'address_id': address_id})


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, "Address deleted successfully.")
        return redirect('users:address_book')
    return render(request, 'users/address_delete_confirm.html', {'address': address})


def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Correctly build the reset link
                reset_link = request.build_absolute_uri(
                    reverse('users:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                )

                mail_subject = 'Reset your password'
                
                # Use the new password reset template
                html_message = render_to_string('users/password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                
                plain_message = f"Please reset your password by clicking on this link: {reset_link}"
                send_mail(mail_subject, plain_message, settings.DEFAULT_FROM_EMAIL, [email], html_message=html_message)
                
                messages.success(request, "A password reset link has been sent to your email.")
                return redirect('users:login')
            except User.DoesNotExist:
                messages.error(request, "User with this email does not exist.")
    else:
        form = PasswordResetRequestForm()
    return render(request, 'users/password_reset_request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, "Your password has been reset successfully. You can now log in.")
                return redirect('users:login')
        else:
            form = SetNewPasswordForm()
        return render(request, 'users/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('users:reset_password')


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home:home')  # Redirect to the home page after deletion
    return render(request, 'users/delete_account_confirm.html')