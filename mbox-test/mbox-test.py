# mbox.reader
# Wraps Python's mailbox library to read MBox formated files
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Jan 15 15:56:43 2014 -0500
#
# Copyright (C) 2014 Tipsy Bear Studios
# For license information, see LICENSE.txt
#
# ID: mbox-test.py [] benjamin@bengfort.com $

"""
Wraps Python's mailbox library to read MBox formated files
"""

##########################################################################
## Imports
##########################################################################

import re
import os

from mailbox import mbox
from datetime import datetime
from collections import defaultdict

##########################################################################
## Module Constants
##########################################################################

FROM_REGEX = re.compile(r'^(\d+)@(\w+)\s(.+)$', re.I)
FROM_DTFMT = "%a %b %d %H:%M:%S %Y"

##########################################################################
## MBox Reader
##########################################################################

class MBoxReader(object):

    def __init__(self, path):
        self.path = path
        self.mbox = mbox(path)

        # Hidden Properties
        self._begin = None
        self._finit = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        path = os.path.abspath(path)

        if not os.path.isfile(path):
            raise Exception("Invalid file at '%s'" % path)
        self._path = path

    @property
    def read_time(self):
        if self._begin is None or self._finit is None:
            return None
        return self._finit - self._begin

    def from_lines(self):
        for msg in self:
            line = msg.get_from().strip()
            if line: yield line

    def __iter__(self):
        self._begin = datetime.now()
        for msg in self.mbox:
            yield msg
        self._finit = datetime.now()

class GmailMBoxReader(MBoxReader):

    def date_extraction(self):
        """
        Extracts dates from the from line.
        """
        errors = 0
        for idx, line in enumerate(self.from_lines()):
            if errors > 100: break
            match = FROM_REGEX.match(line)
            if not match:
                print "No match on line %i: '%s'" % (idx, line)
                errors += 1
                continue

            try:
                yield datetime.strptime(match.groups()[2], FROM_DTFMT)
            except ValueError:
                print "Could not extract date on line %i: '%s'" % (idx, line)
                errors += 1
                continue

##########################################################################
## Testing
##########################################################################

if __name__ == '__main__':
    import time
    import json

    reader = GmailMBoxReader('benjamin@bengfort.com.mbox')
    dates  = defaultdict(int)
    for date in reader.date_extraction():
        dates[time.mktime(date.date().timetuple())] += 1

    print reader.read_time
    print json.dumps(dates)
