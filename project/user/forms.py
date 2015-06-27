from django import forms
from django.contrib.auth.forms import AuthenticationForm

from user.models import User, UserFollow
from core.core import AvatarInput, is_reserved

from nocaptcha_recaptcha.fields import NoReCaptchaField


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
	# def __init__(self, *args, **kwargs):
	# 	super(UserEditForm, self).__init__(*args, **kwargs)
	# 	self.fields['password'].widget.attrs.update({
	# 			'placeholder': 'contraseña actual'
	# 		})
	# 	self.fields['new_password'].widget.attrs.update({
	# 			'placeholder': 'nueva contraseña'
	# 		})

	avatar = forms.ImageField(label='', widget=AvatarInput)
	cover = forms.ImageField(label='', widget=AvatarInput, required=False)
	# password = forms.CharField(label='', widget=forms.PasswordInput, required=False)
	# new_password = forms.CharField(label='', widget=forms.PasswordInput, required=False)

	class Meta:
		model = User
		# fields = ['avatar', 'cover', 'password', 'new_password']
		fields = ['avatar', 'cover']


class SignUpForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		set_user_form_attrs(self)

	username = forms.CharField(label='', max_length=16)
	password = forms.CharField(label='', widget=forms.PasswordInput)
	captcha = NoReCaptchaField(label='')
	
	class Meta:
		model = User
		fields = ['username', 'password']

	def clean(self):
		cleaned_data = super(SignUpForm, self).clean()
		if is_reserved(cleaned_data.get('username')):
			self.add_error('username', 'nombre de usuario no disponible')


class UserFollowForm(forms.ModelForm):
	class Meta:
		model = UserFollow
		fields = []
