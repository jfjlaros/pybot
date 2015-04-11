# __init__.py
#
# Copyright 2003,2004 Wichert Akkerman <wichert@wiggy.net>

__version_info__ = ('0', '0', '1')


__version__ = '.'.join(__version_info__)
__docformat__ = "epytext en"
__author__ = "Wichert Akkerman"
__contact__ = "wichert@wiggy.net"
__copyright__ = "Copyright 2003,2004 Wichert Akkerman"
__homepage__ = 'git://fixedpoint.nl/pybot.git'

__all__ = ["commandbot", "ircbot", "irclib", "logbot", "nicktrack", "sqlbot",
    "tbf", "votebot"]
