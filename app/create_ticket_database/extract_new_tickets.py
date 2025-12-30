import os,sys
cur_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(cur_dir))

from app.create_ticket_database.data_base import TicketDataBase, compare_two_dicts_of_shows

def  extract_new_tickets(DB_type: TicketDataBase,
                         new_DB_file: str,
                         ref_DB_file: str
                         )->dict[tuple[str,str],dict[str,int]]:
    
    '''
    Function that extracts only the events
    that have more tickets then it had
    in the ref_DB
    '''
    if not os.path.isfile(f'{new_DB_file}.{DB_type._extension}'):
        raise FileNotFoundError
    else:
        read_DB = DB_type.importDB(new_DB_file)
        try:
            read_DB2 = DB_type.importDB(ref_DB_file)
            comp_Res=compare_two_dicts_of_shows(read_DB,read_DB2)    
        except FileNotFoundError:
            comp_Res=read_DB
            
        new_tickets={ k:v  for k,v in comp_Res.items() if any(v.values())}

        return new_tickets
