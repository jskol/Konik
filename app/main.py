import bs4 as bs
import requests
from urllib.request import urlopen

import datetime
import calendar
import re

from event_class.event_class import event
from pick_event_type.pick_event_type import pick_eventtype_name

from web_page_details import web_page

page=web_page()
from event_dict.gen_dict import gen_event_dict
ballet_dict=gen_event_dict(web_page,1,False) # generate a dict of plays

#from check_tickets.check_tickets import analize_availability #check_for_tickets
#analize_availability(ballet_dict,page.base_url,False)             
from event_dict.update_dict import update_shows_dict

print("Pre-update: ", ballet_dict)
update_shows_dict(ballet_dict, web_page.base_url)
print("After update: ", ballet_dict)

from check_tickets.get_ticket_num import iterate_over_room_layout
for name, event_list in ballet_dict.items():
    for show in event_list:
        print(" Analyzing tickets for %s"%name)
        print(web_page.base_url+show.link)
        #iterate_over_room_layout(web_page.base_url+show.link)