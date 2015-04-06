from django import forms

from sub.models import Sub

class SubForm(forms.ModelForm):
	class Meta:
		model = Sub
		fields = ('slug',)