# tests.reporting_tests.base_tests
# Test cases for the base Report class
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Dec 29 22:24:42 2013 -0600
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Test cases for the base Report class
"""

##########################################################################
## Imports
##########################################################################

import os
import unittest
import tempfile

from jinja2 import Environment
from mailstat.reporting.base import *
from mailstat.exceptions import *

##########################################################################
## TestCase
##########################################################################

class ReportTests(unittest.TestCase):
    """
    Tests the base report class
    """

    def setUp(self):
        self.outpath = tempfile.mkstemp(suffix=".html")[1]

    def tearDown(self):
        if os.path.exists(self.outpath):
            os.remove(self.outpath)

    def test_arbitrary_values(self):
        """
        Check that values can be set on the Report
        """
        report = Report(foo="bar")
        self.assertTrue(hasattr(report, 'foo'))
        self.assertEqual(report.foo, 'bar')

    def test_jinja_environment(self):
        """
        Check that the Jinja2 Environment can be fetched
        """
        report = Report()
        self.assertTrue(isinstance(report.environment, Environment))

    def test_improperly_configured(self):
        """
        Check to ensure that a blank template errors
        """
        with self.assertRaises(ImproperlyConfigured):
            report   = Report()
            template = report.get_template()

    def test_base_template(self):
        """
        Assert a base template exists and is fetchable
        """
        report = Report(template_name='base.html')
        template = report.get_template()
        self.assertTrue(template)

    def test_render_to_file(self):
        """
        Check that we can render a base template
        """
        report = Report(template_name='base.html')
        report.render(self.outpath, title="test report")
        self.assertTrue(os.path.exists(self.outpath))

        with open(self.outpath, 'r') as data:
            self.assertIn('test report', data.read())

    def test_get_context_data(self):
        """
        Assert a report class is in the context
        """
        report  = Report()
        context = report.get_context_data(foo='bar')
        self.assertIn('foo', context)
        self.assertEqual(context['foo'], 'bar')
        self.assertIn('report', context)
        self.assertEqual(context['report'], report)

