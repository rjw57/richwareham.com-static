#!/usr/bin/env python
"""
Usage:
    calc_hmac.py <file>

The environment variable STATIC_SITE_SECRET must be set to a secret shared with
the destination site.
"""

import hashlib
import hmac
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
log = logging.getLogger()

def main():
    if len(sys.argv) != 2 or 'STATIC_SITE_SECRET' not in os.environ:
        sys.stderr.write(__doc__)
        sys.exit(1)

    _, filename = sys.argv

    log.info('Calculating HMAC of {0}'.format(filename))
    file_contents = open(filename, 'rb').read()

    auth_token = hmac.new(
            os.environ['STATIC_SITE_SECRET'].encode('utf8'),
            file_contents, hashlib.sha256)

    sys.stdout.write(auth_token.hexdigest())

if __name__ == '__main__':
    main()
