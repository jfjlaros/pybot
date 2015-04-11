# sqlbot.py

import dhm.sql.wrap
import ircbot

class SQLBot(ircbot.IrcBot):
    def __init__(self, *args, **kwargs):
        super(SQLBot, self).__init__(*args, **kwargs)
        self.sqlconnect()

    
    def sqlconnect(self):
        self.logger.info("(Re)connecting to SQL server")
        self.sqlserver=dhm.sql.wrap.GetServer(self.config["SQL/driver"])
                #host=self.config["SQL/server"],
                #user=self.config["SQL/username"],
                #password=self.config["SQL/password"])
        self.dbc=self.sqlserver[self.config["SQL/database"]]
    

    def sqlverify(self):
        try:
            self.dbc.query("SELECT 1");
        except self.dbc.Error, e:
            self.logger.warn("Database connection not working: %s" % e)
            self.sqlconnect()
    
    def sqlexecute(self, sql, params=()):
        self.sqlverify()
        try:
            self.dbc.execute(sql, params, "format")
            self.dbc.commit()
        except self.dbc.Error, e:
            self.dbc.rollback()
            raise

    def sqlquery(self, sql, params=()):
        self.sqlverify()
        try:
            res=self.dbc.query(sql, params, "format")
            self.dbc.commit()
            return res
        except self.dbc.Error, e:
            self.dbc.rollback()
            raise

