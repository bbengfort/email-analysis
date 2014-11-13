# mailstat.metric.counts
# Performs counting statistics of emails.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  timestamp
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: counts.py [] benjamin@bengfort.com $

"""
Performs counting statistics of emails.
"""

##########################################################################
## Imports
##########################################################################

from mailstat.metric import Metric

##########################################################################
## Metrics
##########################################################################

class MostFrequentCorrespondents(Metric):
    """
    Determines the top 10 most frequent communicators
    """
    pass
