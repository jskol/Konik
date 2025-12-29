import os,sys

curr_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(curr_dir)
sys.path.append(os.path.dirname(parent_dir))

from app.create_ticket_database.data_base import TicketDataBase, compare_two_dicts_of_shows


def collect_new_tickets(
    DB_type : TicketDataBase,
    path_to_new_DB: str,
    path_to_old_DB: str
    )->dict[tuple[str,str],dict[str,str]]:
    '''
    Extracts new tickets by comparing the
    new DB with old one
    '''
    
    if \
    os.path.isfile(path_to_new_DB) \
    and \
    os.path.isfile(path_to_old_DB):
        read_DB_new = DB_type.importDB(path_to_new_DB)
        read_DB_old = DB_type.importDB(path_to_old_DB)
        comp_Res=compare_two_dicts_of_shows(read_DB_new,read_DB_old)

        # trim the zero-tickets-cases
        new_tickets={ k:v  for k,v in comp_Res.items() if any(v.values())}
        return new_tickets