from django.views.generic import ListView
from django.views.generic.edit import CreateView

from sub.models import Sub
from sub.forms import SubForm


class CreateSubView(CreateView):
	template_name = 'sub/create_sub.html'
	model = Sub
	form_class = SubForm
	success_url = '/subs'


class SubsView(ListView):
	template_name = 'sub/subs.html'
	model = Sub