from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from content.models import Post
from cms.forms import PostForm


class CreatePostView(CreateView):
	template_name = 'cms/create_edit.html'
	model = Post
	form_class = PostForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.save()
		return HttpResponseRedirect(obj.get_edit_url())


class ListPostView(ListView):
	template_name = 'cms/created.html'
	queryset = Post.objects.all()
	paginate_by = 14

	def get_queryset(self):
		queryset = Post.objects.created(self.request.user)
		return queryset


class EditPostView(UpdateView):
	template_name = 'cms/create_edit.html'
	model = Post
	form_class = PostForm

	def get_success_url(self):
		# Añadir mensaje cambios guardados
		return self.object.get_edit_url()