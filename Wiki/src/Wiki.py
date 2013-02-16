#!usr/bin/env python

from Base import UserPageBase
from Toolbar import Toolbar
from DB import Page, Page_History

import logging

from google.appengine.ext import db
import string

def get_latest_ph(parent):
	p = Page_History.all().ancestor(parent).order('-created')
	return p[0]


class WikiHandler(UserPageBase):
	def render(self, template, **kw):
		logging.info("Page: " + self.request.path)
		kw["toolbar"] = Toolbar().generate_toolbar(page = self.request.path, user = self.current_user)
		super(WikiHandler, self).render(template, **kw)

	def get(self):
		self.render("view.html", content="Hello worlds")

class ViewPage(WikiHandler):
	def get(self, page_name):
		page_name = string.replace(page_name, '/', '')
		logging.info("PageName: " + page_name)
		p = Page.get_by("name", page_name+"page")
		if p:
			ph = get_latest_ph(p)
			self.render("view.html", page_data = ph.content)
		else:
			if page_name == '':
				p = Page(name = page_name+"page")
				p.put()
				ph = Page_History(content = "THE FRONT PAGE!", parent = p)
				ph.put()

			if self.current_user:
				logging.info("Redirect!")
				self.redirect('/_edit/%s' % page_name)
			else:
				self.redirect('/')

class EditPage(WikiHandler):
	def get(self, page_name):
		#page_name = self.request.path
		if self.current_user:
			page_name = string.replace(page_name, '/', '')
			p = Page.get_by("name", page_name+"page")
			if p:
				ph = get_latest_ph(p)
				self.render("edit.html", page_data = ph.content)
			else:
				p = Page(name = page_name+"page")
				p.put()
				self.render("edit.html", page_data = "")
		else:
			self.redirect(page_name)

	def post(self, page_name):
		#page_name = self.request.path
		page_name = string.replace(page_name, '/', '')
		p = Page.get_by("name", page_name+"page")
		content = self.request.get('content')
		ph = Page_History(content = content, parent = p)
		ph.put()

		re_page = '/%s' % page_name
		logging.info("redi to" + re_page)
		self.redirect(re_page)