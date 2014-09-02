#!/bin/bash

if [ -z "$STATIC_SITE_SECRET" ]; then
  echo "ERROR: static site secret is not set" >&2
  exit 1
fi

echo "Archiving site"
pushd _site
tar cvjf ../static.tar.bz2 .
popd

echo "TODO: deploy"
