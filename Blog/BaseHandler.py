#!usr/bin/env python

import os
import webapp2
import jinja2
from blackbox import HashStr
import logging
from user import User

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class TemplatedHTML:
	@classmethod
	def generate_page(cls, template, **template_params):
		#logging.info(template)
		#logging.info(str(template_params))
		#logging.info(str(self))
		t = jinja_env.get_template(template)
		page = t.render(template_params)
		#logging.info(page)
		return page


class WA2Handler(TemplatedHTML, webapp2.RequestHandler):
	# General write 
	def write(self, *a, **kw):
		#logging.info(str(*a))
		self.response.out.write(*a, **kw)

	# Template render function using TemplatedHTLM
	def render(self, template, **kw):
		#logging.info(str(self))
		page = self.generate_page(template, **kw)
		#logging.info(page)
		self.write(page)

	# Secure cookie helpers----------------------------------
	def delete_cookie(self, name):
		self.response.headers.add_header('Set-Cookie', "%s=; Thu, 01-Jan-1970 00:00:00 GMT; Path=/" % name)

	def set_cookie(self, name, data, save = False):
		dhash = HashStr.make_sstr(data)
		cookie = "%s=%s;" % (name, dhash)
		if save:
			cookie = cookie+" Expires= Tue, 1 Jan 2025 00:00:00 GMT;"
		cookie = cookie+" Path=/;"
		self.response.headers.add_header('Set-Cookie', cookie)

	def get_cookie(self, name):
		cookie = self.request.cookies.get(name)
		return cookie and HashStr.check_sstr(cookie)
	#--------------------------------------------------------

		
class BlogBaseHandler(WA2Handler):
	current_user = None

	def login(self, user, save = False):
		self.set_cookie('user_id', user.id_str(), save)
		self.current_user = user

	def logout(self):
		self.delete_cookie('user_id')

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.get_cookie('user_id')
		#logging.info(str(uid))
		if uid:
			#logging.info("uid is valid")
			self.current_user = User.get_by_id(int(uid))
		else:
			#logging.info("uid is NOT valid")
			self.current_user = None

	def renderBlog(self, template, **params):
		if self.current_user:
			params["usertools"] = TemplatedHTML.generate_page("usertoolbar-in.html", username = self.current_user.name)
		else:
			params["usertools"] = TemplatedHTML.generate_page("usertoolbar-out.html")

		self.render(template, **params)






