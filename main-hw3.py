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
from HW03 import BlogHandler
from HW03 import CreateHandler
from HW03 import PostHandler


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("welcome to webapp2")

app = webapp2.WSGIApplication( [('/', MainHandler), 
																('/blog', BlogHandler),
																('/blog/newpost', CreateHandler),
																('/blog/([0-9]+)', PostHandler)], 
																debug=False)
