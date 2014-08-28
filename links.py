import datetime
import json
import random
import time
from urlparse import urljoin, urlparse, urlunparse
from urllib import quote

import webapp2
import webapp2_extras.routes

from google.appengine.ext import ndb

# Characters from which an id will be randomly generated
ID_CHARS = 'ABCDEFGHJKLMNOPQRSTUVWXYZ23456789'


class Redirect(ndb.Model):
    """Model an individual redirect with destination, key and created and
    modified timestamps."""

    ANCESTOR_KEY = ndb.Key('Redirects', 'richwareham.com')

    destination = ndb.StringProperty(required=True)
    reserved = ndb.BooleanProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    modified_at = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    @ndb.transactional
    def reserve(cls, id):
        if id is None or id == '':
            # Generate random id
            id = ''.join(random.sample(ID_CHARS, 5))

        # Check that this id doesn't exist or, if it does exist, that it is
        # reserved
        redirect_key = ndb.Key(Redirect, id, parent=Redirect.ANCESTOR_KEY)
        redirect = redirect_key.get()
        if redirect is not None and not redirect.reserved:
            raise ValueError('Redirect already exists')

        # So redirect is None or it is reserved
        if redirect is None:
            redirect = Redirect(id=id, destination='', reserved=True,
                    parent=Redirect.ANCESTOR_KEY)

        return redirect.put()

    @classmethod
    @ndb.transactional
    def assign_reserved(cls, id, destination):
        redirect_key = ndb.Key(Redirect, id, parent=Redirect.ANCESTOR_KEY)
        redirect = redirect_key.get()

        # Redirect must exist and not be reserved
        if redirect is None:
            raise ValueError('Redirect had not been reserved')
        if not redirect.reserved:
            raise ValueError('Redirect already exists')

        # Set fields and save
        redirect.destination = destination
        redirect.reserved = False
        return redirect.put()

    @classmethod
    def get(cls, id_):
        return ndb.Key(Redirect, id_, parent=Redirect.ANCESTOR_KEY).get()

    @classmethod
    def all(cls):
        """Return a list of non-reserved mappings ordered by descending
        modified date."""
        return cls.query(Redirect.reserved == False,
                ancestor=Redirect.ANCESTOR_KEY).order(-cls.created_at)

    @classmethod
    def get_non_reserved(cls, id):
        redirect = ndb.Key(Redirect, id, parent=Redirect.ANCESTOR_KEY).get()
        if redirect is None:
            raise KeyError
        if redirect.reserved:
            raise KeyError
        return redirect

class LinkHandler(webapp2.RequestHandler):
    def get(self, key):
        try:
            # Send redirect
            self.response.headers['Location'] = \
                Redirect.get_non_reserved(key).destination.encode('utf-8')
            self.response.status = 302
        except KeyError:
            # Didn't find this link!
            self.response.status = 404
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(self.response.http_status_message(404))

class ListHandler(webapp2.RequestHandler):
    def get(self):
        redirects = []
        for r in Redirect.all():
            redirects.append({
                'from': r.key.id(),
                'to': r.destination,
                'created': r.created_at.isoformat(),
                'modified': r.modified_at.isoformat(),
                'urls': {
                    'self': urljoin(self.request.host_url, self.uri_for('link', key=r.key.id())),
                    'edit': urljoin(self.request.host_url, self.uri_for('edit', key=r.key.id())),
                    'delete': urljoin(self.request.host_url, self.uri_for('delete', key=r.key.id())),
                },
            })

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(redirects))

class NewLinkHandler(webapp2.RequestHandler):
    def get(self, key):
        # Allocate new key
        try:
            redirect_key = Redirect.reserve(key)
        except ValueError as e:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Error: {0}\n'.format(e.message))
            self.response.write(self.response.http_status_message(400))
            self.response.status = 400
            return

        if key == '':
            # Send redirect to new page
            self.response.headers['Location'] = urljoin(
                    self.request.host_url, self.uri_for('new', key=redirect_key.id()))
            self.response.status = 302
            return

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('''<!doctype html>
<html>
    <head>
        <title>Create new link</title>
    </head>
    <body>
        <form method="post" action="{action}">
            {host}/@{key} to
            <input type="text" name="destination">
            <input type="submit">
        </form>
    </body>
</html>'''.format(
                action=self.uri_for('new', key=redirect_key.id()),
                host=self.request.host_url,
                key=quote(redirect_key.id())))

    def post(self, key):
        if key == '':
            self.response.headers['Content-Type'] = 'text/html'
            self.response.status = 400
            self.response.write(self.response.http_status_message(400))
            return

        destination = self.request.get('destination')
        if destination is None or destination == '':
            self.response.headers['Content-Type'] = 'text/html'
            self.response.status = 400
            self.response.write('Invalid destination\n')
            self.response.write(self.response.http_status_message(400))
            return

        # Normalise scheme
        if '/' not in destination:
            destination = '//' + destination
        destination = urlunparse(urlparse(destination, 'http'))

        # Set redirect
        try:
            redirect_key = Redirect.assign_reserved(key, destination)
        except ValueError as e:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Error: {0}\n'.format(e.message))
            self.response.write(self.response.http_status_message(400))
            self.response.status = 400
            return

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('''<!doctype html>
<html>
    <head>
        <title>Created new link</title>
    </head>
    <body>
        <a href="{host}/@{key}">{host}/@{key}</a>
        created.
    </body>
</html>'''.format(host=self.request.host_url, key=quote(redirect_key.id())))

class EditLinkHandler(webapp2.RequestHandler):
    def get(self, key):
        redirect = Redirect.get_non_reserved(key)
        if redirect is None:
            self.response.status = 404
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(self.response.http_status_message(404))
            return

        redirect_key = redirect.key
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('''<!doctype html>
<html>
    <head>
        <title>Edit link</title>
    </head>
    <body>
        <form method="post" action="{action}">
            Change {host}/@{key} from {destination} to
            <input type="text" name="destination">
            <input type="submit">
        </form>
    </body>
</html>'''.format(
                action=self.uri_for('edit', key=redirect_key.id()),
                destination=redirect.destination,
                host=self.request.host_url,
                key=quote(redirect_key.id())))

    def post(self, key):
        redirect = Redirect.get_non_reserved(key)
        if redirect is None:
            self.response.status = 404
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(self.response.http_status_message(404))
            return

        destination = self.request.get('destination')
        if destination is None or destination == '':
            self.response.headers['Content-Type'] = 'text/html'
            self.response.status = 400
            self.response.write('Invalid destination\n')
            self.response.write(self.response.http_status_message(400))
            return

        # Normalise scheme
        if '/' not in destination:
            destination = '//' + destination
        destination = urlunparse(urlparse(destination, 'http'))

        # Set redirect
        redirect.destination = destination
        redirect.put()

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('''<!doctype html>
<html>
    <head>
        <title>Created new link</title>
    </head>
    <body>
        <a href="{host}/@{key}">{host}/@{key}</a>
        updated.
    </body>
</html>'''.format(host=self.request.host_url, key=quote(redirect.key.id())))

class DeleteLinkHandler(webapp2.RequestHandler):
    def get(self, key):
        redirect = Redirect.get(key)
        if redirect is None:
            self.response.status = 404
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(self.response.http_status_message(404))
        else:
            redirect.key.delete()
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Deleted {0}'.format(key))

application = webapp2.WSGIApplication([
    webapp2.Route(r'/@', handler=ListHandler, name='list'),
    webapp2.Route(r'/@<key>', handler=LinkHandler, name='link'),
    webapp2.Route(r'/@<key:[^/]*>/new', handler=NewLinkHandler, name='new'),
    webapp2.Route(r'/@<key>/edit', handler=EditLinkHandler, name='edit'),
    webapp2.Route(r'/@<key>/delete', handler=DeleteLinkHandler, name='delete'),
], debug=True)
