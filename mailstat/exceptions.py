# mailstat.exceptions
# Exceptions hierarchy for mailstat package
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Dec 29 16:12:46 2013 -0600
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: exceptions.py [] benjamin@bengfort.com $

"""
Exceptions hierarchy for mailstat package
"""

##########################################################################
## Exceptions
##########################################################################

class MailstatException(Exception):
    """
    Base exception for mailstat
    """
    pass

class ReaderException(MailstatException):
    """
    Problems with mailstat reader
    """
    pass

class ConsoleError(MailstatException):
    """
    Something went wrong during the execution from the command line
    """
    pass
