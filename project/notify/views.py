from django.views.generic import ListView

from notify.models import Noty


class Notify(ListView):
	template_name = 'notify/base.html'
	model = Noty