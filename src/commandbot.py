# commandbot.py

import irclib, nicktrack, tbf

class CommandBot(nicktrack.Nicktrack):
	def __init__(self, *args, **kwargs):
		super(CommandBot, self).__init__(*args, **kwargs)
		self.tbf=tbf.TokenBucketFilter()
		self.commands={}

		self.AddHandler("privmsg", self._command_privmsg, -25)
		self.AddHandler("pubmsg", self._command_pubmsg, -25)


	def CheckLimit(self, weight=1):
		return self.tbf.account(weight)
	

	def __RunCommand(self, event):
		content=event.arguments()[0]
		data=content.lstrip().split(None, 2)
		if len(data)==0:
			return None
		if len(data)==1:
			data.append("")
		(command,data)=(data[0][1:], data[1])
		if command not in self.commands:
			return None

		nick=self.people[irclib.nm_to_n(event.source())]
		return self.commands[command](nick, data)


	def _command_privmsg(self, connection, event):
		res=self.__RunCommand(event)
		if res:
			self.connection.privmsg(
					irclib.nm_to_n(event.source()), res)


	def _command_pubmsg(self, connection, event):
		res=self.__RunCommand(event)
		if res:
			self.connection.privmsg(event.target(), res)

