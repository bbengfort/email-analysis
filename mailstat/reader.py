# mailstat.reader
# Wraps the data reading and munging functionality
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Dec 29 16:05:08 2013 -0600
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: reader.py [] benjamin@bengfort.com $

"""
Wraps the data reading and munging functionality
"""

##########################################################################
## Imports
##########################################################################

import os
import re

import unicodecsv as csv
from datetime import datetime
from mailstat.exceptions import *

##########################################################################
## Expected Fields
##########################################################################

EMAIL        = "Email Address"
DISPLAY_NAME = "Display Name"
FIRST_NAME   = "First Name"
MIDDLE_NAME  = "Middle Name"
LAST_NAME    = "Last Name"
CITY         = "City"
REGION       = "Region"
COUNTRY      = "Country"
FACEBOOK     = "Facebook Link"
COUNT        = "Count"
FIRST_SEEN   = "First Seen"
LAST_SEEN    = "Last Seen"

FIELDS       = (
    EMAIL, DISPLAY_NAME, FIRST_NAME, MIDDLE_NAME,
    LAST_NAME, CITY, REGION, COUNTRY, FACEBOOK,
    COUNT, FIRST_SEEN, LAST_SEEN,
)

ENCODING     = 'ISO8859'

##########################################################################
## Reader Class
##########################################################################

class M3Reader(object):
    """
    Iterable that munges and validates MineMyMail CSV Data
    """

    def __init__(self, path, **kwargs):
        """
        Construct an M3Reader for a particular path.

        Optional Keyword Arguments:
            encoding: encoding of file (default ISO8859)
            datefmt:  format of datetimes
        """
        self.path = path

        self.encoding = kwargs.get('encoding', ENCODING)
        self.datefmt  = kwargs.get('datefmt', '%m/%d/%Y %H:%M:%S %p')

    @property
    def path(self):
        """
        Getter for internal `_path` property
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        Setter for internal `_path` property - expands path string and
        checks to ensure that a file exists at the path before setting.
        """
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        path = os.path.abspath(path)

        if not os.path.exists(path) or not os.path.isfile(path):
            raise ReaderException("No CSV file found at '%s'" % path)

        self._path = path

    def munge(self, row):
        """
        Converts the data in the row to Python types.

        Responds to conversions with built in converter lambdas as defined
        on a per-key basis. This method can be overriden in subclasses.
        """

        converters = (
            (FIRST_SEEN, lambda x: datetime.strptime(x, self.datefmt)),
            (LAST_SEEN,  lambda x: datetime.strptime(x, self.datefmt)),
            (COUNT,      lambda x: int(x)),
        )

        for key, func in converters:
            # TODO: Remove and raise exception on validation error
            if row[key]:
                row[key] = func(row[key])

        return row

    def __iter__(self):
        """
        Iterable for rows in CSV file, also counts rows for len.
        """
        with open(self.path, 'rU') as data:
            reader = csv.DictReader(data, encoding=self.encoding)
            self._lines = 0
            for row in reader:
                self._lines += 1
                yield self.munge(row)

    def __len__(self):
        """
        If iteration has alreadyrun, returns the number of lines, else will
        iterate through the CSV file to determine its length.
        """
        if not hasattr(self, '_lines'):
            for row in self: continue
        return self._lines

    def __str__(self):
        return "<M3Reader (%i rows) at '%s'>" % (len(self), self.path)

if __name__ == '__main__':
    reader = M3Reader("tests/fixtures/emailmetrics.csv")
    print reader
    for row in reader:
        for item in row.items():
            print "%s: %s" % item
        break
