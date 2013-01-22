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
from HW02 import signupHandler
from HW02 import signupThanksHandler

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Welcome to CS253 home work')

app = webapp2.WSGIApplication( [('/', MainHandler), 
								('/HW1', hw1Handler),
								('/HW2/rot13', rot13Handler),
								('/HW2/signup', signupHandler),
								('/HW2/signup/thanks', signupThanksHandler),
								('/Blog', BlogHandler),
								('/Blog/newpost', CreateHandler),
								('/Blog/([0-9]+)', PostHandler)], 
								debug=True)
