from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import LoginUser

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'uk-input uk-width-auto'}), label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'uk-input uk-width-auto'}), label='Password')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Invalid username or password.')

        return cleaned_data


class RegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'uk-input uk-width-auto'}), label='Username')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'uk-input uk-width-auto'}), label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'uk-input uk-width-auto'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'uk-input uk-width-auto'}), label='Confirm Password')

  
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This Email is Already in use!")
            return email
        
    def clean_username(self):
            username = self.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("This Username is Already in use!")
            return username


class CreateTopicForm(forms.Form):
    topicname = forms.CharField(widget=forms.TextInput(attrs={'class' : 'uk-input uk-width-auto'}), label='Brandname')