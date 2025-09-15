# rcnb/users/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Address, Profile # <-- Import both Address and Profile

# This form is for user registration
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data

# This form is for user login
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

# This form is for updating the User model (name, email) on the profile page
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'email']

# THIS IS THE NEW, CORRECT FORM FOR HANDLING ADDRESSES
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'address_line_1', 'address_line_2', 'city', 'state', 'pincode']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Contact Number'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'House No., Building, Street, Area'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Landmark (Optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City/Town'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Pin Code'}),
        }