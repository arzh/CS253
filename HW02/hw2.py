#!/usr/bin/env python

import webapp2

class hw2Handler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world from hw2!')