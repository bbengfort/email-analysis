# mailstat.reporting.base
# Code for the creation of Reports
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Dec 29 21:45:46 2013 -0600
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: base.py [] benjamin@bengfort.com $

"""
Code for the creation of Reports
"""

##########################################################################
## Imports
##########################################################################

import six

from jinja2 import Environment, PackageLoader
from mailstat.exceptions import ImproperlyConfigured

##########################################################################
## Report Object
##########################################################################

class Report(object):
    """
    Base class that wraps the templating language in a Django-like way.
    """

    template_name = None

    def __init__(self, **kwargs):
        """
        Constructor. Per-instance override of class based configuration.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    @property
    def environment(self):
        """
        The Jinja2 Environment and Template Loader
        """
        if not hasattr(self, '_environment'):
            loader=PackageLoader('mailstat.reporting', 'templates')
            self._environment = Environment(loader=loader)
        return self._environment

    def render(self, path, **kwargs):
        """
        Renders the report with the template and the context data to the
        output file that is computed from the output_path variable.
        """
        context  = self.get_context_data(**kwargs)
        template = self.get_template()
        template.stream(context).dump(path)

    def get_template(self):
        """
        Uses Jinja2 to fetch the template from the Environment
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "Report requires either a definition of "
                "'template_name' or an implementation of 'get_template()'")
        return self.environment.get_template(self.template_name)

    def get_context_data(self, **kwargs):
        """
        Construct context data on a per report basis to render the report.
        """
        if 'report' not in kwargs:
            kwargs['report'] = self
        return kwargs

if __name__ == '__main__':
    report = Report(template_name="base.html")
    report.render("report.html", title="Test Report")
