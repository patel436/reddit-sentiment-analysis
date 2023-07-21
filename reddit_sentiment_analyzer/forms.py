from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'uk-input uk-width-auto'}), label='Username')
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-input uk-width-auto'}), label='Password')

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'uk-input uk-width-auto'}), label='Username')
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-input uk-width-auto'}), label='Email')
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-input uk-width-auto'}), label='Password')
    confirm_password = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-input uk-width-auto'}), label='Confirm Password')

class CreateTopicForm(forms.Form):
    topicname = forms.CharField(widget=forms.TextInput(attrs={'class' : 'uk-input uk-width-auto'}), label='Brandname')