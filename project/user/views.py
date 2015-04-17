from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth import authenticate, login

from user.models import User
from content.models import Post
from user.forms import SignUpForm


class SignUpView(CreateView):
	form_class = SignUpForm
	template_name = 'user/signup.html'
	success_url = '/'

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.set_password(obj.password)
		obj.save()

		username = self.request.POST['username']
		password = self.request.POST['password']

		user = authenticate(username=username, password=password)
		login(self.request, user)

		return super(SignUpView, self).form_valid(form)


class ProfileView(DetailView):
	template_name = 'user/profile.html'
	model = User

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.by_user(self.kwargs['pk'])
		return context


class UsersView(ListView):
	template_name = 'user/users.html'
	model = User