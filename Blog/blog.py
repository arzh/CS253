#!usr/bin/env python

from google.appengine.ext import db

from BaseHandler import WA2Handler
from BaseHandler import TemplatedHTML

error_class = "error-box"
reguler_class = "norm-box"

class BlogPost(TemplatedHTML, db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_md = db.DateTimeProperty(auto_now = True)

	def render(self):
		self._render_text = self.content.replace('\n', "<br>");
		return self.generate_page("post.html", post = self)

class BlogHandler(WA2Handler):
	def get(self):
		posts = db.GqlQuery("select * from BlogPost order by created desc")
		self.render("front.html", posts = posts)

class CreateHandler(WA2Handler):
	def reset_errors(self):
		self.has_title_error = False
		self.has_text_error = False
		self.titleError = ""
		self.titleClass = reguler_class
		self.textError = ""
		self.textClass = reguler_class

	def handle_errors(self):
		if self.has_title_error:
			self.titleError = "You must have a title"
			self.titleClass = error_class

		if self.has_text_error:
			self.textError = "You must have content"
			self.textClass = error_class

	def render_newpost(self, title="", tent=""):
		self.render("newpost.html", title = title, tent = tent, titleerror = self.titleError, titleclass = self.titleClass, texterror = self.textError, textclass = self.textClass)

	def get(self):
		self.reset_errors()
		self.render_newpost()

	def post(self):
		self.reset_errors()

		title = self.request.get("subject")
		con = self.request.get("content")

		if title == "":
			self.has_title_error = True
		if con == "":
			self.has_text_error = True

		self.handle_errors()

		if self.has_text_error or self.has_title_error:
			self.render_newpost(title, con)
		else:
			p = BlogPost(subject = title, content = con)
			p.put()

			post_id = str(p.key().id())
			permalink = "/Blog/%s" % post_id
			self.redirect(permalink)
			

class PostHandler(WA2Handler):
	def get(self, post_id):
		post = BlogPost.get_by_id(int(post_id))
		if post:
			self.render("permalink.html", post = post)
		else:
			self.write("Post No exist!")