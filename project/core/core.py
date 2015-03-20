import os
import datetime
from binascii import hexlify
from collections import OrderedDict


# TODO: Improve for 100% randomness 
def _createId(): return hexlify(os.urandom(3))


def archivize(posts):
	posts_by_year = {}

	for post in posts:
		post_year = post.pub_date.year
		date = datetime.datetime(post_year, post.pub_date.month, 1)

		if post_year not in posts_by_year:
			posts_by_year.update({post_year: []})

		if date not in posts_by_year[post_year]:
			posts_by_year[post_year].append(date)

	return OrderedDict(list(posts_by_year.items())[::-1])
