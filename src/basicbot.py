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

	def __init__(self, conffile="config"):
		super(BasicBot, self).__init__(conffile)
		self.tbf=tbf.TokenBucketFilter()
		self.people={}

		self.add_global_handler("namreply", self._nicktrack_namreply)
		self.add_global_handler("join", self._nicktrack_join)
		self.add_global_handler("part", self._nicktrack_part)
		self.add_global_handler("quit", self._nicktrack_quit)
		self.add_global_handler("privmsg", self._nicktrack_log)
		self.add_global_handler("pubmsg", self._nicktrack_log)
		self.add_global_handler("topic", self._nicktrack_log)
		self.add_global_handler("nick", self._nicktrack_nick)


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


	def _nicktrack_namreply(self, connection, event):
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


	def _nicktrack_join(self, connection, event):
		"""IRC event method - user joined our channel.

		This method is called when a user joins a channel we are on.
		Also called when we ourself finish joining a channel.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		self.logger.info("%s joined %s" % (event.source(),
						event.target()))
		nick=irclib.nm_to_n(event.source())
		self.people[nick]=Nick(nick, mask=event.source())


	def _nicktrack_part(self, connection, event):
		"""IRC event method - user parted our channel.

		This method is called when a user parts from channel we are on.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""

		nick=irclib.nm_to_n(event.source())
		if nick in self.people:
			del self.people[nick]

		self.logger.info("%s parted channel %s" % (nick, event.target()))


	def _nicktrack_quit(self, connection, event):
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


	def _nicktrack_log(self, connection, event):
		"""IRC event method - we saw a user talk.

		This method is called when a user talks to use using a
		pubmsg or privmsg.

		@param connection IRC connection instance
		@param event      IRC event causing this method invocation
		"""
		content = event.arguments()
		self.logger.info("talked: %s : %s" % 
			(irclib.nm_to_n(event.source()), content[0]))
		self.RegisterNick(event)


	def _nicktrack_nick(self, connection, event):
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

