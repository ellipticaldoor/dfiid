from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from content.models import Post, Sub
from content.forms import PostForm, SubForm


class FrontView(ListView):
	template_name = 'content/front.html'
	queryset = Post.objects.published()
	paginate_by = 3

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.template_name = 'content/ajax/posts.html'

		return super(FrontView, self).get(request, *args, **kwargs)


class PostView(DetailView):
	template_name = 'content/post_view.html'

	def get_queryset(self):
		pk, slug = self.kwargs['pk'], self.kwargs['slug']
		queryset = Post.objects.by_post(pk, slug)
		return queryset


class CreatePostView(CreateView):
	template_name = 'content/create_edit.html'
	model = Post
	form_class = PostForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.save()
		return super(CreatePostView, self).form_valid(form)

	def get_success_url(self):
		return self.object.get_edit_url()


class EditPostView(UpdateView):
	template_name = 'content/create_edit.html'
	model = Post
	form_class = PostForm

	def get_success_url(self):
		return self.object.get_edit_url()


class ListPostView(ListView):
	template_name = 'content/created.html'
	queryset = Post.objects.all()
	paginate_by = 14

	def get_queryset(self):
		queryset = Post.objects.created(self.request.user)
		return queryset


class SubContentView(ListView):
	template_name = 'content/post_list.html'

	def get_queryset(self):
		sub = self.kwargs['sub']
		queryset = Post.objects.by_sub(sub)
		return queryset


class SubView(ListView):
	template_name = 'content/sub.html'
	model = Sub


class CreateSubView(CreateView):
	template_name = 'content/create_sub.html'
	model = Sub
	form_class = SubForm
	success_url = '/sub'