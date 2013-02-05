#!usr/bin/env python
import hmac
import random
import string
import hashlib

hash_sec = "nsecTOPLINEfromwaaaaaaaydown253andsoforth"

def make_salt():
	return ''.join(random.choice(string.letters) for x in xrange(10))

class HashStr:
	@staticmethod
	def hash_str(s):
		return hmac.new(hash_sec, s).hexdigest()

	@staticmethod
	def make_sstr(s):
		return "%s|%s" % (s, HashStr.hash_str(s))

	@staticmethod
	def check_sstr(h):
		s = h.split('|')[0]
		if h == HashStr.make_sstr(s):
			return s

class HashUser:
	@staticmethod
	def generate_phash(name, pw, salt=None):
		if not salt:
			salt = make_salt()
		h = hashlib.sha256(name + pw + salt).hexdigest()
		return "%s,%s" % (h, salt)

	@staticmethod
	def break_salt(phash):
		return phash.split(',')[1]
