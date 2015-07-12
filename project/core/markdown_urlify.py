import markdown

# Global Vars
URLIZE_RE = r'(http[s]?://(?!www\.youtube\.com/watch\?\S*v=(?P<youtubeid>\S[^&/]+)|youtu\.be|(www.|)vimeo\.com/(?P<vimeoid>\d+)\S*)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'

class UrlizePattern(markdown.inlinepatterns.Pattern):
	""" Return a link Element given an autolink (`http://example/com`). """
	def handleMatch(self, m):
		url = m.group(2)

		if url.startswith('<'):
			url = url[1:-1]

		text = url

		if not url.split('://')[0] in ('http','https','ftp'):
			if '@' in url and not '/' in url:
				url = 'mailto:' + url
			else:
				url = 'http://' + url

		el = markdown.util.etree.Element("a")
		el.set('href', url)
		el.text = markdown.util.AtomicString(text)
		return el

class UrlizeExtension(markdown.Extension):
	""" Urlize Extension for Python-Markdown. """

	def extendMarkdown(self, md, md_globals):
		""" Replace autolink with UrlizePattern """
		md.inlinePatterns['autolink'] = UrlizePattern(URLIZE_RE, md)

def makeExtension(*args, **kwargs):
	return UrlizeExtension(*args, **kwargs)

if __name__ == "__main__":
	import doctest
	doctest.testmod()
