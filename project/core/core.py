from binascii import hexlify
from os import urandom
from PIL import Image
from numpy import random

from django.conf import settings


def random_avatar(username):
	a = random.rand(5,5,3) * 255
	avatar = Image.fromarray(a.astype('uint8')).convert('RGBA').resize((200,200))
	avatar_dir = '%s/s/media/img/avatar/%s.jpg' % (settings.BASE_DIR, username)
	avatar.save(avatar_dir)
	return


def _createId():
	return hexlify(urandom(3))