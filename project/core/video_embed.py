import markdown
from markdown.util import etree


class CustomVideoExtension(markdown.Extension):
	def add_inline(self, md, name, klass, re):
		pattern = klass(re)
		pattern.md = md
		pattern.ext = self
		md.inlinePatterns.add(name, pattern, '<reference')

	def extendMarkdown(self, md, md_globals):
		self.add_inline(md, 'vimeo', Vimeo,
			r'([^(]|^)https?://(www.|)vimeo\.com/(?P<vimeoid>\d+)\S*')
		self.add_inline(md, 'youtube', Youtube,
			r'([^(]|^)https?://www\.youtube\.com/watch\?\S*v=(?P<youtubeid>\S[^&/]+)')
		self.add_inline(md, 'youtube_short', Youtube,
			r'([^(]|^)https?://youtu\.be/(?P<youtubeid>\S[^?&/]+)?')


class Vimeo(markdown.inlinepatterns.Pattern):
	def handleMatch(self, m):
		return render_iframe(m.group('vimeoid'), 'vimeo')


class Youtube(markdown.inlinepatterns.Pattern):
	def handleMatch(self, m):
		return render_iframe(m.group('youtubeid'), 'youtube')


def render_iframe(data_id, player):
	div_container = etree.Element('div')
	div_container.set('class', 'video_container')
	div = etree.SubElement(div_container, 'div')
	div.set('class', '%s_player player' % player)
	div.set('data-id', data_id.replace(" ", ""))
	return div_container


def makeExtension(**kwargs):
	return VideoExtension(**kwargs)