from binascii import hexlify
from os import urandom
from PIL import Image, ImageFilter
from numpy import random

from django.conf import settings


def _createId():
	return hexlify(urandom(3))


def is_reserved(username):
	reserved_usernames = ['dfiid', 'admin', 'user', 'sub', 'post', 'anon', 'create',
						  'sub_follow', 'sub_unfollow', 'signup', 'login', 'logout',
						  'contact', 'about', 'legal', 'blog', 'rss', 'feed', 'robots',
						  'sitemap', 'settings', 'debug', 'top', 'new']

	for name in reserved_usernames:
		if name == username: return True
	return False


def random_avatar(username):
	a = random.rand(3,3,3) * 255
	avatar = Image.fromarray(a.astype('uint8')).convert('RGB').resize((300,300))
	avatar_dir = '%s/s/media/user/avatar/%s.png' % (settings.BASE_DIR, username)
	avatar.save(avatar_dir, 'PNG')
	return


def random_avatar_sub(sub_slug):
	a = random.rand(5,5,3) * 255
	avatar = Image.fromarray(a.astype('uint8')).convert('RGB').resize((100,100))
	avatar_dir = '%s/s/media/sub/image/%s.png' % (settings.BASE_DIR, sub_slug)
	avatar.save(avatar_dir, 'PNG')
	return


def avatar_resize(final_avatar_dir):
	THUMB_SIZE = 300, 300
	img = Image.open(final_avatar_dir)
	width, height = img.size

	if width > height:
		delta = width - height
		left = int(delta/2)
		upper = 0
		right = height + left
		lower = height
	else:
		delta = height - width
		left = 0
		upper = int(delta/2)
		right = width
		lower = width + upper

	img = img.crop((left, upper, right, lower))
	img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
	img.save(final_avatar_dir, 'PNG')
	return

def cover_resize(final_cover_dir):
	basewidth = 900
	img = Image.open(final_cover_dir)
	wpercent = (basewidth/float(img.size[0]))
	hsize = int((float(img.size[1])*float(wpercent)))
	img = img.resize((basewidth,hsize), Image.ANTIALIAS).crop((0, 0, 900, 210))
	img.save(final_cover_dir, 'PNG')
	return