# tests.reader_tests
# Testing the M3Reader package for mailstat
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Dec 29 19:30:05 2013 -0600
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: reader_tests.py [] benjamin@bengfort.com $

"""
Testing the M3Reader package for mailstat
"""

##########################################################################
## Imports
##########################################################################

import os
import unittest
import random

from mailstat.reader import *
from mailstat.exceptions import *
from datetime import datetime

##########################################################################
## TestCase
##########################################################################

class ReaderTests(unittest.TestCase):

    def setUp(self):
        self.fixture = "fixtures/emailmetrics.csv"

    def test_bad_path(self):
        """
        Assert the reader checks the path at runtime
        """
        with self.assertRaises(ReaderException):
            reader = M3Reader("/path/to/bad/file.csv")

    def test_munge(self):
        """
        Test the reader munge functionality
        """
        testdata = ('perla.deland@yahoo.com','Perla Deland','Perla','',
                    'Deland','','','','','11','12/25/2011 02:29:44 PM',
                    '1/16/2013 04:20:16 PM')
        testrow  = dict(zip(FIELDS, testdata))
        reader   = M3Reader(self.fixture)
        munged   = reader.munge(testrow)

        self.assertTrue(isinstance(munged[FIRST_SEEN], datetime))
        self.assertTrue(isinstance(munged[LAST_SEEN], datetime))
        self.assertTrue(isinstance(munged[COUNT], int))

    def test_iter(self):
        """
        Assert the reader can read rows
        """
        reader   = M3Reader(self.fixture)
        for row in reader:
            self.assertTrue(isinstance(row, dict), "DictReader must be used")
            self.assertTrue(isinstance(row[COUNT], int), "Row not munged")

            testkey = random.choice(row.keys()) # Test random key
            self.assertIn(testkey, FIELDS, "%s not in expected FIELDS" % testkey)

    def test_len(self):
        """
        Check that the reader can compute the number of rows
        """
        reader   = M3Reader(self.fixture)
        self.assertFalse(hasattr(reader, '_lines'), "Pre-iter property set?")
        self.assertEqual(1430, len(reader), "Length doesn't match.")
        self.assertTrue(hasattr(reader, '_lines'), "Post-iter property set?")
