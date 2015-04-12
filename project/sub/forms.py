from django import forms

from sub.models import Sub

class SubForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SubForm, self).__init__(*args, **kwargs)
		self.fields['slug'].widget.attrs.update({
			'autofocus': 'autofocus',
			'required': 'required',
			'placeholder': 'sub'
			})
		

	class Meta:
		model = Sub
		fields = ('slug',)