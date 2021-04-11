from django import forms
from django.forms import ModelForm

from .models import User, Client, Address, Product, ProductCategory
from django.contrib.auth.hashers import make_password, check_password


class RegisterForm(forms.Form):
    login = forms.CharField(label='login')
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)
    email = forms.EmailField(label='email')

    def clean_login(self):
        login = self.cleaned_data['login'].lower()
        # if user exists
        if User.objects.filter(login=login):
            raise forms.ValidationError('This login is already used, choose another one')

        return login

    def clean_password2(self, *args, **kwargs):
        password = self.cleaned_data['password'].lower()
        password2 = self.cleaned_data['password2'].lower()

        if password2 != password:
            raise forms.ValidationError("Password don't match")

        return password

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email):
            raise forms.ValidationError('This email is already used, choose another one')

        return email

    def db_save(self):
        # hash password
        password = make_password(self.cleaned_data['password'])

        user = User(
            login=self.cleaned_data['login'],
            email=self.cleaned_data['email'],
            password=password,
        )
        user.save()


class LoginForm(forms.Form):
    login = forms.CharField(label='login')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    def clean_password(self):
        login = self.cleaned_data['login'].lower()
        password = self.cleaned_data['password'].lower()

        user = User.objects.get(login=login)
        if not user or not check_password(password, user.password):
            raise forms.ValidationError('Wrong password or login')

        return login


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'surname']


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class ProductForm(ModelForm):
    class Meta:
        model = Product
        # exclude = ['category']
        fields = '__all__'


class CategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'
