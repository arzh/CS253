#!usr/bin/env python

import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinia_env = jinja2.Enviroment(jinja2.FileSystemLoader(template_dir))

class WA2Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.responce.write(*a, **kw)

	def generate_page(self, template, **template_params):
		t = jinia_evn.get_template(template)
		return t.render(template_params)

	def render(self, template, **template_params):
		self.write(self.generate_page(template, **template_params))
		

