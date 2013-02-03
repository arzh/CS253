#!usr/bin/env python

from BaseDB import BaseDBModel
from blackbox import HashUser
from google.appengine.ext import db

class User(BaseDBModel):
	name = db.StringProperty(required = True)
	phash = db.StringProperty(required = True)
	email = db.StringProperty(required = False)
	created = db.DateTimeProperty(auto_now_add = True)
	last_li = db.DateTimeProperty(auto_now = True)

	@staticmethod
	def generate_new(name, pw, email=None):
		h = HashUser.generate_phash(name, pw)
		return User(name = name, phash = h, email = email)
