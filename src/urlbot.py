# urlbot.py

from dhm import sqlwrap
import sqlbot

class URLBot(sqlbot.SQLBot):
	def __init__(self, *args, **kwargs):
		super(URLBot, self).__init__(*args, **kwargs)

		self.add_global_handler("pubmsg", self._urlbot_log)


	def _urlbot_pubmsg(self, connection, event):
		nick=self.people[irclib.nm_to_n(event.source())]
		msg=event.arguments()[0]

		if msg.find("http:")!=-1 or msg.find("ftp:")!=-1:
			pass

