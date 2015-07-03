from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView

from notify.models import Noty


class Notify(ListView):
	template_name = 'notify.html'
	paginate_by = 10

	def get_queryset(self):
		if self.kwargs['tab'] == 'new':
			return Noty.objects.filter(show=True)
		else:
			return Noty.objects.all()

	def get_context_data(self, **kwargs):
		context = super(Notify, self).get_context_data(**kwargs)
		context['tab_show'] = self.kwargs['tab']
		return context


class ReadNoty(View):
	# def post(self, request, *args, **kwargs):
	def get(self, request, *args, **kwargs):
		notyid = self.kwargs['notyid']

		noty = Noty.objects.get(notyid=notyid, user=self.request.user)
		noty.read_noty()

		# return HttpResponse(status=200)
		return HttpResponseRedirect('/notify')
