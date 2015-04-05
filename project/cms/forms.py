from django import forms

from content.models import Post, Tag


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'body', 'pub_date', 'tag', 'draft')


class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ('slug',)