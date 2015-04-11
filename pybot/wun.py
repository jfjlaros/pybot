#!/usr/bin/python
import urllib

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

print wunderground()
