from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.contrib.auth import authenticate, login

from user.models import User
from content.models import Post
from user.forms import SignUpForm
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

	def get_queryset(self):
		return Post.objects.by_user(user=self.kwargs['profile'])

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)
		context['profile'] = User.objects.get(username=self.kwargs['profile'])
		return context


class UsersView(ListView):
	template_name = 'user/user.html'
	model = User