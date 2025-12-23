import re



def fix_name(event_type_name:str)->str:
    '''
    Deal with the wonders of polish language (flexion)
    '''
    event_name_str=event_type_name
    event_name_str=re.sub('a$','', event_name_str)
    event_name_str += 'y'
    return event_name_str

import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(curr_dir)
sys.path.append(parent_dir)
from app.create_ticket_database.data_base import TicketDataBase
from tests.helper_functions import create_DB_if_missing
import pathlib,datetime


def read_DB(
    DB:TicketDataBase,
    event_num:int
    )->tuple[
        dict[tuple[str,str],dict[str,int]],
        str
        ]:
    '''
    Read the database and check the date 
    of its last modification
    return tuple of:
    1) event dict shows name and seats available
    2) string with date of the last modifiaction
    of the DB file
    '''
    curr_dir=os.path.dirname(os.path.abspath(__file__))
    parent_dir=os.path.dirname(curr_dir)
    DB_location=os.path.join(parent_dir,'Ticket_DB',f'DB_event_{event_num}')
    #create_DB_if_missing(DB,DB_location,num_of_months=2,event_type_in_list=event_num)
    #Get last update time
    path=pathlib.Path(DB_location+f'.{DB._extension}')
    time=path.stat().st_mtime
    date_str=datetime.datetime.fromtimestamp(time).strftime("%d/%m/%Y @ %H:%M")
    event_dict=DB.importDB(DB_location)
    return event_dict, date_str
    