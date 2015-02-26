---
layout: post
title: "HMAC: How I securely deploy to this site from Travis CI"
coveralt: "CC-BY-SA from https://secure.flickr.com/photos/cogdog/8431502575"
cover: images/fingerprint.jpg
---

# Overview

This website has dynamic content like my [link
shortener](https://www.richwareham.com/links) and static content like this blog
post. I have Travis CI set up to build my website's static content whenever a
new commit is made to the github repository. My website has a very simple
method of updating itself: HTTP POST-ing a zip file to a magic URL will unzip
that file over the static file directory. This post is how I try to secure that
mechanism while preserving the simplicity of a "deploy via cURL" model.

# The problem

This website's source is [hosted on
github](https://github.com/rjw57/richwareham.com) although the site itself is
hosted on [OpenShift](https://www.openshift.com/). If you look at the site's
source code you'll see that it's just a pretty simple Python web application
using the [flask](http://flask.pocoo.org/) web framework for Python.

Another thing you might notice is that none of the content is in that
repository. That's because having a full dynamic website for my simple little
corner of the web is overkill. Instead I use [jekyll](http://jekyllrb.com/) to
generate a static website from a pile of Markdown files and HTML templates. All
of this magic is hosted in a [separate
repository](https://github.com/rjw57/richwareham.com-static).

Why separate the repos like this? Well there is some non-trivial downtime
associated with pushing a new version of an OpenShift webapp. Previously I had
a lot of pre-build and build hook magic which would install jekyll, install
bower, build the static site, etc which was inappropriate for what is,
essentially, a very simple Python webapp.

By separating out the static content from the dynamic content I can configure
the webapp to simply serve any URL is doesn't know about from the static
directory. All very nice, clean and modular but how do I update the static
files on my website when I make a change?

I tend to subscribe to the "Unix laziness" philosophy which holds that spending
some time automating a solution will make things a lot easier in the long run.
The repo holding the static site content is monitored by a [corresponding
Travis-CI job](https://travis-ci.org/rjw57/richwareham.com-static). Travis CI
is very good at installing the various Node.js, Ruby and JavaScript
dependencies to build the site and so we should make use of its strengths.

So my problem is: I have a webapp serving static content from a directory on
the filesystem and I have Travis with a freshly built pile of HTML, CSS, etc.
How do I get the new content over to the webapp in a secure way? "Secure" here
means that anyone with read access to the webapp repository, static content
repository and Travis CI configuration file shouldn't be able to scribble all
over my website(!)

# Simple is better

I wanted a very simple way to deploy a new bundle of static content. Initially
I thought github releases would be the way forward. My plan was to make Travis
create a new release associated with the static content repo on each
successfully built commit to master. Unfortunately github is geared up to make
releases only when there's an associated tag. Having to tag each and every
commit seemed ugly and, as usual when things seem ugly, it's worth taking a
step back and thinking about the problem. A build of the static content isn't
really a "release" in the github sense; once it's deployed I don't need to keep
it around forever more.

After a bit more thought, I decided to make the deployment process a kind of
"fat webhook". When Travis built the static content, it would zip it up and
then HTTP POST that file to some URL. (In this case,
https://www.richwareham.com/static-content.) The Python webapp would take the
payload and unzip it into the static files area. Handily Python has a
[zipfile](https://docs.python.org/3/library/zipfile.html) module which can
handle zipped up data directly.

So far, so simple. We only need to write two functions. The first is a utility
function to take a destination directory, ensure it exists and to unzip the
contents of a file object to the directory:

```python
def update_static(destdir, fileobj):
    logging.info('Extracting new static site...')
    z = zipfile.ZipFile(fileobj, 'r')
    if not os.path.exists(destdir):
        os.makedirs(destdir)
    z.extractall(destdir)
```

The second is a flask handler for the URL:

```python
@app.route('/static-content', methods=['POST'])
def update_static_content():
    update_static(STATIC_SITE_DIR, request.files['archive'].stream)
    return 'OK'
```

All Travis now needed to do was to zip up the new static site content into a
file called, for example, ``site.zip`` and POST it to my website using
something like cURL:

```bash
$ curl -i -F "archive=@site.zip" https://www.richwareham.com/static-content
```

This works beautifully but it is massively insecure: **anyone can modify my
site's content**. To overwrite or create a file on my site an attacker need
only POST a zipfile to a URL which is plainly listed in the Tavis configuration
file.

# Shhh... It's a (shared) secret

[HMAC](https://en.wikipedia.org/wiki/Hash-based_message_authentication_code) or
"hash-based message authentication code" is a standard technique to compute a
token given a message and a secret value. Anyone in possession of the same
secret value can then verify that the message is authentic. (Or, at least, was
generated by someone who also knew the secret.)

In principle it's quite simple: the deploy script on Travis combines the zip
file and secret together and takes a hash. It then sends the zip file and
computed hash to the webapp. The webapp computes its own version of the hash
from the given zip file and its own copy of the shared secret. If the hashes
match then I know the person who sent me the zip file knows the shared secret.

HMAC itself is a little more subtle than this but fortunately there is a
[implementation](https://docs.python.org/3/library/hmac.html) in the Python
standard library. We're free to choose our own hash algorithm and so, as a good
default, I chose SHA256.

The complete Python code to compute a HMAC from an open file object is very small:

```python
import hashlib
import hmac
# ...
digest = hmac.new(shared_secret, file_obj.read(), hashlib.sha256)
token = digest.hexdigest() # hex-digit string containing HMAC
```

On the Travis side, this is wrapped up into a small
[calc_hmac.py](https://github.com/rjw57/richwareham.com-static/blob/master/scripts/calc_hmac.py)
script. On the webapp side we need only create a check function and modify our
request handler to use it:

```python
def check_hmac(fileobj, secret, provided_digest):
    # Compute expected digest
    digest = hmac.new(secret, fileobj.read(), hashlib.sha256)

    # Does this digest match? Use compare_digest() because it it constant time.
    # (Timing attacks are subtle. Crypto is hard :(.)
    return hmac.compare_digest(provided_digest, digest.hexdigest()):

@app.route('/static-content', methods=['POST'])
def update_static_content():
    # Get a file object pointing to the archive sent with the request
    archive = request.files['archive'].stream

    # Check the HMAC which was provided matches the shared secret
    archive.seek(0)
    hmac_ok = check_hmac(archive, SHARED_SECRET, request.values['hmac'])
    if not hmac_ok:
        return abort(403)

    # Unzip the static files
    archive.seek(0)
    update_static(STATIC_SITE_DIR, archive)
    return jsonify({ 'status': 200, 'message': 'OK' })
```

We're nearly there. All that's needed now is a way to get the shared secret to
Travis and the OpenShift webapp in a secure manner.

## Sharing the secret

Both OpenShift and Travis have the ability to securely store "secret"
information. Travis allows you to store [encrypted environment
variables](http://docs.travis-ci.com/user/encryption-keys/) and OpenShift
recently added [secure environment
variable](https://www.openshift.com/blogs/taking-advantage-of-environment-variables-in-openshift-php-apps)
support.

It's straightforward to arrange for both Travis and OpenShift to have the same
shared secret exposed via the ``STATIC_SITE_SECRET`` variable using a little
bit of bash:

```bash
$ SECRET=`dd if=/dev/urandom count=1024 | sha1sum`
$ cd $OPENSHIFT_APP   # cd to checkout of OpenShift app repo
$ rhc set-env STATIC_SITE_SECRET=$SECRET
$ cd $STATIC_SITE     # cd to checkout of static site repo
$ travis encrypt --add STATIC_SITE_SECRET=$SECRET
```

Note that this can be automated via a cron job and so the shared secret need
not stay constant. The Python webapp can now just use
``os.environ['STATIC_SITE_SECRET']`` for the shared secret.

# Summary

Above, I outlined the method I use for pushing new static site content to my
website without requiring a time-consuming re-deployment. The astute among you
will notice two potential problems which will need to be considered at a later
date:

* The static site contents are just unzipped atop the old ones and so it isn't
  possible to *delete* files.
* Because the zip file is just unzipped over the static files directory, the
  update isn't atomic. A better solution would be to unzip files to a temporary
  directory and use some symlink magic to update them atomically.

For my tiny website neither of these problems are major at the moment although
I may re-visit the solution at a later date.

Also, crypto is hard. Even though this HMAC based system is about a simple as
it can get, there may still be ways for a sufficiently motivated attacker to
push content to my website. I'm defending against the trivial "LOL his website
accepts any zip thrown at it"-style attacker, not someone willing to put real
effort into defacing my website :). That being said, if you *do* find some
obvious way to subvert this method, I'd be interested to hear it. I'm always
willing to learn more about crypto because if anyone claims they know it all,
they're lying or mad.
