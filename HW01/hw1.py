#!/usr/bin/env python

import webapp2

class hw1Handler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world from hw1!')
