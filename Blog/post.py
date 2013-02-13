#!usr/bin/env python

from google.appengine.ext import db
import BaseHandler
from BaseHandler import TemplatedHTML
from BaseDB import BaseDBModel

from datetime import datetime, timedelta
from google.appengine.api import memcache

def age_set(key, value):
	cur_time = datetime.utcnow()
	memcache.set(key, (value, cur_time))

def age_get(key):
	r = memcache.get(key)
	if r:
		val, save_time = r
		age = (datetime.utcnow() - save_time).total_seconds()
	else:
		val, age = None, 0

	return val, age


class PostDB(BaseDBModel):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	username = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_md = db.DateTimeProperty(auto_now = True)

class BlogPost(TemplatedHTML, PostDB):
	def render(self):
		self._render_text = self.content.replace('\n', "<br>")
		return self.generate_page("post.html", post = self)

	def permalink(self):
		return "/blog/%s" % self.id_str()

	def as_dict(self):
		post_dict = {'subject': self.subject,
								 'content': self.content,
								 'username': self.username,
								 'created': self.created.strftime('%c'),
								 'last_mod': self.last_md.strftime('%c')}
		return post_dict

	@classmethod
	def add_post(cls, p):
		p.put()
		BlogPost.get_posts(update = True)

	@classmethod
	def get_posts(cls, update = False):
		ckey = 'BLOGS'

		posts, age = age_get(ckey)
		if update or posts is None:
			qur_posts = db.GqlQuery("select * from BlogPost order by created desc")
			posts = list(qur_posts)
			age_set(ckey, posts)

		return posts, age

	@classmethod
	def get_permalink(cls, post_id):
		ckey = "Post"+str(post_id)

		post, age = age_get(ckey)
		if post is None:
			post = BlogPost.get_by_id(post_id)
			age_set(ckey, post)

		return post, age