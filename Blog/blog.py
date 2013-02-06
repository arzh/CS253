#!usr/bin/env python


from post import BlogPost
from google.appengine.ext import db
from BaseHandler import BlogBaseHandler
from BaseHandler import TemplatedHTML

error_class = "error-box"
reguler_class = "norm-box"


class BlogHandler(BlogBaseHandler):
	def get(self):
		posts = db.GqlQuery("select * from BlogPost order by created desc")

		if self.format == 'html':
			self.renderHtml("front.html", posts = posts)
		elif self.format == 'json':
			self.renderJson([p.as_dict() for p in posts])


class CreateHandler(BlogBaseHandler):
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
		self.renderHtml("newpost.html", title = title, tent = tent, titleerror = self.titleError, titleclass = self.titleClass, texterror = self.textError, textclass = self.textClass)

	def get(self):
		if not self.current_user:
			self.redirect("/login")
		else:
			self.reset_errors()
			self.render_newpost()

	def post(self):
		if not self.current_user:
			self.redirect("/login")
		else:
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
				p = BlogPost(subject = title, content = con, username = self.current_user.name)
				p.put()

				self.redirect(p.permalink())
			

class PostHandler(BlogBaseHandler):
	def get(self, post_id):
		post = BlogPost.get_by_id(int(post_id))
		if not post:
			self.error(404)

		if self.format == 'html':
			self.renderHtml("permalink.html", post = post)
		elif self.format == 'json':
			self.renderJson(post.as_dict())