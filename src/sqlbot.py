# sqlbot.py

import dhm.sqlwrap
import configbot

class SQLBot(configbot.ConfigBot):
	def __init__(self, *args, **kwargs):
		super(SQLbot, self).__init__(*args, **kwargs)

		self.sqlserver=dhm.sqlwrap.GetServer(self.config["SQL/driver"],
				host=cfg["SQL/server"],
				user=cfg["SQL/username"],
				password=cfg["SQL/password"])
		self.dbc=server[self.config["SQL/database"]]
