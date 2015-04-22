from binascii import hexlify
from os import urandom
from PIL import Image, ImageFilter
from numpy import random

from django.conf import settings


def random_avatar(username):
	a = random.rand(3,3,3) * 255
	avatar = Image.fromarray(a.astype('uint8')).convert('RGB').resize((300,300))
	avatar_dir = '%s/s/media/user/avatar/%s.png' % (settings.BASE_DIR, username)
	avatar.save(avatar_dir, 'PNG')
	return


def random_fractal(sub_slug):
	a = random.rand(7,7,3) * 255
	avatar = Image.fromarray(a.astype('uint8')).convert('RGB').resize((100,100))
	avatar_dir = '%s/s/media/sub/image/%s.png' % (settings.BASE_DIR, sub_slug)
	avatar.save(avatar_dir, 'PNG')
	return


def _createId():
	return hexlify(urandom(3))