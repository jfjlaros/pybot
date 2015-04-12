#!/usr/bin/python
# yes this is fugly.

import posix

user="www-data"
if posix.getuid()==1005:
	user="bot"

import dhm.sql.wrap, re

urlmatcher      = re.compile(
        r"\b(?P<url>(?P<scheme>http|https|ftp)://"
        r"(?:(?P<login>(?P<username>[a-zA-Z0-9]+)(?::(?P<password>[A-Za-z0-9]+))?)@)?"
        r"(?P<hostname>[A-Za-z0-9.-]+(?::(?P<port>[0-9]+))?)"
        r"(?P<path>[A-Za-z0-9@~=?/.,&;#+-_%]*))")

print "Content-type: text/html\n"
print "<?xml version=\"1.0\" encoding=\"iso-8859-1\"?>"
print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">"
print "<html lang=\"en\" xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\">"
print "  <head>"
print "    <meta content=\"text/html; charset=utf-8\" http-equiv=\"Content-Type\" />"
print "    <link href=\"http://lithium.liacs.nl/~bot/style/linkurl.css\" type=\"text/css\" rel=\"stylesheet\" />"
print "    <title>UrlLog for #koffie</title>"
print "  </head>"
print "  <body>"
print "    <h1>UrlLog for #koffie</h1>"
print "    <div id=\"content\">"
print "      <table>"
print "        <thead>"
print "        <tr>"
print "            <th>Time</th>"
print "            <th>Nick</th>"
print "            <th>Text</th>"
print "        </tr>"
print "        </thead>"
print "        <tbody>"
print "          <tr>"
#print "            <td class=\"time\">2007-02-24 22:29</td>"
#print "            <td class=\"nick\">&lt;Dominique&gt;</td>"
#print "            <td class=\"text\"><a href=\"http://woonkrant.nl/woonkrant/woning/koop/kopen/26022056/overview/veenhuizerveldweg__48_3881_re_putten.html?woonkrantServer=0\">http://woonkrant.nl/woonkrant/woning/koop/kopen/26022056/overview/veenhuizerveldweg__48_3881_re_putten.html?woonkrantServer=0</a></td>"
#print "          </tr>"
#print "          <tr></tr>"

#sqlserver=dhm.sql.wrap.GetServer("postgres", host="localhost", user=user, password="")
sqlserver=dhm.sql.wrap.GetServer("postgres")
dbc=sqlserver["pybot"]

res=dbc.query("SELECT time, nick, text FROM channel WHERE url='t' ORDER BY time DESC LIMIT 50")

for r in res:
  print "<tr>"
  print "  <td class=\"time\">%s</td>" % ("%s" % r[0])[0:16]
  print "  <td class=\"nick\">&lt;%s&gt;</td>" % r[1]
  urltxt=urlmatcher.search(r[2]).group()
  urlstart=urlmatcher.search(r[2]).start()
  urlend=urlmatcher.search(r[2]).end()

  print "  <td class=\"text\">%s<a href=\"%s\">%s</a>%s</td>" % (r[2][:urlstart], urltxt, urltxt, r[2][urlend:])
  print "</tr>"
  print "<tr></tr>"

print "        </tbody>"
print "      </table>"
print "    </div>"
print "  </body>"
print "</html>"
