# tests.utils_tests.testgen_tests
# Tests for the Test Data Generation utility
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Dec 29 20:34:27 2013 -0600
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: testgen_tests.py [] benjamin@bengfort.com $

"""
Tests for the Test Data Generation utility
"""

##########################################################################
## Imports
##########################################################################

import os
import tempfile
import unittest

from mailstat.utils.testgen import *

##########################################################################
## TestCase
##########################################################################

class TestGenFunctionsTests(unittest.TestCase):

    def setUp(self):
        tdir = os.path.dirname(__file__)
        self.names_fixture   = os.path.join(tdir, "fixtures/names.txt")

    def test_list_from_file(self):
        """
        Check the helper function in testgen
        """
        alist = list(list_from_file(self.names_fixture))
        self.assertEqual(100, len(alist))

        # Ensure commented files aren't in the list
        for item in alist:
            self.assertFalse(item.startswith('#'))

class TestDataGeneratorTests(unittest.TestCase):

    def setUp(self):
        tdir = os.path.dirname(__file__)
        self.names_fixture   = os.path.join(tdir, "fixtures/names.txt")
        self.domains_fixture = os.path.join(tdir, "fixtures/domains.txt")
        self.orig_fixture    = os.path.join(tdir, "../fixtures/emailmetrics.csv")
        self.outpath = tempfile.mkstemp(suffix=".csv", prefix="email-")[1]

    def tearDown(self):
        if os.path.exists(self.outpath):
            os.remove(self.outpath)

    def test_names_fixture(self):
        """
        Check the names fixture exists
        """
        generator = TestDataGenerator(self.names_fixture, self.domains_fixture)
        self.assertGreater(len(generator.names), 0)

    def test_domains_fixture(self):
        """
        Check the domains fixture exists
        """
        generator = TestDataGenerator(self.names_fixture, self.domains_fixture)
        self.assertGreater(len(generator.domains), 0)

    def test_name_fields_helper(self):
        """
        Check the names field helper function
        """
        generator = TestDataGenerator(self.names_fixture, self.domains_fixture)
        testname = "Benjamin Bengfort"
        result   = generator.name_fields(testname)
        self.assertEqual(result[FIRST_NAME], 'Benjamin')
        self.assertEqual(result[LAST_NAME], 'Bengfort')
        self.assertEqual(result[DISPLAY_NAME], testname)
        self.assertEqual(result[MIDDLE_NAME], '')

        testname = "Benjamin John Bengfort"
        result   = generator.name_fields(testname)
        self.assertEqual(result[FIRST_NAME], 'Benjamin')
        self.assertEqual(result[LAST_NAME], 'Bengfort')
        self.assertEqual(result[DISPLAY_NAME], testname)
        self.assertEqual(result[MIDDLE_NAME], 'John')

    def test_email_from_name(self):
        """
        Check the email from name helper function
        """
        generator  = TestDataGenerator(self.names_fixture, self.domains_fixture)
        testname   = "Benjamin Bengfort"
        testdomain = "gmail.com"

        result     = generator.email_from_name(testname, testdomain)
        self.assertEqual(result, 'benjamin.bengfort@gmail.com')

    def test_write_with_anonymize(self):
        """
        Test the write function with a fixture (anonymize)
        """
        generator  = TestDataGenerator(self.names_fixture, self.domains_fixture, self.orig_fixture)
        generator.write(self.outpath)
        self.assertTrue(os.path.exists(self.outpath))

    def test_write_with_generate(self):
        """
        Test the write function without a fixture (generate)
        """
        generator  = TestDataGenerator(self.names_fixture, self.domains_fixture)
        generator.write(self.outpath)
        self.assertTrue(os.path.exists(self.outpath))
