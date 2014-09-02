#!/bin/bash

echo "Checking static site secret is set"
if [ -z "$STATIC_SITE_SECRET" ]; then
  echo "ERROR: static site secret is not set" >&2
  exit 1
fi

echo "Archiving site"
pushd _site
tar cvjf ../static.tar.bz2 .
popd

echo "Calculating HMAC"
HMAC=`scripts/calc_hmac.py static.tar.bz2`
echo "HMAC computed as $HMAC"

echo "Pushing payload"
curl -i -F "hmac=$HMAC" -F "archive=@static.tar.bz2" https://www.richwareham.com/static-content

