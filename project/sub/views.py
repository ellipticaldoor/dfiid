from django.views.generic import ListView
from django.views.generic.edit import CreateView

from sub.models import Sub
from content.models import Post
from sub.forms import SubForm


class CreateSubView(CreateView):
	template_name = 'sub/create_sub.html'
	model = Sub
	form_class = SubForm
	success_url = '/sub'


class SubView(ListView):
	template_name = 'sub/sub.html'
	model = Sub


class SubContentView(ListView):
	template_name = 'content/post_list.html'

	def get_queryset(self):
		sub = self.kwargs['sub']
		queryset = Post.objects.by_sub(sub)
		return queryset