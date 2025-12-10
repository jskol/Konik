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
event_type_list=[
    "Balet","Opera"
]

from event_dict.gen_dict import gen_event_dict

ballet_dict=gen_event_dict(page,2,event_type_list[0],False) # generate a dict of plays

from event_dict.update_dict import update_shows_dict

update_shows_dict(ballet_dict, web_page.base_url)

