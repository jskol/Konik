import bs4 as bs
import requests
from urllib.request import urlopen

import datetime
import calendar
import re

from event_class.event_class import event
from pick_event_type.pick_event_type import pick_eventtype_name

month_it=0
from collections import defaultdict
ballet_dict=defaultdict(list)
months=5
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
    try:
        page = requests.get(url,headers=headers)
        page.raise_for_status()
        soup=bs.BeautifulSoup(page.content,'html.parser')
        events=soup.find_all("div", {"class": "event-in"})

        ballets=pick_eventtype_name(events)
        for ballet in ballets:
            ballet_dict[ballet.title].append(ballet)
    except requests.exceptions.HTTPError :
        print(" Problem z dostępem do strony z wydarzniami dla %i-%i"%(year,month))
    now_is += datetime.timedelta(days=num_days)
    month_it +=1

print("Balety w najbliższych %i miesiącach"% months)
for it,x in enumerate(list(ballet_dict.keys())):
    out="%i: %s"%(it+1,x)
    if ballet_dict[x][0].teaser is not None:
        out += ": %s"%ballet_dict[x][0].teaser
    print(out)

from check_tickets.check_tickets import check_for_tickets
event_num=1
for ballet_name in list(ballet_dict.keys()):
    for ev in ballet_dict[ballet_name]:
        print("#%i: %s"%(event_num,ev.title))
        check_for_tickets(base_url, ev)
        event_num+=1
            
