from django.views.generic import CreateView
from django.contrib.auth import authenticate, login

from user.forms import SignUpForm
from user_profile.models import Profile


class SignUpView(CreateView):
	form_class = SignUpForm
	template_name = 'user/signup.html'
	success_url = '/'

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.set_password(obj.password)
		obj.save()

		Profile.objects.create_profile(user=obj)

		username = self.request.POST['username']
		password = self.request.POST['password']

		user = authenticate(username=username, password=password)
		login(self.request, user)

		return super(SignUpView, self).form_valid(form)