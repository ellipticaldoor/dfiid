from django import forms

from content.models import Post


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'body', 'pub_date', 'sub', 'draft')