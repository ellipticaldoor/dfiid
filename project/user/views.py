from django.http import HttpResponseRedirect
from django.views.generic import View, UpdateView, CreateView, ListView
from django.contrib.auth import authenticate, login

from user.models import User, UserFollow
from content.models import Post
from user.forms import UserEditForm, SignUpForm, UserFollowForm
from core.core import random_avatar


class SignUpView(CreateView):
	form_class = SignUpForm
	template_name = 'user/signup.html'
	success_url = '/'

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.set_password(obj.password)
		obj.avatar = 's/media/user/avatar/%s.png' % (obj.username)
		obj.save()

		username = self.request.POST['username']
		password = self.request.POST['password']

		random_avatar(username)

		user = authenticate(username=username, password=password)
		login(self.request, user)

		return HttpResponseRedirect('/')


class ProfileView(ListView):
	template_name = 'user/profile.html'
	paginate_by = 10

	def get_queryset(self):
		return Post.objects.by_user(user=self.kwargs['profile'])

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)
		username = self.request.user.username
		profile = self.kwargs['profile']
		try: show = self.kwargs['show']
		except: show = False

		context['form'] = UserFollowForm
		context['profile'] = User.objects.get(username=profile)
		context['action'] = 'follow'

		if self.request.user.is_authenticated():
			if username == profile:
				context['action'] = 'edit'
			else:
				follow_state = UserFollow.objects.by_id(follow_id='%s>%s' % (username, profile))
				if follow_state: context['action'] = 'unfollow'
				else: context['action'] = 'follow'

		if show:
			if show == 'commit': context['profile_show'] = 'commit'
			else: context['profile_show'] = 'bio'
		else: context['profile_show'] = 'post'

		return context


class UserView(ListView):
	template_name = 'user/user.html'
	model = User


class UserEdit(UpdateView):
	template_name = 'user/user_update.html'
	form_class = UserEditForm
	get_absolute_url = '/'

	def get_queryset(self):
		return User.objects.filter(username=self.request.user)

	def form_valid(self, form):
		form.save()
		return HttpResponseRedirect('/user/%s/bio' % (self.kwargs['pk']))


class UserFollowCreate(CreateView):
	form_class = UserFollowForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.follower = self.request.user
		obj.followed = User.objects.get(username=self.kwargs['followed'])
		obj.save()
		return HttpResponseRedirect(obj.get_absolute_url())


class UserFollowDelete(View):
	def post(self, *args, **kwargs):
		unfollowed = self.kwargs['unfollowed']
		follow_id = '%s>%s' % (self.request.user, unfollowed)
		follow = UserFollow.objects.get(follow_id=follow_id)
		follow.delete()
		return HttpResponseRedirect('/user/%s' % (unfollowed))