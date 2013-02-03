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
		
class BlogBaseHandler(WA2Handler):
	current_user = None
	save_user = False
	def get_user_from_cookie(self):
		self.response.headers['Content-Type'] = 'text/plain'
		cookie = self.request.cookies.get('user', "")
		logging.info("Getuser cookie:"+cookie)
		if cookie:
			user_id = HashStr.check_sstr(cookie)
			logging.info("Cookie worked: user_id:"+user_id)
			self.current_user = User.get_by_id(int(user_id))

	def set_new_user(self, user):
		self.current_user = user
		self.set_user_cookie()

	def set_user_cookie(self):
		if self.current_user and self.save_user:
			self.response.headers.add_header('Set-Cookie', "user="+HashStr.make_sstr(self.current_user.id_str()) + "; Expires= Tue, 1 Jan 2025 00:00:00 GMT")
		else:
			self.response.headers.add_header('Set-Cookie', "user="+HashStr.make_sstr(self.current_user.id_str()))




