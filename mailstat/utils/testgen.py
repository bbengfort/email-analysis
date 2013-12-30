# mailstat.utils.testgen
# Generates Test Data from a Fixture for MailStat
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Dec 29 17:28:46 2013 -0600
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: testgen.py [] benjamin@bengfort.com $

"""
Generates Test Data from a Fixture for MailStat

If you don't have the luxury of getting to use MineMyMail, you can create
a fake data set using this method here. It requires a list of names and a
list of domains. I got the list of names from:

    http://listofrandomnames.com/

Optionally, you can also anonymize a fixture that you recieved via the
MineMyMail service. This is useful for publishing reports and protecting
private data.
"""

##########################################################################
## Imports
##########################################################################

import os
import sys
import random

from copy import copy
import unicodecsv as csv
from mailstat.reader import *
from datetime import datetime
from dateutil.relativedelta import relativedelta

##########################################################################
## Helper Functions
##########################################################################

def list_from_file(path):
    """
    Reads a newline delimited list from a file and returns an iterable.
    """
    with open(path, 'rU') as data:
        for line in data:
            line = line.decode('utf8')
            line = line.strip()
            if line and not line.startswith('#'):
                yield line

##########################################################################
## Random Generator
##########################################################################

class TestDataGenerator(object):
    """
    Generates random test data for this module.
    """

    def __init__(self, names, domains, fixture=None, **kwargs):
        """
        :param names: A newline delimited file of names (or iterable)
        :param domains: A newline delimited file of domains (or iterable)
        :param fixture: A fixture to anonymize
        """
        self.names    = names
        self.domains  = domains
        self.fixture  = fixture

        self.encoding = kwargs.get('encoding', ENCODING)
        self.datefmt  = kwargs.get('datefmt', '%m/%d/%Y %H:%M:%S %p')

    ##////////////////////////////////////////////////////////////////////
    ## Class Properties
    ##////////////////////////////////////////////////////////////////////

    @property
    def names(self):
        """
        Getter for in-memory names data structure
        """
        return self._names

    @names.setter
    def names(self, names):
        """
        If names is a string, it treats it as a path and reads the names
        from the file (creating an in-memory list). Otherwises, saves list.
        """
        if isinstance(names, str):
            names = list(list_from_file(names))
        self._names = names

    @property
    def domains(self):
        """
        Getter for in-memory domains data structure
        """
        return self._domains

    @domains.setter
    def domains(self, domains):
        """
        If names is a string, it treats it as a path and reads the domains
        from the file (creating an in-memory list). Otherwises, saves list.
        """
        if isinstance(domains, str):
            domains = list(list_from_file(domains))
        self._domains = domains

    ##////////////////////////////////////////////////////////////////////
    ## API Functions
    ##////////////////////////////////////////////////////////////////////

    def write(self, outpath=None):
        """
        The method that selects appropriate execution path from options,
        and if an output is supplied, it will write to that outpath, else
        to stdout rather than the outpath.

        :param outpath: The path to write the data, else to stdout
        """

        # Open outpath or write to stdout
        outfile = open(outpath, 'w') if outpath else sys.stdout

        # Select method based on fixture
        method = self.anonymize if self.fixture else self.generate
        writer = csv.DictWriter(outfile, fieldnames=FIELDS, encoding=self.encoding)

        # Write the file
        writer.writeheader()
        for row in method():
            writer.writerow(row)

        # Clean up file descriptor if not stdout.
        if outpath: outfile.close()

    def generate(self):
        """
        Generates completely random data from the domains and names.

        Note: Currently the regional data is not supported as generated.
        """

        # Create as many rows as there are names
        for name in self.names:
            # Initialize empty row
            row = dict(map(lambda f: (f, ''), FIELDS))

            # Create the parts of the Name
            row.update(self.name_fields(name))

            # Choose a random email count
            row[COUNT] = random.randint(1, 600)

            # Create a random email from the name and random domain
            row[EMAIL] = self.email_from_name(name)

            # Create a random time delta
            year       = random.choice(xrange(2000, 2013))
            month      = random.choice(xrange(1, 12))
            day        = random.choice(xrange(1, 28))
            hour       = random.choice(xrange(0, 23))
            minute     = random.choice(xrange(0, 59))
            first_seen = datetime(year, month, day, hour, minute)
            timedelta  = datetime.now() - first_seen
            seconds    = int(timedelta.total_seconds())
            last_seen  = first_seen + relativedelta(seconds=random.choice(xrange(0, seconds)))

            row[FIRST_SEEN] = first_seen.strftime(self.datefmt)
            row[LAST_SEEN]  = last_seen.strftime(self.datefmt)

            yield row

    def anonymize(self):
        """
        Anonymizes a fixture with random names selected only from the list
        of acceptable domains.

        Note: Currently the regional data is not supported as generated.
        """
        reader = M3Reader(self.fixture)
        for row in reader:
            domain = row[EMAIL].split('@')[1]
            if domain in self.domains:
                # Anonymize the name fields
                name = random.choice(self.names)
                row.update(self.name_fields(name))

                # Anonymize the email field
                row[EMAIL] = self.email_from_name(name)

                # Stringify the datetimes
                row[FIRST_SEEN] = row[FIRST_SEEN].strftime(self.datefmt) if row[FIRST_SEEN] else ''
                row[LAST_SEEN]  = row[LAST_SEEN].strftime(self.datefmt) if row[LAST_SEEN] else ''

                yield row

    ##////////////////////////////////////////////////////////////////////
    ## Helper Functions
    ##////////////////////////////////////////////////////////////////////

    def name_fields(self, name):
        """
        Returns a Dictionary containing expected name fields.

        :param name: The display name to parse into fields
        """
        parts = name.split()
        first = parts[0]
        if len(parts) > 2:
            middle = parts[1]
            last   = ' '.join(parts[2:])
        else:
            middle = ''
            last   = ' '.join(parts[1:])
        return {
            DISPLAY_NAME: name,
            FIRST_NAME: first,
            MIDDLE_NAME: middle,
            LAST_NAME: last,
        }

    def email_from_name(self, name, domain=None):
        """
        Creates an email address from a name, if a domain is provided it
        uses that domain, otherwise it uses a random domain from the list
        of domains built in.

        :param name: The display name of the user to create an email for
        :param domain: Optional domain to use to create email.
        """
        domain = domain or random.choice(self.domains)
        ename  = ".".join([p.lower() for p in name.split()])
        return "@".join((ename, domain))

##########################################################################
## Main Method
##########################################################################

if __name__ == '__main__':
    generator = TestDataGenerator("fixtures/names.txt",
                                  "fixtures/domains.txt",
                                  "fixtures/private-emailmetrics.csv")
    generator.write()
