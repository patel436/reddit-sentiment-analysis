from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'uk-input uk-width-auto'}), label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'uk-input uk-width-auto'}), label='Password')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
                if user.password != password:
                    raise forms.ValidationError("Invalid username or password.")
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid username or password.")

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'uk-input uk-width-auto'}), label='Username')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'uk-input uk-width-auto'}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'uk-input uk-width-auto'}), label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'uk-input uk-width-auto'}), label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

class CreateTopicForm(forms.Form):
    topicname = forms.CharField(widget=forms.TextInput(attrs={'class' : 'uk-input uk-width-auto'}), label='Brandname')