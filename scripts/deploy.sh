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
tar cvjf ../static.tar.bz2 .
popd

echo "Calculating HMAC"
HMAC=`scripts/calc_hmac.py static.tar.bz2`
echo "HMAC computed as $HMAC"

echo "Pushing payload to $DEPLOY_URL"
curl -i -F "hmac=$HMAC" -F "archive=@static.tar.bz2" "$DEPLOY_URL"

