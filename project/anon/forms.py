from django import forms

from anon.models import AnonPost, AnonCommit

from nocaptcha_recaptcha.fields import NoReCaptchaField


class AnonPostForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AnonPostForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs.update({
				'autofocus': 'autofocus',
				'required': 'required',
				'placeholder': 'título'
			})
		self.fields['body'].widget.attrs.update({
				'required': 'required',
				'placeholder': 'markdown'
			})

	title = forms.CharField(label="")
	body = forms.CharField(label="", widget=forms.Textarea)
	captcha = NoReCaptchaField(label='')

	class Meta:
		model = AnonPost
		fields = ('title', 'body', 'image', 'captcha' )


class AnonCommitForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AnonCommitForm, self).__init__(*args, **kwargs)
		self.fields['body'].widget.attrs.update({
				'placeholder': 'comentario',
				'rows': '3',
			})

	body = forms.CharField(label='', max_length=500, widget=forms.Textarea, required=False)
	captcha = NoReCaptchaField(label='')

	class Meta:
		model = AnonCommit
		fields = ('body',)