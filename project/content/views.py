from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from content.models import Sub, Post, Comment
from content.forms import SubForm, PostForm, CommentForm
from core.core import random_fractal


class CreateSubView(CreateView):
	template_name = 'content/sub_create.html'
	form_class = SubForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.save()
		obj.image = 's/media/sub/image/%s.png' % (obj.slug)
		obj.save()
		random_fractal(obj.slug)
		return HttpResponseRedirect('/sub')


class SubView(ListView):
	template_name = 'content/sub.html'
	model = Sub


class SubContentView(ListView):
	template_name = 'content/sub_content_list.html'
	paginate_by = 5

	def get_queryset(self):
		return Post.objects.by_sub(self.kwargs['sub'])

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.template_name = 'content/ajax/posts.html'
		return super(SubContentView, self).get(request, *args, **kwargs)


class FrontView(ListView):
	template_name = 'content/front.html'
	queryset = Post.objects.published()
	paginate_by = 5

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.template_name = 'content/ajax/posts.html'
		return super(FrontView, self).get(request, *args, **kwargs)


class PostView(DetailView):
	template_name = 'content/post_detail.html'

	def get_queryset(self):
		pk, slug = self.kwargs['pk'], self.kwargs['slug']
		queryset = Post.objects.by_post(pk, slug)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(PostView, self).get_context_data(**kwargs)
		context['form'] = CommentForm
		return context


class PostCommentView(CreateView):
	form_class = CommentForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.post = Post.objects.get(post_id=self.kwargs['pk'])
		obj.save()
		obj.user.last_commented = obj.created
		obj.user.save()
		obj.post.last_commented = obj.created
		obj.post.comment_number += 1
		obj.post.save()
		obj.post.sub.last_commented = obj.created
		obj.post.sub.save()
		return HttpResponseRedirect(obj.get_absolute_url())


class CreatePostView(CreateView):
	template_name = 'content/post_create_update.html'
	form_class = PostForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.save()
		return HttpResponseRedirect(obj.get_edit_url())


class UpdatePostView(UpdateView):
	template_name = 'content/post_create_update.html'
	form_class = PostForm

	def get_queryset(self):
		return Post.objects.by_user(self.request.user)

	def get_success_url(self):
		return self.object.get_edit_url()


class PostUserCreatedView(ListView):
	template_name = 'content/post_user_created.html'
	paginate_by = 14

	def get_queryset(self):
		return Post.objects.by_user(self.request.user)