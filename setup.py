#!/usr/bin/python

from distutils.core import setup

setup(	name		= "pybot",
	version		= "0.1",
	author		= "Wichert Akkerman",
	author_email	= "wichert@wiggy.net",
	license		= "BSD",
	description	= "IRC bot basics",
	packages	= [ "pybot" ],
	package_dir	= { "pybot" : "src" },
	keywords	= [ "IRC", "bot" ],
	)
