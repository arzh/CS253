#!usr/bin/env python

# Database model definitions for use in the wiki

from google.appengine.ext import db
from Blackbox import HashUser

class BaseDBModel(db.Model):
		def id_str(self):
			return str(self.key().id())

		@classmethod
		def get_by(cls, property_name, value):
			ftr = '%s =' % property_name
			return cls.all().filter(ftr, value).get()

class User(BaseDBModel):
	name = db.StringProperty(required = True)
	phash = db.StringProperty(required = True)
	email = db.StringProperty(required = False)
	created = db.DateTimeProperty(auto_now_add = True)
	last_li = db.DateTimeProperty(auto_now = True)

#TODO: remove these methods and add them to the SecUser(formally HashUser) class
	@classmethod
	def generate_new(cls, name, pw, email=None):
		h = HashUser.generate_phash(name, pw)
		return User(name = name, phash = h, email = email)

	def check_password(self, pw):
		salt = HashUser.break_salt(self.phash)
		return self.phash == HashUser.generate_phash(self.name, pw, salt)


# Page model used as a parent for Page_Updates that hold 
# the content of the page being updated
class Page(BaseDBModel):
	name = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)

class Page_History(BaseDBModel):
	content = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)
