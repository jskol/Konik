import pytest

import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(curr_dir))
from app.check_tickets.check_tickets import check_for_tickets
from app.event_dict.gen_dict import gen_event_dict
from app.web_page_details import web_page


page_main=web_page()
ballet_dict=gen_event_dict(web_page,1,"Balet",False)
from app.event_dict.update_dict import update_shows_dict
print(ballet_dict)
update_shows_dict(ballet_dict, web_page.base_url)
print(ballet_dict)
exit()


event_look_up=ballet_dict[list(ballet_dict.keys())[-1]]
print(event_look_up[0])
check_for_tickets(web_page.base_url,event_look_up[-2],False)

'''
@pytest.mark.parametrize("url_main, event, print_out",[
    (web_page.base_url,event_look_up[0],False)
])
def test_check_for_tickets(url_main,event,print_out):
    check_for_tickets(url_main,event,print_out)
'''    
