from django.views.generic import ListView, DetailView

from user.models import User
from content.models import Post


class FrontView(ListView):
	template_name = 'content/front.html'
	queryset = Post.objects.published()[:1]

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


class AjaxContentView(ListView):
	template_name = 'content/ajax/posts.html'

	def get_queryset(self):
		query = self.request.GET.get('query')
		if query: queryset = Post.objects.published()
		else: queryset = Post.objects.published()[:1]
		return queryset