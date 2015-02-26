#!/bin/bash
#
# Simple script to install build dependencies for website.

# Flags for npm. Add "-g" here if you don't mind polluting a semi-global
# namespace.
NPM_INSTALL_FLAGS=""

# Flags for gem
GEM_INSTALL_FLAGS="--user"

# Find npm
NPM=$(which npm)
if [ -z "$NPM" ]; then
	echo "could not find npm" >&2
	exit 1
fi

# Find npm
GEM=$(which gem)
if [ -z "$GEM" ]; then
	echo "could not find gem" >&2
	exit 1
fi

# Install npm packahes
for pkgname in less less-plugin-clean-css uglify; do
	echo "Installing ${pkgname}..."
	${NPM} install ${NPM_INSTALL_FLAGS} "${pkgname}"
done

# Install gem packages
for pkgname in jekyll; do
	echo "Installing ${pkgname}..."
	${GEM} install ${GEM_INSTALL_FLAGS} "${pkgname}"
done

