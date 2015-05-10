
from django.http import HttpResponseRedirect
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from content.models import Sub, SubFollow, Post, Commit
from content.forms import SubForm, SubFollowForm, PostForm, CommitForm
from core.core import random_avatar_sub


class CreateSubView(CreateView):
	template_name = 'content/sub_create.html'
	form_class = SubForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.save()
		obj.image = 's/media/sub/image/%s.png' % (obj.slug)
		obj.save()
		random_avatar_sub(obj.slug)
		return HttpResponseRedirect('/sub')


class SubView(ListView):
	template_name = 'content/sub.html'
	model = Sub


class FrontView(ListView):
	template_name = 'layouts/post_list.html'
	paginate_by = 10

	def get_queryset(self):
		return Post.objects.published()

	def get_context_data(self, **kwargs):
		context = super(FrontView, self).get_context_data(**kwargs)
		context['view_title'] = 'portada'
		return context


class SubPostListView(ListView):
	template_name = 'content/sub_post_list.html'
	paginate_by = 10

	def get_queryset(self):
		return Post.objects.by_sub(self.kwargs['sub'])

	def get_context_data(self, **kwargs):
		context = super(SubPostListView, self).get_context_data(**kwargs)
		sub = self.kwargs['sub']
		user = self.request.user

		context['view_title'] = sub
		context['action'] = 'follow'

		if user.is_authenticated():
			follow_state = SubFollow.objects.by_id(sub_follow_id='%s>%s' % (user.username, sub))
			if follow_state: context['action'] = 'unfollow'
			else: context['action'] = 'follow'

		return context


class SubFollowCreate(CreateView):
	form_class = SubFollowForm

	def form_valid(self, form):
		followed = self.kwargs['followed']
		obj = form.save(commit=False)
		obj.follower = self.request.user
		obj.sub = Sub.objects.get(slug=followed)
		obj.save()
		return HttpResponseRedirect('/sub/%s' % (followed))


class SubFollowDelete(View):
	def post(self, *args, **kwargs):
		unfollowed = self.kwargs['unfollowed']
		sub_follow_id = '%s>%s' % (self.request.user, unfollowed)
		follow = SubFollow.objects.get(sub_follow_id=sub_follow_id)
		follow.delete()
		return HttpResponseRedirect('/sub/%s' % (unfollowed))


class PostView(DetailView):
	template_name = 'layouts/post_detail.html'

	def get_queryset(self):
		pk, slug = self.kwargs['pk'], self.kwargs['slug']
		queryset = Post.objects.by_post(pk, slug)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(PostView, self).get_context_data(**kwargs)
		context['form'] = CommitForm
		return context


class PostCommitView(CreateView):
	form_class = CommitForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.post = Post.objects.get(post_id=self.kwargs['pk'])
		obj.save()
		obj.user.last_commited = obj.created
		obj.user.save()
		obj.post.last_commited = obj.created
		obj.post.commit_number += 1
		obj.post.save()
		obj.post.sub.last_commited = obj.created
		obj.post.sub.save()
		return HttpResponseRedirect(obj.get_absolute_url())


class CreatePostView(CreateView):
	template_name = 'content/post_create_update.html'
	form_class = PostForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.save()

		if obj.draft: return HttpResponseRedirect('/created')
		else: return HttpResponseRedirect(obj.get_absolute_url())


class UpdatePostView(UpdateView):
	template_name = 'content/post_create_update.html'
	form_class = PostForm

	def get_queryset(self):
		return Post.objects.by_user(self.request.user)

	def form_valid(self, form):
		obj = form.save()

		if obj.draft: return HttpResponseRedirect('/created')
		else: return HttpResponseRedirect(obj.get_absolute_url())


class PostUserCreatedView(ListView):
	template_name = 'content/post_user_created.html'
	paginate_by = 10

	def get_queryset(self):
		return Post.objects.by_user(self.request.user)