import pytest

import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent
sys.path.append(parent_dir)

from app.event_dict.gen_dict import gen_event_dict
ballet_dict=gen_event_dict(1,"Balet",False) # generate a dict of plays

from app.event_dict.update_dict import update_shows_dict

@pytest.mark.parametrize("num_of_months",[1,2,3])
def test_update_size_1(num_of_months):
    '''
    Simple test to see if after update the number of events didn't 
    excceded the number of all events in a given time period
    TEST IS SLOW
    '''
    ballet_dict=gen_event_dict(num_of_months,"Balet",False) # generate a dict of plays
    num_of_evetns_pre=len(ballet_dict.keys())
    print("Pre-update: ", ballet_dict)
    update_shows_dict(ballet_dict)
    print("After update: ", ballet_dict)
    num_of_evetns_after=len(ballet_dict.keys())
    assert num_of_evetns_after <= num_of_evetns_pre

