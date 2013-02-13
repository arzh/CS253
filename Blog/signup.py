#!/usr/bin/env python


from user import User
from BaseHandler import BlogBaseHandler

import re
import logging


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

NORMAL_BOX = "norm-box"
ERROR_BOX = "error-box"

class inputData:
	isValid = True
	rndClass = NORMAL_BOX
	errorMsg = ""
	regex = ""
	data = ""
	name = ""

	def __init__(self, regex, name):
		self.regex = regex
		self.name = name
		self.data = ""
		self.reset()

	def reset(self):
		self.isValid = True
		self.rndClass = NORMAL_BOX
		self.errorMsg = ""

	def set_regex(self, regex):
		self.regex = regex

	def is_valid(self, data):
		self.data = data
		match = self.regex.match(data)
		if match == None:
			self.set_false()

	def set_false(self):
		self.isValid = False
		self.rndClass = ERROR_BOX
		self.errorMsg = "Invalid %s" % self.name


class signupHandler(BlogBaseHandler):
	userData = inputData(regex = USER_RE, name = "Username")
	passData = inputData(regex = PASS_RE, name = "Password")
	emailData = inputData(regex = EMAIL_RE, name = "Email")

	def renderSignup(self):
		#logging.info("userData:"+self.userData.data+" passData:"+self.passData.data+" emailData:"+self.emailData.data)
		self.renderHtml("signup.html", userData = self.userData, passData = self.passData, emailData = self.emailData)

	def resetErrors(self):
		self.userData.reset()
		self.passData.reset()
		self.emailData.reset()

	def get(self):
		self.resetErrors()
		self.renderSignup()

	def post(self):
		self.resetErrors()
		rawName = self.request.get("username")
		if rawName and User.get_by_name(rawName):
			self.userData.set_false()
			self.userData.errorMsg = "Username already taken"
		else:
			self.userData.is_valid(rawName)
		
		#logging.info("username is: %s", self.userError)

		rawPassword = self.request.get("password")
		rawVerify = self.request.get("verify")
		passwordsMatch = rawPassword == rawVerify

		if rawPassword and passwordsMatch:
			self.passData.is_valid(rawPassword)
		else:
			self.passData.set_false()
			self.passData.errorMsg = "Passwords do not match"

		#logging.info("password is: %s", self.passwordError)

		rawEmail = self.request.get("email")
		if rawEmail:
			self.emailData.is_valid(rawEmail)

		#logging.info("email is: %s", self.emailError)

		if not self.userData.isValid or not self.passData.isValid or not self.emailData.isValid:
			#logging.info("somethings gone wrong! userData:"+str(self.userData.isValid)+" passData: "+str(self.passData.isValid)+" emailData: "+str(self.emailData.isValid))
			self.renderSignup()
		else:
			#logging.info("it worked!")
			newUser = User.generate_new(rawName, rawPassword, rawEmail)
			newUser.put()
			self.login(newUser)
			self.redirect("/welcome")

class loginHandler(BlogBaseHandler):
	userData = inputData(regex = USER_RE, name = "Username")
	passData = inputData(regex = PASS_RE, name = "Password")

	def reset(self):
		self.userData.reset()
		self.passData.reset()

	def renderPage(self):
		#logging.info("userData:"+self.userData.data+" passData:"+self.passData.data+" emailData:"+self.emailData.data)
		self.renderHtml("login.html", userData = self.userData, passData = self.passData)

	def get(self):
		self.reset()
		self.renderPage()

	def post(self):
		self.reset()

		name = self.request.get("username")
		u = User.get_by_name(name)
		if not u:
			self.userData.set_false()
		else:
			pw = self.request.get("password")	
			if not u.check_password(pw):
				self.passData.set_false()

		if not self.userData.isValid or not self.passData.isValid:
			self.renderPage()
		else:
			self.login(u)
			self.redirect("/welcome")

class signupThanksHandler(BlogBaseHandler):
	def get(self):
		logging.info(str(self.current_user))
		if not self.current_user:
			self.redirect("/signup");
		else:
			self.write("Welcome %s!!!" % self.current_user.name)
			#self.redirect("/wait?timer=5&next=blog")

class logoutHandler(BlogBaseHandler):
	def get(self):
		self.logout()
		self.redirect('/signup')