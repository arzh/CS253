#!/usr/bin/env python

import webapp2
import cgi
import re
import logging

form="""
<form method="post">
	<label> Username <input style="%(userES)s" type="text" name="username" value="%(userMsg)s" /> %(userEM)s </label>
	<br>
	<label> Password <input style="%(passES)s" type="password" name="password" /> </label>
	<br>
	<label> Verify <input style="%(passES)s" type="password" name="verify" /> %(passEM)s </label>
	<br>
	<label> email <input style="%(emailES)s" type="text" name="email" value="%(emailMsg)s" /> %(emailEM)s </label>
	<br>
	<input type="submit"/>
</form>
"""

errorCSS="border: 1px solid red"


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


class signupHandler(webapp2.RequestHandler):

	def resetErrors(self):
		self.userError = False
		self.passwordError = False
		self.emailError = False

	def renderPage(self, userMsg='', emailMsg=''):
		userES = ''
		userEM = ''
		passES = ''
		passEM = ''
		emailES = ''
		emailEM = ''

		if self.userError:
			userES = errorCSS
			userEM = "Username is incorrect!"

		if self.passwordError:
			passES = errorCSS
			passEM = "Password is incorrect!"

		if self.emailError:
			emailES = errorCSS
			emailEM = "Email is incorrect!"

		self.response.out.write(form % {"userES":userES, "userMsg":cgi.escape(userMsg), "userEM":userEM, "passES":passES, "passEM":passEM, "emailES":emailES, "emailMsg":cgi.escape(emailMsg), "emailEM":emailEM})

	def get(self):
		self.resetErrors()
		self.renderPage()

	def validate_username(self, username):
		match = USER_RE.match(username)
		if match == None:
			return False
		else:
			return True

	def validate_password(self, password):
		match = PASS_RE.match(password)
		if match == None:
			return False
		else:
			return True

	def validate_email(self, email):
		match = EMAIL_RE.match(email)
		if match == None:
			return False
		else:
			return True

	def post(self):
		self.resetErrors()
		rawUser = self.request.get("username")
		if rawUser:
			self.userError = not self.validate_username(rawUser)
		else:
			self.userError = True

		logging.error("username is: %s", self.userError)

		rawPassword = self.request.get("password")
		rawVerify = self.request.get("verify")
		passwordsMatch = rawPassword == rawVerify

		if rawPassword and passwordsMatch:
			passwordError = not self.validate_password(rawPassword)
		else:
			self.passwordError = True

		logging.error("password is: %s", self.passwordError)

		rawEmail = self.request.get("email")
		if rawEmail:
			self.emailError = not self.validate_email(rawEmail)

		logging.error("email is: %s", self.emailError)

		if self.userError or self.passwordError or self.emailError:
			self.renderPage(rawUser, rawEmail)
		else:
			self.redirect("/HW2/signup/thanks?username=%s" % rawUser)


class signupThanksHandler(webapp2.RequestHandler):
	def get(self):
		username = self.request.get("username")
		welcomeMsg = "Thanks for signing up %s!" % username 
		self.response.out.write(welcomeMsg)