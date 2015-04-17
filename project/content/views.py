from django.views.generic import ListView, DetailView

from user.models import User
from content.models import Post, PostComment


class FrontView(ListView):
	template_name = 'content/front.html'
	queryset = Post.objects.published()
	paginate_by = 2

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.template_name = 'content/ajax/posts.html'

		return super(FrontView, self).get(request, *args, **kwargs)


class PostView(DetailView):
	template_name = 'content/post_view.html'

	def get_queryset(self):
		pk, slug = self.kwargs['pk'], self.kwargs['slug']
		queryset = Post.objects.by_post(pk, slug)
		return queryset