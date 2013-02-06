#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from HW01 import hw1Handler
from HW02 import rot13Handler
from Blog import signupHandler
from Blog import loginHandler
from Blog import logoutHandler
from Blog import signupThanksHandler
from Blog import BlogHandler
from Blog import CreateHandler
from Blog import PostHandler
from Blog import timerRedirectHandler

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/blog')

app = webapp2.WSGIApplication( [('/', MainHandler), 
																('/signup', signupHandler),
																('/login', loginHandler),
																('/logout', logoutHandler),
																('/welcome', signupThanksHandler),
																('/blog/?(?:\.json)?', BlogHandler),
																('/blog/newpost', CreateHandler),
																('/blog/([0-9]+)(?:\.json)?', PostHandler),
																('/wait', timerRedirectHandler)], 
																debug=True)
