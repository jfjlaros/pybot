# urlbot.py

from dhm import sqlwrap
import irclib, sqlbot

class LogBot(sqlbot.SQLBot):
	def __init__(self, *args, **kwargs):
		super(LogBot, self).__init__(*args, **kwargs)

		self.AddHandler("pubmsg", self._urlbot_pubmsg)
		self.logcmd=("INSERT INTO %s (url,nick,text) VALUES (%%s,%%s,%%s)" % 
				self.config["SQL/table"])


	def _urlbot_pubmsg(self, connection, event):
		nick=irclib.nm_to_n(event.source())
		msg=event.arguments()[0]

		try:
			self.sqlverify()
			self.dbc.execute(self.logcmd, 
				(("http" in msg or "https" in msg or "ftp:" in msg),
				 nick, msg), "format")
			self.dbc.commit()
		except self.dbc.Error, e:
			self.logger.error("Failed to log message: %s" % e)

