import re
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension


urlfinder = re.compile(r'(http[s]?://(?!www\.youtube\.com/watch\?\S*v=(?P<youtubeid>\S[^&/]+)|youtu\.be|(www.|)vimeo\.com/(?P<vimeoid>\d+)\S*)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')


class URLify(Preprocessor):
	def run(self, lines):
		return [urlfinder.sub(r'<\1>', line) for line in lines]


class URLifyExtension(Extension):
	def extendMarkdown(self, md, md_globals):
		md.preprocessors.add('urlify', URLify(md), '_end')
