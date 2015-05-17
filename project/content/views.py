
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
		context['list'] = 'portada'
		return context


class SubPostListView(ListView):
	template_name = 'content/sub_post_list.html'
	paginate_by = 10

	def get_queryset(self):
		return Post.objects.by_sub(self.kwargs['sub'])

	def get_context_data(self, **kwargs):
		context = super(SubPostListView, self).get_context_data(**kwargs)
		sub = Sub.objects.get(pk=self.kwargs['sub'])
		user = self.request.user
		try: context['followers'] = self.kwargs['followers']
		except: context['followers'] = False


		context['list'] = sub
		context['action'] = 'follow'

		if user.is_authenticated():
			follow_state = SubFollow.objects.by_id(sub_followid='%s>%s' % (user.username, sub.pk))
			if follow_state: context['action'] = 'unfollow'
			else: context['action'] = 'follow'

		return context


class SubFollowCreate(CreateView):
	form_class = SubFollowForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.follower = self.request.user
		obj.sub = Sub.objects.get(slug=self.kwargs['followed'])
		obj.save()
		obj.sub.follower_number += 1
		obj.sub.save()
		return HttpResponseRedirect('/sub/%s' % (obj.sub.slug))


class SubFollowDelete(View):
	def post(self, *args, **kwargs):
		unfollowed = Sub.objects.get(slug=self.kwargs['unfollowed'])
		sub_followid = '%s>%s' % (self.request.user, unfollowed.slug)
		follow = SubFollow.objects.get(sub_followid=sub_followid)
		follow.delete()
		unfollowed.follower_number -= 1
		unfollowed.save()
		return HttpResponseRedirect('/sub/%s' % (unfollowed.slug))


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
	template_name = 'layouts/post_create.html'
	form_class = PostForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.save()

		if obj.draft: return HttpResponseRedirect('/created')
		else: return HttpResponseRedirect(obj.get_absolute_url())


class UpdatePostView(UpdateView):
	template_name = 'layouts/post_create.html'
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