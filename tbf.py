# tbf.py

import time

class TokenBucketFilter:
	"""Token Bucket Filter implementation.

	This class can be used to rate-limit events.
	"""
	def __init__(self):
		self.max=5
		self.tokens=self.max
		self.last=time.time()

	def account(self, charge=1):
		now=time.time()
		self.tokens+=(now-self.last)/2
		if self.tokens>self.max:
			self.tokens=self.max
		self.last=now
		if self.tokens<0:
			return 0

		self.tokens-=charge
		if self.tokens>0:
			return 1
		else:
			return 0



