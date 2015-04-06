from django.contrib.syndication.views import Feed
from content.models import Post


class ContentFeed(Feed):
	title = "dfiid content"
	link = "/feed"
	description = "Latest Trantoor posts"

	def items(self):
		return Post.objects.published()[:5]