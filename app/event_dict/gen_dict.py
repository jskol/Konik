import datetime,calendar,requests
import bs4
from collections import defaultdict

import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent
sys.path.append(parent_dir)
from web_page_details import web_page
from event_class.event_class import event
from pick_event_type.pick_event_type import pick_eventtype_name

def gen_event_dict(page:web_page, months_to_check:int, event_type_name:str ="Balet",print_events:bool =True)-> dict[str,list[event]]:
    month_it=0
    ballet_dict=defaultdict(list)
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
    now_is=datetime.datetime.now()
    while month_it < months_to_check: 
        year,month=now_is.year,now_is.month
        num_days = calendar.monthrange(year, month)[1]
        url=page.base_url+"/kalendarium/data/%i/"%year
        url+= "{:0=2d}".format(month) # need two digit number format
        url+= "/#/f/0/1-%i"%num_days
        try:
            sub_page = requests.get(url,headers=headers)
            sub_page.raise_for_status()
            soup=bs4.BeautifulSoup(sub_page.content,'html.parser')
            events=soup.find_all("div", {"class": "event-in"})

            ballets=pick_eventtype_name(events,event_type_name= event_type_name)
            for ballet in ballets:
                ballet_dict[ballet.title].append(ballet)
        except requests.exceptions.HTTPError :
            print(" Problem z dostępem do strony z wydarzniami dla %i-%i"%(year,month))
        now_is += datetime.timedelta(days=num_days)
        month_it +=1
    
    if print_events:
        print("Balety w najbliższych %i miesiącach"% months_to_check)
        for it,x in enumerate(list(ballet_dict.keys())):
            out="%i: %s"%(it+1,x)
            if ballet_dict[x][0].teaser is not None:
                out += ": %s"%ballet_dict[x][0].teaser
            print(out)
    
    return ballet_dict

