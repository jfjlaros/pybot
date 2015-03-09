# eddie.py

import commandbot
import re, urllib

class Eddie(commandbot.CommandBot):
	def __init__(self, *args, **kwargs):
		super(Eddie, self).__init__(*args, **kwargs)
		self.commands["reload"]=self._eddie_reload
		self._eddie_load()

	def _eddie_load(self):
		#TODO: delete eddie_* first
   		for f in dir(getattr(__import__("pybot.eddie"),"eddie")):
			if f.startswith("eddie_"):
				print "loading eddie: %s" % f
				self.commands[f[6:]]=globals()[f]

	def _eddie_reload(self, nick, text):
		#TODO: check levels, etc
   		eddiepy = getattr(__import__("pybot.eddie"), "eddie")
		reload(eddiepy)
		self._eddie_load()

def eddie_zut(nick, text):
	return "zut alors, %s!" % nick.nick

def eddie_espresso(nick, text):
	return "De espresso is tijdelijk niet verkrijgbaar."
	#msg="schenkt %s een overheerlijk kopje espresso in!" % nick.nick
	#self.server.ctcp("ACTION", self.config["IRC/channel"], msg)
	#return None

def eddie_koekie(nick, text):
	return "Koekie d'rbij?"

def eddie_koekje(nick, text):
	return "Koekje d'rbij?"

def eddie_bier(nick, text):
	return "lekker!"

def eddie_weekend(nick, text):
	return "nu al?"

def eddie_wekeend(nick, text):
	return "KWAK!"

def eddie_weer(nick, text):
	return "Het weer: %s Graden / %s" % wunderground()[0:2]

def eddie_maan(nick, text):
	fasemap={"New Moon":"nieuwe maan", 
                 "Waxing Crescent":"wassende maan",
                 "First Quarter":"halve maan (eerste kwartier)",
                 "Waxing Gibbous":"wassende halve maan",
                 "Full Moon":"volle maan",
                 "Waning Gibbous":"afnemende volle maan",
                 "Last Quarter":"halve maan (laatste kwartier)",
                 "Waning Crescent":"afnemende maan"}

	maan=wunderground()[2]
	try:
		(fase, illu)=maan.split(', ')
	except:
		return "Het is hier veel te donker om de maan te zien."
        fase=fasemap[fase]
	illu=illu[0:illu.find('%')]
	return "Het is %s, %s%% is verlicht." % (fase, illu)


def wunderground():
	deg="?";
	wea="Geen weer";
	moon="Spontane maansverduistering";
	wund="http://dutch.wunderground.com/global/stations/06240.html"
	u=urllib.urlopen(wund)
	lines=u.read().splitlines()
	u.close()
	for l in range(len(lines)): 
		if '<td class="vaM taC full">' in lines[l]:
			deg=lines[l+4]
			deg=deg[deg.find('<b>')+3:deg.find('</b>')]
			wea=lines[l+6]
			wea=wea[wea.find('>')+1:wea.find('</div>')]
		if 'id="moonTable">' in lines[l]:
			moon=lines[l-1]
			moon=moon[moon.find('>')+1:moon.find('</h4>')]
	return (deg, wea, moon)

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
