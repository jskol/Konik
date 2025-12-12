
import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent dir
sys.path.append(parent_dir)

from app.main import page, event_type_list
from app.event_dict.gen_dict import gen_event_dict
from app.event_dict.update_dict import update_shows_dict
from app.event_dict.export_event_dict import export_dict

from app.create_ticket_database.data_base import TicketDBJSON,compare_two_dicts_of_shows
DB=TicketDBJSON()

dict1=DB.importDB('DB')
dict2=DB.importDB('DB_altered')

new_ticket_dict=compare_two_dicts_of_shows(dict1,dict1)
DB.notify(new_ticket_dict,['foo@gmail.com'])
