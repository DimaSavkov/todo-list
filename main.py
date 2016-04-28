#!/usr/bin/env python
import os
import webapp2
import jinja2
import json
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import users

from models import ToDoList

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url(self.request.uri)
        todo_list = []
        if user:
            login_url = users.create_logout_url(self.request.uri)
            todo_list = ToDoList.query(ToDoList.user == user).order(ToDoList.is_done, ToDoList.created)

        template_values = {
            'user': user,
            'login_url': login_url,
            'todo_list': todo_list
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class CreateToDoTask(webapp2.RequestHandler):
    """
    Save ToDo task in database, return its id
    """
    def post(self):
        todo = ToDoList(user=users.get_current_user(),
                        task=self.request.get('task_text'),
                        is_done=False)
        todo.put()
        self.response.write(json.dumps({'id': todo.key.id(), 'task-text': todo.task}))


class UpdateToDoTask(webapp2.RequestHandler):
    """
    Change task status
    """
    def get(self):
        todo_id = self.request.get('id')
        todo_id = int(todo_id)
        todo = ToDoList.get_by_id(todo_id)
        # If task was completed(is_done=True) open it
        if todo.is_done:
            todo.is_done = False
        # If task was uncompleted(is_done=False) close it
        else:
            todo.is_done = True
        todo.put()
        self.response.write(json.dumps('updated'))


class DeleteTodoTask(webapp2.RequestHandler):
    """
    Delete task form database
    """
    def get(self):
        todo_id = self.request.get('id')
        todo_id = int(todo_id)
        todo = ToDoList.get_by_id(todo_id)
        todo.key.delete()
        self.response.write(json.dumps('deleted'))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create', CreateToDoTask),
    ('/update', UpdateToDoTask),
    ('/delete', DeleteTodoTask)
], debug=True)