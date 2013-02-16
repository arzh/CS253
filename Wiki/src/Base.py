#!usr/bin/env python

import os
import jinja2

import webapp2

from DB import User
from Blackbox import HashStr

import logging

class Jinja2HTML:
	def __init__(self):
		self.set_template_path()

	def set_template_path(self, path=""):
		template_dir = os.path.join(os.path.dirname(__file__), '../templates'+path)
		logging.info(template_dir)
		self.jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

	def generate_html(self, template, **tparams):
		t = self.jinja_env.get_template(template)
		return t.render(tparams)


class WA2Handler(webapp2.RequestHandler):
	#def __init__(self):
		#logging.info("WHAT")
		#webapp2.RequestHandler.__init__()
		#self.html_render = Jinja2HTML()
	def initialize(self, *a, **kw):
		super(WA2Handler, self).initialize(*a, **kw)
		self.html_render = Jinja2HTML()

	# General write 
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	# Template render function using TemplatedHTLM
	def render(self, template, **kw):
		page = self.html_render.generate_html(template, **kw)
		self.write(page)

	# Secure cookie helpers----------------------------------
	def delete_cookie(self, name):
		self.response.headers.add_header('Set-Cookie', "%s=; Path=/" % name)

	def set_cookie(self, name, data, save = False):
		dhash = HashStr.make_sstr(data)
		cookie = "%s=%s; Path=/;" % (name, dhash)
		if save:
			cookie = cookie+" Expires= Tue, 1 Jan 2025 00:00:00 GMT;"

		self.response.headers.add_header('Set-Cookie', cookie)

	def get_cookie(self, name):
		cookie = self.request.cookies.get(name)
		return cookie and HashStr.check_sstr(cookie)
	#--------------------------------------------------------

class UserPageBase(WA2Handler):
	current_user = None

	def login(self, user, save = False):
		self.set_cookie('user_id', user.id_str(), save)
		self.current_user = user

	def logout(self):
		self.delete_cookie('user_id')

	def cached_user(self):
		uid = self.get_cookie('user_id')
		if uid:
			return User.get_by_id(int(uid))
		else:
			return None

	def initialize(self, *a, **kw):
		super(UserPageBase, self).initialize(*a, **kw)
		self.current_user = self.cached_user()
