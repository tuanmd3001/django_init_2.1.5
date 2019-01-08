from django import forms
from app_authentication.routines import authenticated_user

class LoginForm(forms.Form):
    widget = forms.TextInput(attrs={'required': '', 'class': 'input100', 'placeholder': 'Tên đăng nhập'})
    username = forms.CharField(label='Username', widget=widget)
    attrs = {'required': '', 'autocomplete': 'off', 'class': 'input100', 'placeholder': 'Mật khẩu'}
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs), label="Password")

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username', '')
        password = cleaned_data.get('password', '')
        if username and password:
            user, error = authenticated_user(username, password)

            if not user:
                raise forms.ValidationError(error)
            cleaned_data['user'] = user
        return cleaned_data