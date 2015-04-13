from django.views.generic import ListView, DetailView

from user.models import User
from content.models import Post


class FrontView(ListView):
	template_name = 'content/front.html'
	queryset = Post.objects.published()[:2]


class PostView(DetailView):
	template_name = 'content/post_view.html'

	def get_queryset(self):
		pk, slug = self.kwargs['pk'], self.kwargs['slug']
		queryset = Post.objects.by_post(pk, slug)
		return queryset


class PostBySubView(ListView):
	template_name = 'content/post_list.html'

	def get_queryset(self):
		sub = self.kwargs['sub']
		queryset = Post.objects.by_sub(sub)
		return queryset