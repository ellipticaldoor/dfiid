
import os

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import View, UpdateView, CreateView, ListView
from django.contrib.auth import authenticate, login
from django import forms

from user.models import User, UserFollow
from content.models import Post, Commit
from user.forms import UserEditForm, SignUpForm, UserFollowForm
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
		obj.avatar = 's/media/user/avatar/%s.png' % (obj.username)
		obj.save()

		random_avatar(username)

		user = authenticate(username=username, password=password)
		login(self.request, user)

		return HttpResponseRedirect('/')


class ProfileView(ListView):
	template_name = 'user/profile.html'
	paginate_by = 4

	def get(self, request, *args, **kwargs):
		if request.is_ajax(): self.template_name = 'ajax/post_list.html'
		return super(ProfileView, self).get(request, *args, **kwargs)

	def get_queryset(self):
		return Post.objects.by_user_profile(user=self.kwargs['profile'])

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)
		username = self.request.user.username
		profile = self.kwargs['profile']
		context['list_url'] = '/%s' % profile
		try: context['profile_show'] = self.kwargs['show']
		except: context['profile_show'] = 'post'

		context['form'] = UserFollowForm
		context['profile'] = User.objects.get(username=profile)
		context['action'] = 'follow'

		if self.request.user.is_authenticated():
			if username == profile: context['action'] = 'edit'
			else:
				follow_state = UserFollow.objects.by_id(followid='%s>%s' % (username, profile))
				if follow_state: context['action'] = 'unfollow'
				else: context['action'] = 'follow'

		if context['profile_show'] == 'commit':
			context['commits'] = Commit.objects.filter(user_id=profile, show=True)

		return context


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
		if user_before.cover:
			print('hayyyyyyyyyyy')
			cover_exists = True
		else:
			print('no haaaaaaaaaaay')
			cover_exists = False

		obj = form.save(commit=False)
		obj.save()

		final_avatar_dir = 's/media/user/avatar/%s.png' % username

		if not obj.avatar == final_avatar_dir:
			avatar_dir = '%s/%s' % (settings.BASE_DIR, obj.avatar)
			os.rename(avatar_dir, final_avatar_dir)
			obj.avatar = final_avatar_dir
			obj.save()
			avatar_resize(final_avatar_dir)

		final_cover_dir = 's/media/user/cover/%s.png' % username

		def create_cover():
			cover_dir = '%s/%s' % (settings.BASE_DIR, obj.cover)
			os.rename(cover_dir, final_cover_dir)
			obj.cover = final_cover_dir
			obj.save()
			cover_resize(final_cover_dir)

		if not obj.cover == final_cover_dir:
			if os.path.isfile(final_cover_dir):
				create_cover()

		if obj.cover and not cover_exists: create_cover()

		return HttpResponseRedirect('/%s/edit' % self.kwargs['pk'])


class UserFollowCreate(CreateView):
	form_class = UserFollowForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.follower = self.request.user
		obj.follower.following_number += 1
		obj.follower.save()
		obj.followed = User.objects.get(username=self.kwargs['followed'])
		obj.followed.follower_number += 1
		obj.followed.save()
		obj.save()
		return HttpResponseRedirect(obj.get_absolute_url())


class UserFollowDelete(View):
	def post(self, *args, **kwargs):
		follower = self.request.user
		followed = User.objects.get(username=self.kwargs['unfollowed'])
		followid = '%s>%s' % (follower.pk, followed.pk)
		follow = UserFollow.objects.get(followid=followid)
		follow.delete()
		follower.following_number -= 1
		follower.save()
		followed.follower_number -= 1
		followed.save()
		return HttpResponseRedirect('/%s' % followed.pk)