from django.views.generic import ListView, DetailView

from user.models import User
from user_profile.models import Profile
from content.models import Post


class ProfileView(DetailView):
	template_name = 'user_profile/profile.html'
	model = Profile

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.by_user(self.kwargs['pk'])
		return context


class UsersView(ListView):
	template_name = 'user_profile/users.html'
	model = User