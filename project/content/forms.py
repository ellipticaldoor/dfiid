from django import forms

from content.models import Sub, Post, Comment


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


class PostForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs.update({
			'autofocus': 'autofocus',
			'required': 'required',
			'placeholder': 'título'
			})
		self.fields['body'].widget.attrs.update({'required': 'required'})
		self.fields['pub_date'].widget.attrs.update({
			'required': 'required',
			'placeholder': 'yyyy-mm-dd hh:mm:ss'
			})
		self.fields['sub'].widget.attrs.update({'required': 'required'})

	class Meta:
		model = Post
		fields = ('title', 'body', 'pub_date', 'sub', 'draft')


class CommentForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CommentForm, self).__init__(*args, **kwargs)
		self.fields['body'].widget.attrs.update({ 'required': 'required' })

	body = forms.CharField(label="", max_length=500, widget=forms.Textarea)

	class Meta:
		model = Comment
		fields = ('body',)