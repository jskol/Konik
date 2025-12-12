
import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent dir
sys.path.append(parent_dir)

from app.main import page, event_type_list
from app.event_dict.gen_dict import gen_event_dict
from app.event_dict.update_dict import update_shows_dict
from app.event_dict.export_event_dict import export_dict

from app.create_ticket_database.data_base import TicketDBJSON
DB=TicketDBJSON()


ballet_dict=gen_event_dict(page,2,event_type_list[0],False) # generate a dict of plays
update_shows_dict(ballet_dict)
final_dict=export_dict(ballet_dict)
DB.exportDB(final_dict,'DB')

readDB=DB.importDB('DB')
#new_ticket_dict=DB.update(final_dict,'DB')
#DB.notify(new_ticket_dict,['skolimowski.jan@gmail.com'])

for (k1,v1),(k2,v2) in zip(readDB.items(),final_dict.items()):
    assert k1 == k2
    assert v1 == v2


