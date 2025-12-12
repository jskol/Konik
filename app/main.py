
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from web_page_details import web_page

page=web_page() # Its a singleton 
event_type_list=[
    "Balet","Opera"
]

from event_dict.gen_dict import gen_event_dict
from event_dict.update_dict import update_shows_dict
from event_dict.export_event_dict import export_dict

if __name__=="__main__":
    ballet_dict=gen_event_dict(page,2,event_type_list[0],True) # generate a dict of plays
    #do an update by hand
    update_shows_dict(ballet_dict)
    final_dict=export_dict(ballet_dict)

    for k,v in final_dict.items():
        print(f'{k}: {v}')




