import pytest
import os,sys
cur_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(cur_dir))

from app.create_ticket_database.data_base import TicketDBJSON, compare_two_dicts_of_shows
DB=TicketDBJSON()


test_cases=[
    (os.path.join(cur_dir,'DB_1_less'),True),
    (os.path.join(cur_dir,'DB_1_more'),False),
    (os.path.join(cur_dir,'DB_1_same_but_different'),True)
]



@pytest.mark.parametrize("ref_DB,has_tickets",test_cases)
def test_check_for_new_tickets(ref_DB, has_tickets):
    read_DB = DB.importDB(os.path.join(cur_dir,'DB_1'))
    read_DB2 = DB.importDB(ref_DB)
    comp_Res=compare_two_dicts_of_shows(read_DB,read_DB2)
    #print(comp_Res)
    for DB1,DB2,DB3 in zip(read_DB.items(),read_DB2.items(),comp_Res.items()):
        print(f'shows: {DB1[0]}, {DB2[0]}, {DB3[0]}')
        print(f'main: {DB1[1]}\nref:{DB2[1]}\ndiff:{DB3[1]}')    
    
    new_tickets={ k:v  for k,v in comp_Res.items() if any(v.values())}

    print(f'len={len(new_tickets)}, for {ref_DB}')    
    print(list(new_tickets.keys()))
    assert bool(len(new_tickets)>0) == has_tickets



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