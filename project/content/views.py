from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from content.models import Sub, SubFollow, Post, Commit
from content.forms import SubForm, PostForm, CommitForm
from notify.models import Noty
from core.core import random_avatar_sub


class CreateSubView(CreateView):
	template_name = 'content/sub_create.html'
	form_class = SubForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.save()
		obj.image = 'sub/%s.png' % (obj.slug)
		obj.save()
		random_avatar_sub(obj.slug)
		return HttpResponseRedirect('/sub')


class SubView(ListView):
	template_name = 'content/sub.html'
	model = Sub


class FrontView(ListView):
	template_name = 'layouts/post_list.html'
	paginate_by = 4

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.template_name = 'ajax/post_list.html'
		return super(FrontView, self).get(request, *args, **kwargs)

	def get_queryset(self):
		if self.kwargs['tab'] == 'top':
			return Post.objects.last_commited()
		else:
			return Post.objects.created()

	def get_context_data(self, **kwargs):
		context = super(FrontView, self).get_context_data(**kwargs)
		context['list'] = 'portada'
		context['tab_show'] = self.kwargs['tab']

		if self.kwargs['tab'] == 'top':
			context['list_url'] = '/'
		else:
			context['list_url'] = '/new'
		return context


class SubPostListView(ListView):
	template_name = 'content/sub_post_list.html'
	paginate_by = 4

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.template_name = 'ajax/post_list.html'
		return super(SubPostListView, self).get(request, *args, **kwargs)

	def get_queryset(self):
		if self.kwargs['tab'] == 'top':
			return Post.objects.sub_last_commited(self.kwargs['sub'])
		else:
			return Post.objects.sub_created(self.kwargs['sub'])

	def get_context_data(self, **kwargs):
		context = super(SubPostListView, self).get_context_data(**kwargs)
		sub = Sub.objects.get(pk=self.kwargs['sub'])
		user = self.request.user

		if self.kwargs['tab'] == 'followers':
			context['followers'] = True

		context['tab_show'] = self.kwargs['tab']
		context['list'] = sub

		context['tab'] = self.kwargs['tab']
		if self.kwargs['tab'] == 'top':
			context['list_url'] = '/sub/%s' % sub
		else:
			context['list_url'] = '/sub/%s/new' % sub

		context['action'] = 'follow'

		if user.is_authenticated():
			follow_state = SubFollow.objects.by_id(sub_followid='%s>%s' % (user.pk, sub.pk))
			if follow_state:
				context['action'] = 'unfollow'
			else:
				context['action'] = 'follow'

		return context


class PostCommitView(CreateView):
	template_name = 'layouts/post_detail.html'
	form_class = CommitForm

	def get_context_data(self, **kwargs):
		context = super(PostCommitView, self).get_context_data(**kwargs)
		pk, slug = self.kwargs['pk'], self.kwargs['slug']
		context['object'] = Post.objects.by_post(pk, slug)
		return context

	def form_valid(self, form):
		if self.request.user.is_authenticated():
			user = self.request.user
			post = Post.objects.get(postid=self.kwargs['pk'])

			obj = form.save(commit=False)
			obj.create_commit(user, post)

			if not obj.post.user.pk == user.pk:
				noty = Noty.objects.create(user_id=obj.post.user_id, category='C', commit=obj)
				noty.create_noty()

			return HttpResponseRedirect(obj.get_commit_url())
		else:
			commit_url = '/post/%s/%s/' % (self.kwargs['pk'], self.kwargs['slug'])
			return HttpResponseRedirect('/login/?next=%s' % (commit_url))


class CreatePostView(CreateView):
	template_name = 'layouts/post_create.html'
	form_class = PostForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.save()

		if obj.draft: return HttpResponseRedirect('/created')
		else:
			obj.user.last_commited = obj.created
			obj.user.save()
			obj.sub.last_commited = obj.created
			obj.sub.save()
			obj.last_commited = obj.created
			obj.save()
			return HttpResponseRedirect(obj.get_absolute_url())


class UpdatePostView(UpdateView):
	template_name = 'layouts/post_create.html'
	form_class = PostForm

	def get_queryset(self):
		return Post.objects.by_user(self.request.user)

	def form_valid(self, form):
		obj = form.save(commit=False)
		if not obj.last_commited and not obj.draft:
			now = datetime.now()
			obj.last_commited = now
			obj.user.last_commited = now
			obj.user.save()
			obj.sub.last_commited = now
			obj.sub.save()
		obj.save()

		if obj.draft: return HttpResponseRedirect('/created')
		else: return HttpResponseRedirect(obj.get_absolute_url())


class PostUserCreatedView(ListView):
	template_name = 'content/post_user_created.html'

	def get_queryset(self):
		return Post.objects.by_user(self.request.user)


class SubFollowCreate(View):
	def post(self, request, *args, **kwargs):
		sub_followed = self.kwargs['followed']

		sub_followed_obj = SubFollow.objects.create(follower=self.request.user,sub_id=sub_followed)
		sub_followed_obj.save()
		sub_followed_obj.follower.sub_following_number += 1
		sub_followed_obj.follower.save()
		sub_followed_obj.sub.follower_number += 1
		sub_followed_obj.sub.save()

		return HttpResponse(status=200)


class SubFollowDelete(View):
	def post(self, request, *args, **kwargs):
		sub_unfollowed = self.kwargs['unfollowed']

		sub_unfollowed_obj = SubFollow.objects.get(follower=self.request.user, sub_id=sub_unfollowed)
		sub_unfollowed_obj.follower.sub_following_number -= 1
		sub_unfollowed_obj.follower.save()
		sub_unfollowed_obj.sub.follower_number -= 1
		sub_unfollowed_obj.sub.save()
		sub_unfollowed_obj.delete()

		return HttpResponse(status=200)
