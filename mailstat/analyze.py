# mailstat.analyze
# Analysis module for the email analysis project
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Dec 29 23:45:58 2013 -0600
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Analysis module for the email analysis project
"""

##########################################################################
## Imports
##########################################################################

from copy import deepcopy
from mailstat.metric import *
from mailstat.reader import *
from mailstat.exceptions import *

##########################################################################
## Module Constants
##########################################################################

METRICS = [DomainDistribution,]

##########################################################################
## Analysis Harness
##########################################################################

class Analysis(object):
    """
    The analysis and data processing harness
    """

    def __init__(self, csvfile, **kwargs):
        self.csvfile = csvfile
        self.metrics = kwargs.get('metrics', METRICS)

    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        self._metrics = []
        for metric in metrics:
            self._metrics.append(metric())

    @property
    def dataset(self):
        if not hasattr(self, '_dataset'):
            self._dataset = M3Reader(self.csvfile)
        return self._dataset

    def before_analysis(self):
        for metric in self.metrics:
            metric.preprocess()

    def after_analysis(self):
        for metric in self.metrics:
            metric.postprocess()

    def analyze(self):
        self.before_analysis()
        for row in self.dataset:
            for metric in self.metrics:
                metric.process(deepcopy(row))
        self.after_analysis()

    def serialize(self):
        """
        TODO: Check analysis state
        """
        return dict((m.get_name(), m.get_value()) for m in self.metrics)
