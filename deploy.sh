#!/bin/bash

echo "Archiving site"
pushd _site
tar cvjf ../static.tar.bz2 .
popd

echo "TODO: deploy"
