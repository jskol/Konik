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
from gen_event_dict.gen_dict import gen_event_dict
ballet_dict=gen_event_dict(web_page,12,False)

from check_tickets.check_tickets import analize_availability #check_for_tickets
analize_availability(ballet_dict,page.base_url,False)
            
