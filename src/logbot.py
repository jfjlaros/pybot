# urlbot.py

from dhm import sqlwrap
import sqlbot

class LogBot(sqlbot.SQLBot):
	def __init__(self, *args, **kwargs):
		super(LogBot, self).__init__(*args, **kwargs)

		self.AddHandler("pubmsg", self._urlbot_log)
		self.logcmd=("INSERT INTO %s (url,nick,text) VALUES (?,?,?)" % 
				self.config["SQL/table"])


	def _urlbot_pubmsg(self, connection, event):
		nick=self.people[irclib.nm_to_n(event.source())]
		msg=event.arguments()[0]

		self.dbc.execute(self.logcmd, 
			(("http" in msg or "https" in msg or "ftp:" in msg),
			 nick, msg), "format")
		self.dbc.commit()

