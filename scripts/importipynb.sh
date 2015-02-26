#!/bin/bash
#
# Simple script to import an IPython notebook into the site

# Find which directory this script is in
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ $# -ne 1 ]; then
  echo "syntax: $0 <FILE>"
  exit 1
fi

ipynb_path=`readlink -m "$1"`; shift
echo "Importing '$ipynb_path' into project"

# Make a temporary directory to build results in
TMPFILE=`mktemp -t -d importipynb.XXXXXX`
trap "echo Deleting '$TMPFILE'; rm -rf '$TMPFILE'" EXIT

cd $TMPFILE

echo "Converting post..."
ipython nbconvert --config "$DIR/ipynb-post.py" "$ipynb_path" || exit 1

echo "Copying post files and markdown"
md_output=`basename "$ipynb_path" .ipynb`.md
files_dir=`basename "$ipynb_path" .ipynb`_files
if [ -f "$md_output" ]; then
  mkdir -p "$DIR/../_posts"
  cp -v "$md_output" "$DIR/../_posts"
fi
if [ -d "$files_dir" ]; then
  mkdir -p "$DIR/../images"
  cp -vr "$files_dir" "$DIR/../images"
fi

if [ -f "$ipynb_path" ]; then
  echo "Copying original notebook"
  mkdir -p "$DIR/../downloads"
  cp -v "$ipynb_path" "$DIR/../downloads"
fi

echo "Done"

