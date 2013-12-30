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
from collections import defaultdict

##########################################################################
## Domain Analysis
##########################################################################

class DomainDistribution(object):
    """
    Statistical Distribution of Domain Names
    """

    def __init__(self, dataset):
        self.dataset = dataset

    def analyze(self):
        """
        Performs the analysis of the email domains
        """
        result = defaultdict(int)
        for row in self.dataset:
            domain = row[EMAIL].split('@')[1]
            result[domain] += 1
        return result

if __name__ == '__main__':

    from mailstat.reader import *
    from operator import itemgetter

    distro = DomainDistribution(M3Reader("fixtures/private-emailmetrics.csv"))
    result = distro.analyze()
    result = sorted(result.items(), key=itemgetter(1))

    for item in result:
        print "%s: %i" % item
