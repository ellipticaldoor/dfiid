from django.contrib.syndication.views import Feed
from blog.models import Post


class BlogFeed(Feed):
	title = "Trantoor blog"
	link = "/feed"
	description = "Latest Trantoor posts"

	def items(self):
		return Post.objects.published()[:5]
