import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(curr_dir))


from app.main import event_type_list
from app.event_dict.gen_dict import gen_event_dict
from app.event_dict.update_dict import update_shows_dict
from app.event_dict.export_event_dict import export_dict    

from app.create_ticket_database.data_base import TicketDBJSON,TicketDataBase


def create_DB_if_missing(DB_type:TicketDataBase,
                      DB_name:str, #dont use the extension
                      num_of_months:int, 
                      event_type_in_list:int=0)->None:
    '''
    If DB is missing-> make it
    '''
    if not os.path.isfile(DB_name+f'.{DB_type._extension}'):
        print(f'Creating the missing DB: {DB_name}.{DB_type._extension}')
        ballet_dict=gen_event_dict(num_of_months,event_type_list[event_type_in_list],False) # generate a dict of plays
        update_shows_dict(ballet_dict)
        final_dict=export_dict(ballet_dict)
        DB_type.exportDB(final_dict,DB_name)
        print("Done")
    else:
        print("DB- found")

if __name__=="__main__":
    DB=TicketDBJSON()
    create_DB_if_missing(DB,"DB_test",num_of_months=1)
    