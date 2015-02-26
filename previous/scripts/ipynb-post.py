"""IPython nbconvert configuration for importing IPython notebooks

Use: ipython nbconvert --config scripts/ipynb-post.py <FILE>

"""
# Originally from https://gist.github.com/cscorley/9144544

try:
    from urllib.parse import quote  # Py 3
except ImportError:
    from urllib2 import quote  # Py 2

import logging
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

c = get_config()
c.NbConvertApp.export_format = 'markdown'
c.MarkdownExporter.template_path = [os.path.dirname(__file__)]
c.MarkdownExporter.template_file = 'ipynb-post.tpl'

def path2support(path):
    """Turn a file path into a URL"""
    parts = path.split(os.path.sep)
    return '{{ site.baseurl}}/images/' + '/'.join(quote(part) for part in parts)

c.MarkdownExporter.filters = { 'path2support': path2support }
