#!/usr/bin/python

import datetime, sys
import irclib, ircbot, tbf

class Nick:
	def __init__(self, nick, mask=None, voice=False, ops=False):
		self.nick=nick
		self.voice=voice
		self.ops=ops
		if mask!=None:
			self.mask=mask



class BasicBot(ircbot.IrcBot):
	"""A basic template for an irc bot.

	This class is more advanced that the standard IrcBot and knows how
	to delegate commands to methods and will log events.
	"""

	PublicCommands	= { }

	def __init__(self, conffile="config"):
		super(BasicBot, self).__init__(conffile)
		self.tbf=tbf.TokenBucketFilter()
		self.people={}


	def CheckLimit(self, weight=1):
		return self.tbf.account(weight)
	

	def RegisterNick(self, event):
		nick=irclib.nm_to_n(event.source())
		if not nick in self.people:
			self.people[nick]=Nick(nick, event.source())
		elif not hasattr(self.people[nick], "mask"):
			self.people[nick].mask=event.source()

		self.people[nick].seen=datetime.datetime.now()
		return self.people[nick]


	def OnConnect(self, connection, event):
		"""IRC event method - server connection established.

		This method is called when the connection to an IRC server
		is fully established.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		self.logger.info("connection to server %s completed" % 
			self.connection.get_server_name())


	def OnNamReply(self,connection,event):
		"""IRC event method - name received.

		This method is called when information about a name/
		nick on our channel is received.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		for nick in event.arguments()[2]:
			if nick[0]=='@':
				self.people[nick[1:]]=Nick(nick[1:], ops=True)
			elif nick[0]=='+':
				self.people[nick[1:]]=Nick(nick[1:], voice=True)
			else:
				self.people[nick]=Nick(nick)

		self.logger.info("Person on channel: %s" % event.arguments()[2])


	def OnEndOfNames(self, connection, event):
		"""IRC event method - end of name list.

		This method is called when information all names have been
		transmitted.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		self.logger.info("End of namelist, join completed")


	def OnJoin(self, connection, event):
		"""IRC event method - user joined our channel.

		This method is called when a user joins a channel we are on.
		Also called when we ourself finish joining a channel.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		self.logger.info("%s joined %s" % (event.source(), event.target()))
		nick=irclib.nm_to_n(event.source())
		self.people[nick]=Nick(nick, mask=event.source())


	def OnPart(self, connection, event):
		"""IRC event method - user parted our channel.

		This method is called when a user parts from channel we are on.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""

		nick=irclib.nm_to_n(event.source())
		if nick in self.people:
			del self.people[nick]

		self.logger.info("%s parted channel %s" % (nick, event.target()))


	def OnQuit(self, connection, event):
		"""IRC event method - user quits.

		This method is called when a user quits irc while he is on a
		channel we are on.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		nick=irclib.nm_to_n(event.source())
		if nick in self.people:
			del self.people[nick]

		self.logger.info("%s quit irc with reason: %s" % 
			(nick, event.arguments()[0]))


	def OnPrivMsg(self, connection, event):
		"""IRC event method - private message.

		This method is called when a user sends a privmsg to us.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		content = event.arguments()
		self.logger.info("privmsg: %s : %s" % 
			(irclib.nm_to_n(event.source()), content[0]))
		self.RegisterNick(event)



	def OnPubMsg(self, connection, event):
		"""IRC event method - public message.

		This method is called when we receive a public (on-channel)
		message from a user.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		content = event.arguments()
		self.logger.info("pubmsg: %s : %s" % 
			(irclib.nm_to_n(event.source()), content[0]))
		self.RegisterNick(event)


	def OnCTCP(self, connection, event):
		"""IRC event method - CTCP event recieved.

		This method is called when we receive a CTCP event.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		if event.arguments()[0]=="ACTION" and len(event.arguments()) > 1:
			print " * "+irclib.nm_to_n(event.source())+" "+event.arguments()[1]


	def OnTopic(self, connection, event):
		"""IRC event method - channel topic change.

		This method is called when the topic on one of our channels
		is changed.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		self.logger.info("%s changed topic to %s" %
			(event.source(), event.arguments()[0]))
		self.RegisterNick(event)
	

	def OnDisconnect(self, connection, event):
		"""IRC event method - disconnect from irc

		This method is called when we are disconnected from the
		IRC server.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		self.logger.warn("Disconnect received, exiting")
		sys.exit(1)
		

	def OnNick(self, connection, event):
		"""IRC event method - nick change

		This method is called when someone who shares a channel with
		us changes his/her nickname.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		nick=self.RegisterNick(event)
		self.logger.info("%s changed nick to %s" %
			(nick.nick, event.target()))
		self.people[event.target()]=self.people[nick.nick]
		del self.people[nick.nick]

