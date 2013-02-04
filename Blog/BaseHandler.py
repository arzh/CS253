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
	def generate_page(self, template, **template_params):
		#logging.info(template)
		#logging.info(str(template_params))
		logging.info(str(self))
		t = jinja_env.get_template(template)
		page = t.render(template_params)
		logging.info(page)
		return page


class WA2Handler(TemplatedHTML, webapp2.RequestHandler):
	def write(self, *a, **kw):
		logging.info(str(*a))
		self.response.out.write(*a, **kw)

	def render(self, template, **kw):
		logging.info(str(self))
		page = self.generate_page(template, **kw)
		logging.info(page)
		self.write(page)

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

		
class BlogBaseHandler(WA2Handler):
	current_user = None
	save_user = False

	#TODO: Add login to save cookie
	#TODO: Add logout to delete the cookie

	def set_user_cookie(self):
		if self.current_user and self.save_user:
			self.set_cookie("user", self.current_user.id_str(), True)
		else:
			self.set_cookie("user", self.current_user.id_str())

	def initilize




