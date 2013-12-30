# mailstat.metric.base
# The base metric class for all metrics
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Dec 29 23:01:26 2013 -0600
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
The base metric class for all metrics
"""

##########################################################################
## Imports
##########################################################################

import abc

from mailstat.exceptions import *

##########################################################################
## Base Metric
##########################################################################

class Metric(object):
    """
    A Metric is a single unit of computation that can be used for analysis.
    For instance, a metric can compute a timeseries, a minimum or maximum
    value, average values, or even a collection of these values. The
    metric's data is then accessible by the reporting module.
    """

    __metaclass__ = abc.ABCMeta

    name = None

    def preprocess(self):
        """
        This hook will be called before a dataset is processed.
        """
        return False

    @abc.abstractmethod
    def process(self, row):
        """
        Every metric will have access to a copy of every single row in the
        dataset to perform it's analytics upon. The metric should store
        its data on the instance and compute for each row accordingly.
        """
        raise NotImplementedError("Metrics must proccess rows.")

    def postprocess(self):
        """
        This hook will be called after a dataset is completely processed.
        """
        return False

    @abc.abstractmethod
    def get_value(self):
        raise NotImplementedError("Metrics must report a value.")

    def get_name(self):
        if not self.name:
            raise ImproperlyConfigured("Metrics must provide a name or implementation of get_name()")
        return self.name

