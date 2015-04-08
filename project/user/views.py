from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from user.forms import RegistrationForm
from user.models import User


class RegistrationView(CreateView):
	form_class = RegistrationForm
	template_name = 'registration/register.html'
	model = User

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.save()
		# Crear perfil y usuario
		print(obj.username)
		print(obj.password)
		return HttpResponseRedirect('/')