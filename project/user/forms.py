from nocaptcha_recaptcha.fields import NoReCaptchaField
from django import forms

from user.models import User


class SignUpForm(forms.ModelForm):
	captcha = NoReCaptchaField()
	
	class Meta:
		model = User
		fields = ['username', 'password', ]