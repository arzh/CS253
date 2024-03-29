#!usr/bin/env python

import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class TemplatedHTML:
	def generate_page(self, template, **template_params):
		t = jinja_env.get_template(template)
		page = t.render(template_params)
		return page


class WA2Handler(TemplatedHTML, webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render(self, template, **kw):
		self.write(self.generate_page(template, **kw))
		

