import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, UpdateView, CreateView, ListView
from django.contrib.auth import authenticate, login
from django import forms

from user.models import User, UserFollow
from content.models import Post, Commit, SubFollow
from notify.models import Noty
from user.forms import UserEditForm, SignUpForm
from core.core import random_avatar, avatar_resize, cover_resize


class SignUpView(CreateView):
	form_class = SignUpForm
	template_name = 'user/signup.html'
	success_url = '/'

	def form_valid(self, form):
		username = self.request.POST['username']
		password = self.request.POST['password']

		obj = form.save(commit=False)
		obj.set_password(obj.password)
		obj.avatar = 'user/avatar/%s.png' % (obj.username)
		obj.save()

		random_avatar(username)

		user = authenticate(username=username, password=password)
		login(self.request, user)

		return HttpResponseRedirect('/')


def profile_context(self, context):
	username = self.request.user.username
	profile = self.kwargs['profile']
	context['list_url'] = '/%s' % profile
	context['profile'] = User.objects.get(username=profile)
	context['action'] = 'follow'

	if self.request.user.is_authenticated():
		if username == profile:
			context['action'] = 'edit'
		else:
			follow_state = UserFollow.objects.by_id(followid='%s>%s' % (username, profile))
			if follow_state: context['action'] = 'unfollow'
			else: context['action'] = 'follow'

	return context


class ProfilePostView(ListView):
	template_name = 'user/profile/post.html'
	paginate_by = 4

	def get(self, request, *args, **kwargs):
		if request.is_ajax(): self.template_name = 'ajax/post_list.html'
		return super(ProfilePostView, self).get(request, *args, **kwargs)

	def get_queryset(self):
		return Post.objects.by_user_profile(user=self.kwargs['profile'])

	def get_context_data(self, **kwargs):
		context = super(ProfilePostView, self).get_context_data(**kwargs)
		context['profile_show'] = 'post'
		return profile_context(self, context)


class ProfileCommitView(ListView):
	template_name = 'user/profile/commit.html'
	paginate_by = 5

	def get_queryset(self):
		return Commit.objects.filter(user_id=self.kwargs['profile'], show=True)

	def get_context_data(self, **kwargs):
		context = super(ProfileCommitView, self).get_context_data(**kwargs)
		return profile_context(self, context, **kwargs)


class ProfileShowView(ListView):
	template_name = 'user/profile/show.html'
	paginate_by = 20

	def get_queryset(self):
		show = self.kwargs['show']

		if show == 'followers': return UserFollow.objects.filter(followed=self.kwargs['profile'])
		elif show == 'following': return UserFollow.objects.filter(follower=self.kwargs['profile'])
		else: return SubFollow.objects.filter(follower=self.kwargs['profile'])

	def get_context_data(self, **kwargs):
		context = super(ProfileShowView, self).get_context_data(**kwargs)
		context['profile_show'] = self.kwargs['show']
		return profile_context(self, context, **kwargs)


class BlogView(ListView):
	template_name = 'user/blog.html'
	model = User


class UserEdit(UpdateView):
	template_name = 'user/edit.html'
	form_class = UserEditForm
	get_absolute_url = '/'

	def get_queryset(self):
		return User.objects.filter(username=self.request.user)

	def form_valid(self, form):
		username = self.request.user
		user_before = User.objects.get(username=username)
		if user_before.cover: cover_exists = True
		else: cover_exists = False

		obj = form.save(commit=False)
		obj.save()

		final_avatar_dir = 'm/user/avatar/%s.png' % username

		if not 'm/%s' % (obj.avatar) == final_avatar_dir:
			avatar_dir = '%s/m/%s' % (settings.BASE_DIR, obj.avatar)
			os.rename(avatar_dir, final_avatar_dir)
			obj.avatar = final_avatar_dir[2:]
			obj.save()
			avatar_resize(final_avatar_dir)

		final_cover_dir = 'm/user/cover/%s.png' % username

		def create_cover():
			cover_dir = '%s/m/%s' % (settings.BASE_DIR, obj.cover)
			os.rename(cover_dir, final_cover_dir)
			obj.cover = final_cover_dir[2:]
			obj.save()
			cover_resize(final_cover_dir)

		if not 'm/%s' % (obj.cover) == final_cover_dir:
			if os.path.isfile(final_cover_dir):
				create_cover()

		if obj.cover and not cover_exists: create_cover()

		return HttpResponseRedirect('/%s/edit' % self.kwargs['pk'])


class UserFollowCreate(View):
	def post(self, request, *args, **kwargs):
		user = self.request.user
		followed = self.kwargs['followed']

		obj = UserFollow.objects.create(follower=user, followed_id=followed)
		obj.save()
		obj.follower.following_number += 1
		obj.follower.save()
		obj.followed.follower_number += 1
		obj.followed.save()

		noty = Noty.objects.create(user_id=followed, category='F', follow_id=obj.pk)
		noty.create_noty()

		return HttpResponse(status=200)


class UserFollowDelete(View):
	def post(self, request, *args, **kwargs):
		user = self.request.user
		unfollowed = self.kwargs['unfollowed']

		obj = UserFollow.objects.get(follower_id=user, followed_id=unfollowed)

		noty = Noty.objects.get(user_id=obj.followed_id, follow_id=obj.pk)
		if noty.show == True: obj.followed.noty_number -= 1

		obj.follower.following_number -= 1
		obj.follower.save()
		obj.followed.follower_number -= 1
		obj.followed.save()
		obj.delete()

		return HttpResponse(status=200)
