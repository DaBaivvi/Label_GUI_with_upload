from django import forms
from django.contrib.auth.models import User

#Register form
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This name is already taken')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email or '.' not in email:
            raise forms.ValidationError('Please enter a valid email address')
        if email.index('@') > email.index('.'):
            raise forms.ValidationError('Please enter a valid email address')
        if email.count('@') !=1 or email.count('.') !=1:
            raise forms.ValidationError('Please enter a valid email address')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')

        if password and confirm_password and password !=confirm_password:
            raise forms.ValidationError('Password do not match')
        
        if '@' not in email or '.' not in email:
            raise forms.ValidationError('Please enter a valid email address')
        
        return cleaned_data

