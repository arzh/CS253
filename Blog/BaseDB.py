#!usr/bin/env python

from google.appengine.ext import db

class BaseDBModel(db.Model):
		def id_str(self):
			return str(self.key().id())