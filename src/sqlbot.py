# sqlbot.py

import dhm.sqlwrap
import ircbot

class SQLBot(ircbot.IrcBot):
	def __init__(self, *args, **kwargs):
		super(SQLBot, self).__init__(*args, **kwargs)

		self.sqlserver=dhm.sqlwrap.GetServer(self.config["SQL/driver"],
				host=cfg["SQL/server"],
				user=cfg["SQL/username"],
				password=cfg["SQL/password"])
		self.dbc=server[self.config["SQL/database"]]
