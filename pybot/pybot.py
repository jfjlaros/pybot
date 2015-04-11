#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime, random
import mx.DateTime
from . import logbot, commandbot, votebot, irclib, eddie

class Event:
    pass

def GetEventsForDate(dbc, cfg, date):
    res=dbc.query("SELECT DISTINCT id FROM %s WHERE date=%%s" %
            cfg["Paradiso/table"], (date,), "format")
    ids=map(lambda x: x[0], res)
    events=[]

    for id in ids:
        res=dbc.query("SELECT date,attribute,value FROM %s WHERE id=%%s" % cfg["Paradiso/table"],
            (id,), "format")
        if not res:
            continue

        event=Event()
        event.id=id
        event.date=res[0][0]
        for (date,attr,value) in res:
            setattr(event, attr, value)

        events.append(event)

    return events


class Bolt(logbot.LogBot, votebot.VoteBot, eddie.Eddie):
    def __init__(self, *args, **kwargs):
        super(Bolt, self).__init__(*args, **kwargs)

        self.zenActive=False

        self.AddHandler("pubmsg", self._no_colours_please)
        self.commands["seen"]=self.CommandSeen
        self.commands["koffie"]=self.CommandKoffie
        self.commands["thee"]=self.CommandThee
        self.commands["linkurl"]=self.CommandUrlLog
        self.commands["urlog"]=self.CommandUrlLog
        self.commands["urlgrep"]=self.CommandUrlGrep
        self.commands["zen"]=self.CommandZen
        self.commands["do"]=self.CommandDo
        self.commands["say"]=self.CommandSay

        self.commands["klant"]=self.CommandKlant
        self.commands["customer"]=self.CommandCustomer
        self.commands["cliente"]=self.CommandCliente
        self.commands["kunde"]=self.CommandKunde
        self.commands["kund"]=self.CommandKund
        self.commands["asiakas"]=self.CommandAsiakas
        self.commands["client"]=self.CommandClient

#        self.commands["paradiso"]=self.CommandParadiso

        self.AddHandler("join", self._voice_join)


    def _no_colours_please(self, connection, event):
        nick=irclib.nm_to_n(event.source())
        msg=event.arguments()[0]
        evil=[c for c in msg if ord(c)<=27]
        if len(evil):
            self.devoice(nick)
            self.server.ctcp("ACTION", self.config["IRC/channel"],
                    "wordt bijna doof!")


    def GetUserLevel(self, nickmask):
        self.sqlverify()
        try:
            res=self.dbc.query("SELECT mask, level FROM ircopers WHERE channel=%s",
                (self.config["IRC/channel"],), "format")
            for (mask,level) in res:
                if irclib.mask_matches(nickmask, str(mask)):
                    return level
        except self.dbc.Error, e:
            print ".. database error! %s" % str(e)
            self.logger.error("GetUserLevel failed: %s" % e)

        return 0
    

    def CommandUrlLog(self, nick, text):
        return "http://irc.fixedpoint.nl/koffie/linkurl"


    def CommandKlant(self, nick, text):
        return "En weer verlaat een tevreden klant het pand"


    def CommandCustomer(self, nick, text):
        return "And yet again a satisfied customer exits the building"


    def CommandCliente(self, nick, text):
        # Spanish version
        return "Y un otro cliente satsifecho sale del edificio"


    def CommandAsiakas(self, nick, text):
        # Finnish version by liw
        return u"Ja jälleen yksi tyytyväinen asiakas poistuu rakennuksesta".encode("raw_unicode_escape")

    def CommandKunde(self, nick, text):
        # German version by Ganneff
        return u"Und wieder verlässt ein zufriedener Kunde das Gebäude".encode("raw_unicode_escape")

    def CommandKund(self, nick, text):
        # Swedish version by maswan
        return u"Och ännu en nöjd kund lämnar byggnad".encode("raw_unicode_escape")

    def CommandClient(self, nick, text):
        # French version by JohnR
        return u"Mais encore un client satisfait sort le bâtiment".encode("raw_unicode_escape")

    def CommandThee(self, nick, text):
        if not self.CheckLimit():
            return

        product=random.choice(["Earl Grey", "mango", "groene ",
                "kaneel", "bosvruchten", "citroen"])
        msg="schenkt %s een lekker kopje %sthee in" % (nick.nick, product)
        self.server.ctcp("ACTION", self.config["IRC/channel"], msg)


    def CommandKoffie(self, nick, text):
        if not self.CheckLimit():
            return

        chance=random.randint(0, 20)
        if chance<=1:
            product="decafe"
        elif chance<5:
            product=random.choice([ "espresso", "cappuccino",
                    "irish coffee", "koffie verkeerd",
                    "wiener melange"])
        else:
            product="koffie"

        msg="schenkt %s een lekker kopje %s in" % (nick.nick, product)
        self.server.ctcp("ACTION", self.config["IRC/channel"], msg)


    def CommandParadiso(self, nick, text):
        today=mx.DateTime.now()-mx.DateTime.TimeDelta(hours=6)
        today=mx.DateTime.DateTime(today.year, today.month, today.day)
        events=GetEventsForDate(self.dbc, self.config, today)

        response="Playing in paradiso today: " + \
            ", ".join(map(lambda x: x.info_naam, events))
        return response.encode("ascii", "ignore")


    def CommandDo(self, nick, text):
        if not self.CheckLimit():
            return

        try:
            level=self.GetUserLevel(nick.mask)
        except AttributeError:
            return

        if level<100:
            return

        self.server.ctcp("ACTION", self.config["IRC/channel"], text)


    def CommandSay(self, nick, text):
        if not self.CheckLimit():
            return

        try:
            level=self.GetUserLevel(nick.mask)
        except AttributeError:
            return

        if level<100:
            return

        self.connection.privmsg(self.config["IRC/channel"], text)


    def CommandZen(self, nick, text):
        if self.zenActive:
            return

        if not self.CheckLimit():
            return

        scan=text.split(None, 1)
        try:
            level=self.GetUserLevel(nick.mask)
        except AttributeError:
            print "attribute error, nick has no mask"
            print "nick is %s" % `nick`
            print "nick is %s" % nick.__dict__
            level=0

        print "userlevel: %s" % level

        chance=10 + level/2
        print "change limit: %d" % chance
        if random.randint(0, 100)>=chance:
            print "random not hit.. skipping"
            return

        if level<0:
            return "Geen zen voor jou. Kom volgend jaar maar terug."
        elif level>0 and len(scan)>1 and scan[0].lower()=="voor":
            target=scan[1]
        else:
            target=nick.nick

        self.zenActive=True
        self.server.ctcp("ACTION", self.config["IRC/channel"], 
                "mediteert voor %s" % target)
        self.irc.execute_delayed(random.randint(5, 30)*60,
                self.ZenFinished, (target,))


    def ZenFinished(self, target):

        licht="verlichting"
        today=mx.DateTime.now()
        if today.month==12 and today.day>5:
            licht="kerstverlichting"

        easterstart=mx.DateTime.Feasts.EasterFriday(today.year)
        easterend=mx.DateTime.Feasts.EasterSunday(today.year)+2
        if easterstart<=today and today<=easterend:
            licht="paasverlichting"

        msg="heeft volledige %s bereikt voor %s" % (licht, target)
        self.server.ctcp("ACTION", self.config["IRC/channel"], msg)
        self.zenActive=False


    def _voice_join(self, connection, event):
        nick=irclib.nm_to_n(event.source())
#        if nick==self.connection.get_nickname():  # this is us!
#            self.logger.info("We finished joining %s ourselves" 
#                    % event.target())
#            return 

        if self.CheckLimit(weight=2):
            if self.GetUserLevel(event.source())>=100:
                self.op(nick)
            else:
                self.voice(nick)
                self.connection.notice(nick, self.config["messages/welcome"])

def main():
    """
    Main entry point.
    """
    bot=Bolt(config=".pybot.conf")
    bot.MainLoop()


if __name__ == "__main__":
    main()
