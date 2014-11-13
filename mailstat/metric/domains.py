# mailstat.domains
# Analyzes the domains of the mail data
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  timestamp
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: domains.py [] benjamin@bengfort.com $

"""
Analyzes the domains of the mail data
"""

##########################################################################
## Imports
##########################################################################

from mailstat.reader import EMAIL
from mailstat.metric import Metric
from collections import defaultdict

##########################################################################
## Domain Analysis
##########################################################################

class DomainDistribution(Metric):
    """
    Statistical distribution of email domains
    """

    name = "Domain Distribution"

    def preprocess(self):
        """
        Instantiate the data store for domain counting
        """
        self.data = defaultdict(int)

    def process(self, row):
        """
        Increments the frequency distribution for email domains
        """
        domain = row[EMAIL].split('@')[1]
        self.data[domain] += 1

    def get_value(self):
        return self.data
