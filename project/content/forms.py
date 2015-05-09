from django import forms

from content.models import Sub, SubFollow, Post, Commit


class SubForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SubForm, self).__init__(*args, **kwargs)
		self.fields['slug'].widget.attrs.update({
			'autofocus': 'autofocus',
			'required': 'required',
			'placeholder': 'nombre del sub'
			})

	slug = forms.CharField(label="")
		
	class Meta:
		model = Sub
		fields = ('slug',)


class SubFollowForm(forms.ModelForm):
	class Meta:
		model = SubFollow
		fields = []


class PostForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs.update({
			'autofocus': 'autofocus',
			'required': 'required',
			'placeholder': 'título'
			})
		self.fields['body'].widget.attrs.update({'required': 'required'})
		self.fields['sub'].widget.attrs.update({'required': 'required'})

	class Meta:
		model = Post
		fields = ('title', 'body', 'sub', 'draft')


class CommitForm(forms.ModelForm):
	body = forms.CharField(label='', max_length=500, widget=forms.Textarea, required=False)

	class Meta:
		model = Commit
		fields = ('body',)