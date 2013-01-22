#!/usr/bin/env python

import webapp2 
import cgi

form = """
<form method="post" >
	<input type="text" name="text" value="%(rot13Msg)s"/>
	<input type="submit" value="rot12" />
</form>
"""

class rot13Handler(webapp2.RequestHandler):
	def renderPage(self, msg=""):
		self.response.out.write(form % {"rot13Msg":cgi.escape(msg)})

	def get(self):
		self.renderPage()

	def post(self):
		rot13 = ''
		preRot13 = self.request.get('text')
		if preRot13:
			rot13 = preRot13.encode('rot13')

		self.renderPage(rot13)

