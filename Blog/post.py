#!usr/bin/env python

from google.appengine.ext import db
from BaseHandler import TemplatedHTML
from BaseDB import BaseDBModel

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