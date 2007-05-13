# eddie.py

import commandbot
import re, urllib

class Eddie(commandbot.CommandBot):
	def __init__(self, *args, **kwargs):
		super(Eddie, self).__init__(*args, **kwargs)
		self._eddie_load()
		self.commands["reload"]=self._eddie_reload

	def _eddie_load(self):
		self.commands["zut"]=eddie_zut
		self.commands["babel"]=eddie_babelfish

	def _eddie_reload(self, nick, text):
		#TODO: check levels, etc
   		eddiepy = getattr(__import__("pybot.eddie"), "eddie")
		reload(eddiepy)
		self._eddie_load()

def eddie_zut(nick, text):
		return "zut alors %s, %s!" % (nick, text)



def language(phrase): 
   languages = {
      'english': 'en', 
      'scots': 'en', 
      'german': 'de', 
      'greek': 'el', 
      'french': 'fr', 
      'rumantsch': 'fr', 
      'bosnian': 'fr', 
      'spanish': 'es', 
      'romanian': 'es', 
      'italian': 'it', 
      'japanese-shift_jis': 'ja', 
      'dutch': 'nl', 
      'afrikaans': 'nl', 
      'frisian': 'nl', 
      'middle_frisian': 'nl', 
      'portuguese': 'pt', 
      'albanian': 'ru', 
      'russian': 'ru', 
      'unknown': 'nl'
   }
 
   query = urllib.quote(phrase)
   u = urllib.urlopen('http://ziu.let.rug.nl/vannoord_bin/tc?a1=' + query)
   bytes = u.read()
   u.close()
   for line in bytes.splitlines(): 
      if '<pre>' in line: 
         language = line[line.find('<pre>') + 5: line.find('</pre>')]
         return languages[language.strip(' \t').lower()]
   return None

r_translation = re.compile(r'<div style=padding:10px;>([^<]+)</div>')

def translate(phrase, lang): 
   babelfish = 'http://world.altavista.com/tr'
   tolang='_en'
   if lang=='en': tolang='_nl'

   form = {
      'doit': 'done', 
      'intl': '1', 
      'tt': 'urltext', 
      'trtext': phrase, 
      'lp': lang + tolang
   }

   u = urllib.urlopen(babelfish, urllib.urlencode(form))
   bytes = u.read()
   u.close()

   m = r_translation.search(bytes)
   if m: 
      print m.group(1)
      translation = m.group(1)
      translation = translation.replace('\r', '')
      return translation.replace('\n', ' ')
   return None

def eddie_babelfish(nick, text): 
   phrase = text

   try: lang = language(phrase)
   except KeyError, e: 
      msg = "Ik spreek geen %s..." % str(e).split().pop()
      return msg

   if lang is None: return

   translation = translate(phrase, lang)
   if translation is not None: 
      msg = '"%s" (%s)' % (translation, lang)
      return msg
