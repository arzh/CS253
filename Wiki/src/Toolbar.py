#!usr/bin/env python

from Base import Jinja2HTML

class Toolbar(Jinja2HTML):
	def __init__(self):
		self.user_template = "user.html"
		self.login_template = "login.html"
		self.set_template_path('/toolbar')


	def generate_toolbar(self, page, user):
		if user:
			tb_html = self.generate_html(self.user_template, page = page, username = user.name)
		else:
			tb_html = self.generate_html(self.login_template)

		return tb_html