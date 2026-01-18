from django import forms
from .models import Customer

class RegisterForm(forms.ModelForm):
    confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        data = super().clean()

        if data.get('password') != data.get('confirm'):
            raise forms.ValidationError("Passwords do not match")

        return data
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
