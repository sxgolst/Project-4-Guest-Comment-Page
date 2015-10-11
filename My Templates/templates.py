import os

import jinja2
import webapp2
import cgi
import urllib

# import users and db
from google.appengine.api import users
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Contact(db.Model):  # Inherit class from db.Model
    # Define the properties that our Contacts will have
    # Associate these properties with Datastore Properties
    name = db.StringProperty()
    email = db.StringProperty()
    comment = db.StringProperty(multiline=True)
    date_added = db.DateTimeProperty(auto_now_add=True)
    last_updated = db.DateTimeProperty(auto_now=True)

  

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
        def render(self, template, **kw):
            self.write(self.render_str(template, **kw)) 

class RetrieveHandler(webapp2.RequestHandler):
    def get(self):
        # Retrieve the contact from the database
        
        stanley_contact = Contact.query(Contact.name == 'Stanley').get()

        # Display the contact to the user on the page.
        output = "Name: %s" % stanley_contact.name
        output = output + "<br>"
        output = output + "Email: %s" % stanley_contact.email
        output = output + "<br>"
        output = output + "comment: %s" % stanley_contact.comment  
                                  

class GuestHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get(self):
        notes = self.request.get('notes')
        print 'This is the contents of notes: ', notes
        if notes:
            if notes == 'Lesson1.html':
                # display the lesson 1 notes
                #self.response.write("The value is notes 1!")
                self.render("Lesson1.html")
            elif notes == 'Lesson2.html':
                # display the lesson 2 notes
                #self.response.write("The value is notes 2!")
                self.render("Lesson2.html")
            elif notes == 'Lesson3.html':
                # display the lesson 3 notes
                #self.response.write("The value is notes 3!")
                self.render("Lesson3.html")
            elif notes == 'Lesson4.html':
                # display the lesson 4 notes
                #self.response.write("The value is notes 4!")
                self.render("Lesson4.html")
        else:
            self.render("dropdown.html")
                   

    def escape_html(s):
        return cgi.escape(s, quote = True)
            

    def post(self):
        contact = Contact()
        contact.name = self.request.get('name')
        contact.email = self.request.get('email')
        contact.comment = self.request.get('content')
        if not (contact.name and contact.email and contact.comment):
            error = 'Field/s can not be left blank.'
            self.render("dropdown.html",error=error)
        else:
            contact.put()
            self.redirect("/thanks")
            import time
            time.sleep(5)
             

class ThanksHandler(GuestHandler):
    def get(self):
        comments=Contact.all()
        self.render("thanks.html", list_of_comments=comments)
         
         
 

        
                     
                        
             

app = webapp2.WSGIApplication([('/guest', GuestHandler),
                               ('/retrieve', RetrieveHandler),
                               ('/thanks', ThanksHandler),
                             ],
                              debug=True)
