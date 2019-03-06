from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.'
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=256,
        help_text='Required. Inform a valid email address.'
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        self.user = authenticate(username=email, password=password)
        if not self.user:
            raise forms.ValidationError("email or password is not correct")
        elif not self.user.is_active:
            raise forms.ValidationError("user is not active")

        return self.cleaned_data
