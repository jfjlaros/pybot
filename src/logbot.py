# urlbot.py

import re
import irclib, sqlbot

class LogBot(sqlbot.SQLBot):
	urlmatcher      = re.compile(
		r"\b(?P<url>(?P<scheme>http|https|ftp)://"
		r"(?:(?P<login>(?P<username>[a-zA-Z0-9]+)(?::(?P<password>[A-Za-z0-9]+))?)@)?"
		r"(?P<hostname>[A-Za-z0-9.-]+(?::(?P<port>[0-9]+))?)"
		r"(?P<path>[A-Za-z0-9@~=?/.&;#+-]*))")

	def __init__(self, *args, **kwargs):
		super(LogBot, self).__init__(*args, **kwargs)

		self.AddHandler("pubmsg", self._urlbot_pubmsg)
		self.logcmd=("INSERT INTO %s (url,nick,text) VALUES (%%s,%%s,%%s)" % 
				self.config["SQL/table"])


	def hasurl(self, text):
		return self.urlmatcher.match(text)!=None


	def _urlbot_pubmsg(self, connection, event):
		nick=irclib.nm_to_n(event.source())
		msg=event.arguments()[0]

		try:
			self.sqlverify()
			url=self.hasurl(msg)

			self.dbc.execute(self.logcmd, (url,nick,msg), "format")
			self.dbc.commit()
		except self.dbc.Error, e:
			self.logger.error("Failed to log message: %s" % e)

