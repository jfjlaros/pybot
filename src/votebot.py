# votebot.py

import commandbot

class VoteBot(commandbot.CommandBot):
	def __init__(self, *args, **kwargs):
		super(VoteBot, self).__init__(*args, **kwargs)

		self.commands["vote"]=self._votebot_vote
	
	def _votebot_vote(self, nick, text):
		params=text.strip().split()
		if len(params)!=1:
			return

		command=params[0].lower()
		if command=="start":
			for nick in self.people.keys():
				try:
					delattr(self.people[nick], "vote")
				except AttributeError:
					pass
			return "Starting a new vote"
		elif command=="stop":
			votes={"yes" : 0, "no" : 0, "abstain" : 0, "skip" : 0}
			for person in self.people.values():
				votes[getattr(person, "vote", "skip")]+=1

			if votes["yes"]>votes["no"]:
				result="yes"
			elif votes["yes"]<votes["no"]:
				result="no"
			else:
				result="tie"
			return ("vote result: %s. %d yes votes, %d no votes and %d abstains" %
				(result, votes["yes"], votes["no"], votes["abstain"]))


		elif command=="yes":
			nick.vote="yes"
			return "Noted yes vote from %s" % nick.nick
		elif command=="no":
			nick.vote="no"
			return "Noted no vote from %s" % nick.nick
		elif command=="abstain":
			nick.vote="abstain"
			return "Noted that %s abstains" % nick.nick

