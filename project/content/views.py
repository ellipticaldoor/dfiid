from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, FormMixin

from content.models import Sub, Post, Comment
from content.forms import SubForm, PostForm, CommentForm


class CreateSubView(CreateView):
	template_name = 'content/create_sub.html'
	success_url = '/sub'
	model = Sub
	form_class = SubForm


class SubView(ListView):
	template_name = 'content/sub.html'
	model = Sub


class SubContentView(ListView):
	template_name = 'content/post_list.html'

	def get_queryset(self):
		queryset = Post.objects.by_sub(self.kwargs['sub'])
		return queryset


class FrontView(ListView):
	template_name = 'content/front.html'
	queryset = Post.objects.published()
	paginate_by = 3

	def get(self, request, *args, **kwargs):
		if request.is_ajax(): self.template_name = 'content/ajax/posts.html'
		return super(FrontView, self).get(request, *args, **kwargs)


class PostView(DetailView, CreateView):
	template_name = 'content/post_detail.html'
	form_class = CommentForm

	def get_queryset(self):
		pk, slug = self.kwargs['pk'], self.kwargs['slug']
		queryset = Post.objects.by_post(pk, slug)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(PostView, self).get_context_data(**kwargs)
		context['form'] = CommentForm
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.post = Post.objects.get(post_id=self.kwargs['pk'])
		obj.save()
		return super(PostView, self).form_valid(form)


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