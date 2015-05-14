from django import forms
from django.contrib.auth.forms import AuthenticationForm
from nocaptcha_recaptcha.fields import NoReCaptchaField

from user.models import User, UserFollow


def set_user_form_attrs(self):
		self.fields['username'].widget.attrs.update({
			'autofocus': 'autofocus',
			'required': 'required',
			'placeholder': 'usuario'
			})
		self.fields['password'].widget.attrs.update({
			'required': 'required',
			'placeholder': 'contraseña'
			})
		return self


class LoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		set_user_form_attrs(self)

	username = forms.CharField(label='', max_length=16, )
	password = forms.CharField(label='', widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):	
	class Meta:
		model = User
		fields = ['avatar', 'bio', 'password']


class SignUpForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		set_user_form_attrs(self)

	username = forms.CharField(label='', max_length=16)
	password = forms.CharField(label='', widget=forms.PasswordInput)

	
	class Meta:
		model = User
		fields = ['username', 'password' ]


class UserFollowForm(forms.ModelForm):
	class Meta:
		model = UserFollow
		fields = []