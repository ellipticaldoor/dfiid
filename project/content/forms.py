

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

	slug = forms.CharField(label="", max_length=10)
		
	class Meta:
		model = Sub
		fields = ('slug',)


class SubFollowForm(forms.ModelForm):
	class Meta:
		model = SubFollow
		fields = []


class ImageInput(forms.ClearableFileInput):
	template_with_initial = (
		'<div id="image_post_edit"><div><img src="/%(initial_url)s"></div>'
		'<input id="image-clear_id" name="image-clear" type="checkbox"> <label for="image-clear_id">borrar</label></div>'
		'%(input)s'
	)


class PostForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs.update({
				'autofocus': 'autofocus',
				'required': 'required',
				'placeholder': 'título'
			})
		self.fields['body'].widget.attrs.update({
				'required': 'required',
				'placeholder': 'post'
			})
		self.fields['sub'].widget.attrs.update({'required': 'required'})

	image = forms.ImageField(widget=ImageInput, required=False)

	class Meta:
		model = Post
		fields = ('title', 'body', 'image', 'sub', 'draft')


class CommitForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CommitForm, self).__init__(*args, **kwargs)
		self.fields['body'].widget.attrs.update({
				'placeholder': 'comentario',
				'rows': '3',
			})

	body = forms.CharField(label='', max_length=500, widget=forms.Textarea, required=False)

	class Meta:
		model = Commit
		fields = ('body',)