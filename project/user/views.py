from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView, RedirectView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


class LoginView(FormView):
	form_class = AuthenticationForm
	template_name = 'user/auth/login.html'
	success_url =  reverse_lazy('cms_post_list')

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect(self.get_success_url())
		else:
			return super(LoginView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		login(self.request, form.get_user())
		return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
	pattern_name = 'login'

	def get(self, request, *args, **kwargs):
		logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)
