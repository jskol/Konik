import pytest
import os,sys
cur_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(cur_dir))

from app.create_ticket_database.data_base import TicketDBJSON, compare_two_dicts_of_shows
DB=TicketDBJSON()

main_DB_path=os.path.join(cur_dir,'DB_update_1')

test_cases=[(main_DB_path+x[0],x[1]) for x in [('_less',True),('_more',False),('_same_but_different',True)]]

@pytest.mark.parametrize("ref_DB,has_tickets",test_cases)
def test_check_for_new_tickets(ref_DB, has_tickets):
    read_DB = DB.importDB(os.path.join(cur_dir,'DB_update_1'))
    read_DB2 = DB.importDB(ref_DB)
    comp_Res=compare_two_dicts_of_shows(read_DB,read_DB2)
   
    new_tickets={ k:v  for k,v in comp_Res.items() if any(v.values())}

    print(f'len={len(new_tickets)}, for {ref_DB}')    
    print(list(new_tickets.keys()))
    assert bool(len(new_tickets)>0) == has_tickets

from app.create_ticket_database.extract_new_tickets import extract_new_tickets

@pytest.mark.parametrize("ref_DB,has_tickets",test_cases)
def test_compare_check_for_new_tickets_with_extract(ref_DB, has_tickets):
    read_DB = DB.importDB(main_DB_path)
    read_DB2 = DB.importDB(ref_DB)
    comp_Res=compare_two_dicts_of_shows(read_DB,read_DB2)
    new_tickets={ k:v  for k,v in comp_Res.items() if any(v.values())}
    
    new_tickets_V2=extract_new_tickets(DB,main_DB_path,ref_DB)

    for old,new in zip(new_tickets.items(),new_tickets_V2.items()):
        assert old[0]==new[0]

if __name__=="__main__":
    read_DB=DB.importDB('DB_1')
    name='DB_1_less'
    read_DB2=DB.importDB(name)
    comp_Res=compare_two_dicts_of_shows(read_DB,read_DB2)

    new_tickets={ k:v  for k,v in comp_Res.items() if any(v.values())}
    print(f'len={len(new_tickets)}, for {name}')    
    print(list(new_tickets.keys()))
    for k,v in comp_Res.items():
        if any(v.values()):
            print(k, " : ", v)