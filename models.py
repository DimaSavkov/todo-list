#!/usr/bin/python
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class ToDoList(ndb.Model):
    user = ndb.UserProperty(required=True)
    task = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    is_done = ndb.BooleanProperty()