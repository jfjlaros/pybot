# sqlbot.py

import dhm.config, dhm.nestdict
import ircbot

class ConfigBot(ircbot.IrcBot):
	def __init__(self, *args, **kwargs):
		super(ConfigBot, self).__init__(*args, **kwargs)

		self.config=dhm.nestdict.NestedDict(kwargs["config"])

