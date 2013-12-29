# tests
# Tests for the mailstat package
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Dec 29 15:07:45 2013 -0600
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Tests for the mailstat package
"""

##########################################################################
## Imports
##########################################################################

from unittest import TestCase

##########################################################################
## TestCase
##########################################################################

class InitialTests(TestCase):
    """
    Initial tests cases for mailstat package
    """

    def sanity_test(self):
        """
        Assert a world fact, 2+3=5
        """
        self.assertEqual(2+3, 5)

    def import_test(self):
        """
        Assert that we're able to import mailstat
        """
        try:
            import mailstat
        except ImportError:
            self.fail("Unable to import mailstat package")
