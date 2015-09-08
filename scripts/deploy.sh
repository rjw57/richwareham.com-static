#!/bin/bash

echo "Checking static site secret is set"
if [ -z "$STATIC_SITE_SECRET" ]; then
  echo "ERROR: static site secret is not set" >&2
  exit 1
fi

if [ ! -d "_site" ]; then
  echo "Static site output directory not present" >&2
  exit 1
fi

if [ -z "$DEPLOY_URL" ]; then
  DEPLOY_URL="https://www.richwareham.com/static-content"
fi
echo "Will deploy to $DEPLOY_URL"

echo "Archiving site"
pushd _site
zip -r ../static.zip .
popd

echo "Calculating HMAC"
HMAC=`scripts/calc_hmac.py static.zip`
echo "HMAC computed as $HMAC"

echo "Pushing payload to $DEPLOY_URL"
# NOTE: the --insecure option is here since the Travis build machines don't have
# the startssl CA in the default list of certificates. It's OK to be insecure
# here since a) I don't need to trust the identity of the upload server since b)
# the authentication is that I have valid static content.
curl --insecure -i -F "hmac=$HMAC" -F "archive=@static.zip" "$DEPLOY_URL"

