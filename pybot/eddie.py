# eddie.py

import commandbot
import re, urllib, random

class Eddie(commandbot.CommandBot):
	def __init__(self, *args, **kwargs):
		super(Eddie, self).__init__(*args, **kwargs)
		self.commands["reload"]=self._eddie_reload
		self.commands["espresso"]=self._eddie_espresso
		self.commands["whisky"]=self._eddie_whisky
		self._eddie_load()


	def _eddie_load(self):
		#TODO: delete eddie_* first
		eddie_code=getattr(__import__("pybot.eddie"),"eddie")
		eddie_class=getattr(eddie_code, "Eddie")
		for func in dir(eddie_class):
			if func.startswith("eddie_"):
				print "loading eddie: %s" % func
				self.commands[func[6:]]=Eddie.__dict__[func]


	def _eddie_reload(self, nick, text):
		#TODO: check levels, etc
		eddiepy = getattr(__import__("pybot.eddie"), "eddie")
		reload(eddiepy)
		self._eddie_load()


	def _eddie_whisky(self, nick, text):
		malts=( "Aberlour 10 years",
			"Aberlour 12 years",
			"AnCnoc 12 years",
			"Ardmore",
			"Arran 10 years",
			"Arran Sherry",
			"Auchroisk 28 years",
			"Ardbeg 10 years",
			"Ardbeg Uigeadail",
			"Ardbeg Airigh Nam Beist",
			"Ardbeg Corry Vreckan",
			"Ardbeg Supernova",
			"Auchentoshan 10 years",
			"Auchentoshan 12 years",
			"Bunnahabhain 12 years",
			"Bunnahabhain 18 years",
			"Bladnoch 13 years",
			"Balblair 10 years",
			"Balvenie 12 years signature",
			"Balvenie 12 years double wood",
			"Balvenie 15 years",
			"Balvenie 1993 portwood",
			"Balvenie madeira cask",
			"Balvenie sherry oak 17 years",
			"Balvenie portwood 21 years",
			"Bladnoch Lowland 13 years",
			"Bruichladdich 12 se",
			"Bruichladdich Fifteen",
			"Bruichladdich 1998 sherry",
			"Bruichladdich organic",
			"Ben Nevis 10 years",
			"Benriach Heart of Speyside",
			"Benriach 12 years",
			"Benromach tradition",
			"Benromach organic",
			"Blue Hanger 4th Release",
			"Caol Ila 12 years",
			"Caol Ila 18 years",
			"Caol Ila D.E. Moscatel",
			"Caol Ila 23 years",
			"Cardhu 12 years",
			"Clynelisch 14 years",
			"Clynelisch Berrys' Own 1993",
			"Cragganmore 12 years",
			"Dalmore 12 years",
			"Dalwhinnie 15 years",
			"Dalwhinnie dist. ed.",
			"Drumguish",
			"Edradour 10 years",
			"Glen Deveron 10 years",
			"Glen Elgin 12 years",
			"Glen Garioch 10 years",
			"Glen Grant",
			"Glen Keith 13 years",
			"Glenkinchie 10 years",
			"Glenkinchie 12 years",
			"Glen Moray 12 years",
			"Glen Ord 12 years",
			"Glendronach 12 years",
			"Glendronach 15 years",
			"Glenfarclas 8 years",
			"Glenfarclas 10 years",
			"Glenfarclas 12 years",
			"Glenfarclas 15 years",
			"Glenfarclas 21 years",
			"Glenfarclas 25 years",
			"Glenfiddich 12 years",
			"Glenfiddich 15 years solera",
			"Glenfiddich 18 years ancient res.",
			"Glenfiddich 21 years gran res.",
			"Glenfiddich 30 years",
			"Glengoyne 10 years",
			"Glengoyne 17 years",
			"Glengoyne 21 years",
			"Glenlivet 12 years",
			"Glenlivet 15 years French oak",
			"Glenlivet 18 years",
			"Glenmorangie portwood",
			"Glenmorangie 10 years",
			"Glenrothes 1994",
			"Glenrothes 1991",
			"Glenturret 10 years",
			"Glen Scotia 14 years",
			"Highland Park 12 years",
			"Highland Park 18 years",
			"Highland Park 15 years Magnus",
			"Highland Park 19 years Ultimate",
			"Highland Park 16 years S. cask",
			"Highland Park 30 years",
			"Lagavulin 16 years",
			"Lagavulin L.E. 1990",
			"Lagavulin 12 years 1995",
			"Longrow Gaja fin.",
			"Laphroaig 10 years",
			"Laphroaig 15 years",
			"Laphroaig 18 years",
			"Laphroaig 25 years",
			"Laphroaig signatory 2001",
			"Laphroaig Berrys' Own 1990",
			"Laphroaig Hag Rap Oil 9 years",
			"Macallan Fine Oak 10 years",
			"Macallan Fine Oak 12 years",
			"Macallan Fine Oak 15 years",
			"Macallan Fine Oak 18 years",
			"Macallan Sherry Oak 12 years",
			"Macallan Sherry Oak 7 years",
			"Macallan 21 years Signatory 1988",
			"Old Ballantruan ",
			"Old Pulteney 12 years",
			"Port Askaig 17 years",
			"Rosebank 1990 Berrys' Own",
			"Rosebank 1981 Daily Dram",
			"Springbank 10 years",
			"Springbank 15 years",
			"Springbank 1997",
			"Tamdhu",
			"Tamnavulin 12 years",
			"Talisker 10 years",
			"Tomatin 12 years",
			"Bushmills Original",
			"Bushmills Black Bush",
			"Bushmills Malt 10 years",
			"Bushmills Malt 16 years",
			"Connemara",
			"Knappoque Castle 1995",
			"Red Breast 12 years")

		malt=random.choice(malts)
		msg="schenkt %s een glaasje %s in." % (nick.nick, malt)
		self.server.ctcp("ACTION", self.config["IRC/channel"], msg)


	def _eddie_espresso(self, nick, text):
		#return "De espresso is tijdelijk niet verkrijgbaar."
		msg="schenkt %s een overheerlijk kopje espresso in!" % nick.nick
		self.server.ctcp("ACTION", self.config["IRC/channel"], msg)
		#return None


	def eddie_zut(nick, text):
		return "zut alors, %s!" % nick.nick


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
		wun=wunderground()
		return "Het weer: %s Graden (voelt als %s) / %s / Luchtvochtigheid %s%% / Wind %s km/u" % (wun["deg"], wun["feel"], wun["wea"], wun["hum"], wun["wind"])


	def eddie_maan(nick, text):
		fasemap={"New Moon":"nieuwe maan", 
			"Waxing Crescent":"wassende maan",
			"First Quarter":"halve maan (eerste kwartier)",
			"Waxing Gibbous":"wassende halve maan",
			"Full Moon":"volle maan",
			"Waning Gibbous":"afnemende volle maan",
			"Last Quarter":"halve maan (laatste kwartier)",
			"Waning Crescent":"afnemende maan"}
	
		maan=wunderground()["moon"]
		try:
			(fase, illu)=maan.split(', ')
		except:
			return "Het is hier veel te donker om de maan te zien."
		#try:
		#	fase=fasemap[fase]
                #except:
		#	fase="blauwe maan"

		illu=illu[0:illu.find('%')]
		return "Het is %s, %s%% is verlicht." % (fase, illu)

	def eddie_zon(nick, text):
		zonop="?:??"
		zononder="?:??"
		rtlweer="http://www.rtl.nl/actueel/rtlweer/nederland/index.xml"
		u=urllib.urlopen(rtlweer)
		lines=u.read().splitlines()
		u.close()
		for l in range(len(lines)): 
			if '>Zon op/onder<' in lines[l]:
				zonop=lines[l+1][11:-4]
				zononder=lines[l+2][11:-8]
		return "Zon op %s, zon onder %s" % (zonop, zononder)

	def eddie_babelfish(nick, text): 
		phrase = text

		try:
			lang = language(phrase)
	 	except KeyError, e: 
			msg = "Ik spreek geen %s..." % str(e).split().pop()
			return msg

	 	if lang is None:
	 		return

		translation = translate(phrase, lang)
		if translation is not None: 
			msg = '"%s" (%s)' % (translation, lang)
			return msg


def wunderground():
	wun={}
	wun["deg"]="?";
	wun["wea"]="Geen weer";
	wun["wind"]="x";
	wun["hum"]="??";
	wun["moon"]="Spontane maansverduistering";
	wund="http://dutch.wunderground.com/global/stations/06240.html"
	u=urllib.urlopen(wund)
	lines=u.read().splitlines()
	u.close()
	for l in range(len(lines)): 
		if '<div id="curCond">' in lines[l]:
			wl=lines[l]
			wun["wea"]=wl[wl.find('>')+1:wl.find('</div>')]

		if '<div id="nowTemp">' in lines[l]:
			wl=lines[l+3]
			wun["deg"]=wl[wl.find('"b"')+4:wl.find('</span>')]
		if '<div id="tempFeel">' in lines[l]:
			wl=lines[l+1]
			wun["feel"]=wl[wl.find('"b"')+4:wl.find('</span>')]


		if '<div id="conds_details_moisture">' in lines[l]:
			wl=lines[l+3]
			wun["hum"]=wl[wl.find('<nobr>')+6:wl.find('</nobr>')]

		if '<div id="conds_details_wind">' in lines[l]:
			wl=lines[l+5]
			wun["wind"]=wl[wl.find('"b"')+4:wl.find('</span>')]

		if 'id="moonTable">' in lines[l]:
			moon=lines[l+2]
			wun["moon"]=moon[moon.find('>')+1:moon.find('</td>')]
	return wun




def wunderground_old():
	wun={}
	wun["deg"]="?";
	wun["wea"]="Geen weer";
	wun["wind"]="x";
	wun["hum"]="??";
	wun["moon"]="Spontane maansverduistering";
	wund="http://dutch.wunderground.com/global/stations/06240.html"
	u=urllib.urlopen(wund)
	lines=u.read().splitlines()
	u.close()
	for l in range(len(lines)): 
		if '<td class="vaM taC full">' in lines[l]:
			deg=lines[l+2]
			wun["deg"]=deg[deg.find('"b"')+4:deg.find('</span>')]
			wea=lines[l+4]
			wun["wea"]=wea[wea.find('>')+1:wea.find('</div>')]
		if '<td>Luchtvochtigheid:</td>' in lines[l]:
			hum=lines[l+1]
			wun["hum"]=hum[hum.find('<nobr>')+6:hum.find('</nobr>')]
		if '<td>Wind:</td>' in lines[l]:
			wind=lines[l+3]
			wun["wind"]=wind[wind.find('"b"')+4:wind.find('</span>')]
		if 'id="moonTable">' in lines[l]:
			moon=lines[l-1]
			wun["moon"]=moon[moon.find('>')+1:moon.find('</div>')]
	return wun

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



