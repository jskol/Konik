import pytest
import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent dir
sys.path.append(parent_dir)

from app.main import event_type_list
from app.event_dict.gen_dict import gen_event_dict
from app.event_dict.update_dict import update_shows_dict
from app.event_dict.export_event_dict import export_dict

from app.create_ticket_database.data_base import TicketDBJSON
DB=TicketDBJSON()


@pytest.mark.parametrize("num_of_monts",[1])
def test_dict_to_DB_and_back_transfotmation(num_of_monts):
    '''
    The goal of the test is to see if 
    none of the information about the events is lost
    after transforming a dict of events into a JSON format 
    and back
    '''

    ballet_dict=gen_event_dict(num_of_monts,event_type_list[0],False) # generate a dict of plays
    update_shows_dict(ballet_dict)
    final_dict=export_dict(ballet_dict)
    DB.exportDB(final_dict,os.path.join(curr_dir,f'DB_{num_of_monts}'))
    readDB=DB.importDB(os.path.join(curr_dir,f'DB_{num_of_monts}'))

    for (k1,v1),(k2,v2) in zip(readDB.items(),final_dict.items()):
        assert k1 == k2
        assert v1 == v2




