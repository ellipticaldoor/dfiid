from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from blog.models import Post, Tag
from cms.forms import PostForm, TagForm


# Post related views

class PostListView(ListView):
	template_name = 'cms/post/list.html'
	queryset = Post.objects.all()
	paginate_by = 14


class PostEditView(UpdateView):
	template_name = 'cms/post/edit.html'
	model = Post
	form_class = PostForm

	def get_success_url(self):
		# Añadir mensaje cambios guardados
		return self.object.get_edit_url()


class PostCreateView(CreateView):
	template_name = 'cms/post/edit.html'
	model = Post
	form_class = PostForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.author = self.request.user
		obj.save()
		return HttpResponseRedirect(obj.get_edit_url())


# Tag related views

class TagListView(ListView):
	template_name = 'cms/tag/list.html'
	queryset = Tag.objects.all()
	paginate_by = 14


class TagCreateView(CreateView):
	template_name = 'cms/tag/edit.html'
	model = Post
	form_class = TagForm
	success_url = '/cms/tags'
