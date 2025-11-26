import bs4 as bs
import mechanicalsoup as ms
from urllib.request import urlopen

import datetime
import calendar
import re

from event_class import event

def pick_ballets(events: list[bs.ResultSet],event_type_name:str ="Balet") -> list[event]:
    ballets=[]
    current_day=datetime.datetime.now()
    for ballet in events:
        event_type=ballet.find("span", {"class":"category"})
        if event_type and event_type.text==event_type_name:
            temp_ev=event(ballet)
            if temp_ev.time> current_day:
                ballets.append(temp_ev)

    return ballets

month_it=0
from collections import defaultdict
ballet_dict=defaultdict(list)
months=5
browser=ms.Browser()
base_url="https://teatrwielki.pl"
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
now_is=datetime.datetime.now()
while month_it < months: 
    year,month=now_is.year,now_is.month
    num_days = calendar.monthrange(year, month)[1]
    url=base_url+"/kalendarium/data/%i/"%year
    url+= "{:0=2d}".format(month) # need two digit number format
    url+= "/#/f/0/1-%i"%num_days
    page = browser.get(url,headers=headers)
    assert page.status_code==200
    soup=page.soup

    #print(soup)

    events=soup.find_all("div", {"class": "event-in"})

    ballets=pick_ballets(events)
    for ballet in ballets:
        ballet_dict[ballet.title].append(ballet)
    #list(map(lambda x: ballet_dict[x.title].append(x), ballets)) # unnecessary creation of an additional list
    now_is += datetime.timedelta(days=num_days)
    month_it +=1

print("Balety w najbliższych %i miesiącach"% months)
for it,x in enumerate(list(ballet_dict.keys())):
    out="%i: %s"%(it+1,x)
    if ballet_dict[x][0].teaser is not None:
        out += ": %s"%ballet_dict[x][0].teaser
    print(out)


for it,pg in enumerate(ballet_dict[' Peer Gynt ']):
    print( it, " ", pg.time)
from check_tickets import check_for_tickets

check_for_tickets(base_url, ballet_dict[' Pinokio '][0])
