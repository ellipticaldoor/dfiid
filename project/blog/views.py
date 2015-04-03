from django.views.generic import ListView, DetailView

from user.models import User
from blog.models import Post, Tag


class FrontView(ListView):
	template_name = 'blog/front.html'
	queryset = Post.objects.published()
	paginate_by = 5


class PostView(DetailView):
	template_name = 'blog/post_view.html'

	def get_queryset(self):
		pk, slug = self.kwargs['pk'], self.kwargs['slug']
		queryset = Post.objects.by_post(pk, slug)
		return queryset


class PostTagView(ListView):
	template_name = 'blog/post_list.html'

	def get_queryset(self):
		tag = self.kwargs['tag']
		queryset = Post.objects.by_tag(tag)
		return queryset


class PostDateView(ListView):
	template_name = 'blog/post_list.html'

	def get_queryset(self):
		year, month = self.kwargs['year'], self.kwargs['month']
		queryset = Post.objects.by_date(year, month)
		return queryset


class ArchiveView(ListView):
	template_name = 'blog/archive.html'
	model = Tag

	def get_context_data(self, **kwargs):
		context = super(ArchiveView, self).get_context_data(**kwargs)
		context['authors'] = User.objects.all()
		return context


class AuthorView(DetailView):
	template_name = 'blog/profile.html'
	model = User

	def get_context_data(self, **kwargs):
		context = super(AuthorView, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.by_author(self.kwargs['pk'])
		return context
