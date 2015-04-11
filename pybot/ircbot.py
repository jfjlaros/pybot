# ircbot.py

import logging
import dhm.config, dhm.nestdict
import irclib

class IrcBot(object):
    """Generic IRC bot code.

    This class implements the basis of an irc bot: it takes care of
    communication with an irc server and translating irc events into
    python method calls.

    Event handlers are implemented by creating a method whose name starts
    with 'On' followed by the name of the method (case is not relevant).
    These will be automatically discovered in the constructor.
    
    @ivar connection: IRC connection instance
    @ivar     server: IRC server instance
    @ivar     logger: logging object
    """

    def __init__(self, *args, **kwargs):
        """IrcBot constructor.

        @param conffile: name of configuration file
        @type  conffile: string
        """
        self.config=dhm.nestdict.NestedDict(
                dhm.config.Parse(kwargs["config"]))
        self.logger=logging.getLogger("ircbot")

        self.irc=irclib.IRC()
        self.server=self.irc.server()

        self.logger.info("Connecting to irc server " + 
                self.config["IRC/server"])
        self.connection=self.server.connect(self.config["IRC/server"],
            self.config["IRC/port"], self.config["IRC/nick"],
            username=self.config["IRC/name"])

        self.logger.info("Trying to join channel " + 
                self.config["IRC/channel"])
        if self.config.has_key("IRC/password"):
            self.server.join(self.config["IRC/channel"],
                    self.config["IRC/password"])
        else:
            self.server.join(self.config["IRC/channel"])
        
        for i in filter(lambda x: x.startswith("On"), dir(self)):
            self.connection.add_global_handler(i[2:].lower(),
                getattr(self, i))


    def AddHandler(self, event, func, prio=0):
        self.connection.add_global_handler(event, func, prio)


    def devoice(self,nick):
        """Remove voice a nick on our channel.

        @param nick Nick to devoice.
        @type  nick string
        """
        self.logger.debug("devoicing %s" % nick)
        self.connection.mode(self.config["IRC/channel"],"-v "+nick)


    def voice(self,nick):
        """Give voice a nick on our channel.

        @param nick Nick to voice.
        @type  nick string
        """
        self.logger.debug("voicing %s" % nick)
        self.connection.mode(self.config["IRC/channel"],"+v "+nick)


    def op(self,nick):
        """Give ops to a nick on our channel.

        @param nick Nick to op.
        @type  nick string
        """
        self.logger.debug("giving ops to %s" % nick)
        self.connection.mode(self.config["IRC/channel"],"+o "+nick)


    def leave(self):
        """Instruct eventloop to exit.
        """
        self.pleaseQuit=1


    def MainLoop(self):
        """Bot main event loop.

        This starts the main event loop which continues running
        until internal logic decides to end things by calling
        leave().
        """
        self.pleaseQuit=0

        self.logger.info("Starting main eventloop")
        try:
            self.irc.process_forever(1)
        except KeyboardInterrupt:
            self.logger.warn("Received interrupt, disconnecting from irc")
            #self.irc.disconnect_all("^C received")
            self.irc.disconnect_all("even de suiker bijvullen")
        
            self.logger.info("Finished disconnecting, shutting down")
