from django import forms

from anon.models import AnonPost, AnonCommit


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

	class Meta:
		model = AnonPost
		fields = ('title', 'body', 'image')


class AnonCommitForm(forms.ModelForm):
	body = forms.CharField(label='', max_length=500, widget=forms.Textarea, required=False)

	class Meta:
		model = AnonCommit
		fields = ('body',)