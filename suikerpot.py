#!/usr/bin/python

import re
import irclib, basicbot

def IsFriend(nick):
	if not getattr(nick, "mask", None):
		return 0

	try:
		for line in open('friends').readlines():
			words=re.split("\s",line.rstrip())
			if len(words)==0:
				continue
			
			if re.search("^%s$" % words[0], nick.mask):
				if len(words)==2:
					return int(words[1])
				return 1

	except IOError,x:
		print "Unable to open 'friends' file: ",x
	
	return 0



class SuikerPot(basicbot.BasicBot):
	PublicCommands	= { }

	def OnEndOfNames(self, connection, event):
		self.server.privmsg(event.arguments()[0],
				self.config["messages/startup"])

	def OnPubMsg(self, connection, event):
		basicbot.BasicBot.OnPubMsg(self, connection, event)

		msg=event.arguments()[0]
		channel=event.target()

		args=msg[1:].split(None, 1)
		(cmd,args)=(args[0], args[1:])
		func="PubCmd"+cmd.capitalize()
		if msg[0]=='!' and hasattr(self, func):
			nick=self.people[irclib.nm_to_n(event.source())]
			getattr(self, func)(channel, nick, args)


	def OnPrivMsg(self, connection, event):
		basicbot.BasicBot.OnPrivMsg(self, connection, event)

		msg=event.arguments()[0]
		args=msg[1:].split(None, 1)
		(cmd,args)=(args[0], args[1:])
		func="PrivCmd"+cmd.capitalize()
		if msg[0]=='!' and hasattr(self, func):
			nick=self.people[irclib.nm_to_n(event.source())]
			getattr(self, func)(nick, args)


	def OnJoin(self, connection, event):
		basicbot.BasicBot.OnJoin(self, connection, event)

		nick=irclib.nm_to_n(event.source())
		if nick==self.connection.get_nickname():  # this is us!
			self.logger.info("We finished joining %s ourselves" 
					% event.target())
			return 

		if IsFriend(event.source()):
			self.logger.info("%s is a friend, giving ops" % nick)
			self.op(nick)
		else:
			self.logger.info("%s is not a friend, giving voice and sending welcome message" % nick)
			self.voice(nick)
			if self.CheckLimit():
				self.connection.notice(nick.nick, self.config["messages/welcome"])
	

	def PubCmdKoffie(self, channel, nick, args):
		if self.CheckLimit():
			self.server.ctcp("ACTION", channel,
					self.config["messages/koffie"] % nick.nick)
	

	def PubCmdKlant(self, channel, nick, args):
		if self.CheckLimit():
			self.server.privmsg(channel,
					self.config["messages/klant"])



	def PrivCmdOp(self, nick, args):
		if IsFriend(nick)>1:
			self.server.privmsg(nick.nick, "You will be opped")
			self.op(nick.nick)
		else:
			self.server.privmsg(nick.nick, "Sorry, I do not trust you.")


if __name__ == "__main__":
	bot=SuikerPot()
	bot.MainLoop()

