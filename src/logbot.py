# urlbot.py

from dhm import sqlwrap
import basicbot

class LogBot(basicbot.BasicBot):
	def __init__(self, *args, **kwargs):
		super(LogBot, self).__init__(*args, **kwargs)
		server=self.GetServer(self.config["SQL/driver"],
				host=cfg["SQL/server"],
				user=cfg["SQL/username"],
				password=cfg["SQL/password"])
		self.dbc=server[self.config["SQL/database"]]


	def OnPubMsg(self, connection, event):
		super(LogBot, self).OnPubMsg(connection, event)

