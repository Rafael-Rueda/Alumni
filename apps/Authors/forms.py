import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import field_attr


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_attr(self.fields['password'], 'placeholder', 'Digite sua senha aqui')
        field_attr(self.fields['password2'], 'placeholder', 'Digite sua senha novamente')
        field_attr(self.fields['email'], 'placeholder', 'Digite seu email aqui')
        field_attr(self.fields['first_name'], 'placeholder', 'Ex: Fulano')
        field_attr(self.fields['last_name'], 'placeholder', 'Ex: Silva')

    # Form fields

    password = forms.CharField(required=True, widget=forms.PasswordInput(), label='Senha')
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(), label='Repita a senha')

    # Meta class for ModelForm

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'username': 'Username',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Digite seu usuário aqui',
            }),
            'email': forms.EmailInput(attrs={
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'required': True
            }),
        }
        error_messages = {
            'email': {
                'required': 'Esse campo é obrigatório.'
            },
            'first_name': {
                'required': 'Esse campo é obrigatório.'
            },
            'last_name': {
                'required': 'Esse campo é obrigatório.'
            },
            'username': {
                'required': 'Esse campo é obrigatório.'
            },
        }
    
    # Cleaning data

    def clean_password(self):
        data = self.cleaned_data.get('password', '')
        regex = re.compile('^(?!^\s)(.{8,32})?(?<!\s)$')

        if regex.match(data) == None:
            if len(data) < 8 or len(data) > 32:
                raise ValidationError('A senha deve ter entre 8-32 caracteres.')
            else:
                raise ValidationError('A senha deve conter apenas caracteres válidos.')
        
        # always return the data
        return data
    
    def clean_first_name(self):
        data = self.cleaned_data['first_name'].strip()

        if len(data) < 3:
            raise ValidationError('Esse campo é obrigatório (Mín. 3 caracteres).')

        return data
    
    def clean_last_name(self):
        data = self.cleaned_data['last_name'].strip()

        if len(data) < 3:
            raise ValidationError('Esse campo é obrigatório (Mín. 3 caracteres).')

        return data
    
    def clean_email(self):
        data = self.cleaned_data['email'].strip()

        if not '@' in data:
            raise ValidationError('O email deve conter um "@".')
        
        if User.objects.filter(email=data).exists():
            raise ValidationError('Esse email já está em uso.')

        return data
    
    def clean(self):
        data = super().clean()
        password = data.get('password', '')
        password2 = data.get('password2', '')

        if password and password2:
            if password != password2:
                raise ValidationError({
                    'password': 'As senhas devem ser iguais.',
                    'password2': 'As senhas devem ser iguais.'
                })

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_attr(self.fields['login'], 'placeholder', 'Digite seu usuário ou e-mail aqui')
        field_attr(self.fields['password'], 'placeholder', 'Digite sua senha aqui')

    login = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={'required': True}),
        label='Usuário ou E-mail'
    )
    password = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(attrs={'required': True}),
        label='Senha'
    )