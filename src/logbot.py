# logbot.py

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

		self.AddHandler("pubmsg", self._logbot_pubmsg)
		self.AddHandler("ctcp", self._logbot_ctcp)
		self.AddHandler("topic", self._logbot_topic)
		self.logcmd=("INSERT INTO %s (url,type,nick,text) VALUES (%%s,%%s,%%s,%%s)" % 
				self.config["SQL/table"])


	def hasurl(self, text):
		return self.urlmatcher.search(text)!=None


	def _logbot_log(self, type, nick, msg):
		try:
			self.sqlverify()
			url=self.hasurl(msg)

			self.dbc.execute(self.logcmd, (url,type,nick,msg), "format")
			self.dbc.commit()
		except self.dbc.Error, e:
			self.logger.error("Failed to log message: %s" % e)


	def _logbot_ctcp(self, connection, event):
		if not event.arguments()[0]=="ACTION":
			return
		nick=irclib.nm_to_n(event.source())
		msg=event.arguments()[1]
		self._logbot_log("ACTION", nick, msg)


	def _logbot_pubmsg(self, connection, event):
		nick=irclib.nm_to_n(event.source())
		msg=event.arguments()[0]
		self._logbot_log("PUBMSG", nick, msg)

	def _logbot_topic(self, connection, event):
		nick=irclib.nm_to_n(event.source())
		msg=event.arguments()[0]
		self._logbot_log("TOPIC", nick, msg)
