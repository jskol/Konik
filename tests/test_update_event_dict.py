import pytest

import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent
sys.path.append(parent_dir)
from app.event_class.event_class import event

from app.web_page_details import web_page

page=web_page()
from app.event_dict.gen_dict import gen_event_dict
ballet_dict=gen_event_dict(web_page,1,False) # generate a dict of plays

from app.event_dict.update_dict import update_shows_dict


def test_update_size_1():
    num_of_evetns_pre=len(ballet_dict.keys())
    print("Pre-update: ", ballet_dict)
    update_shows_dict(ballet_dict, web_page.base_url)
    print("After update: ", ballet_dict)
    num_of_evetns_after=len(ballet_dict.keys())
    assert num_of_evetns_after <= num_of_evetns_pre

