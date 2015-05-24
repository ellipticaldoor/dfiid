
import os

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import View, UpdateView, CreateView, ListView
from django.contrib.auth import authenticate, login
from django import forms

from user.models import User, UserFollow
from content.models import Post, Commit
from user.forms import UserEditForm, SignUpForm, UserFollowForm
from core.core import random_avatar, avatar_resize


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
	paginate_by = 5

	def get(self, request, *args, **kwargs):
		if request.is_ajax(): self.template_name = 'ajax/post_list.html'
		return super(ProfileView, self).get(request, *args, **kwargs)

	def get_queryset(self):
		return Post.objects.by_user(user=self.kwargs['profile'])

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)
		username = self.request.user.username
		profile = self.kwargs['profile']
		try: context['profile_show'] = self.kwargs['show']
		except:
			context['profile_show'] = 'post'
			context['list_url'] = '/%s' % username

		context['form'] = UserFollowForm
		context['profile'] = User.objects.get(username=profile)
		context['action'] = 'follow'

		if self.request.user.is_authenticated():
			if username == profile:
				context['action'] = 'edit'
			else:
				follow_state = UserFollow.objects.by_id(followid='%s>%s' % (username, profile))
				if follow_state: context['action'] = 'unfollow'
				else: context['action'] = 'follow'

		if context['profile_show'] == 'commit':
			context['commits'] = Commit.objects.filter(user_id=profile)

		return context


class UserView(ListView):
	template_name = 'user/user.html'
	model = User


class UserEdit(UpdateView):
	template_name = 'user/edit.html'
	form_class = UserEditForm
	get_absolute_url = '/'

	def get_queryset(self):
		return User.objects.filter(username=self.request.user)

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.save()

		username = self.request.user
		final_avatar_dir = 's/media/user/avatar/%s.png' % username

		if not obj.avatar == final_avatar_dir:
			avatar_dir = '%s/%s' % (settings.BASE_DIR, obj.avatar)
			os.rename(avatar_dir, final_avatar_dir)
			obj.avatar = final_avatar_dir
			obj.save()
			avatar_resize(final_avatar_dir)

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