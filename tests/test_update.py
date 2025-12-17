import pytest
import os,sys
cur_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(cur_dir))

from app.create_ticket_database.data_base import TicketDBJSON, compare_two_dicts_of_shows
DB=TicketDBJSON()


test_cases=[
    ('DB_1_more',False),
    ('DB_1_less',True),
    ('DB_1_same_but_different',True)
]

@pytest.mark.parametrize("ref_DB,has_tickets",test_cases)
def test_check_for_new_tickets(ref_DB, has_tickets):
    read_DB=DB.importDB('DB_1')
    read_DB2=DB.importDB(ref_DB)
    comp_Res=compare_two_dicts_of_shows(read_DB,read_DB2)
    new_tickets=[{k:v} for k,v in comp_Res.items() if any(v.values())]
    assert len(new_tickets) == has_tickets

if __name__=="__main__":
    read_DB=DB.importDB('DB_1')
    read_DB2=DB.importDB('DB_1_same_but_different')
    comp_Res=compare_two_dicts_of_shows(read_DB,read_DB2)
    for k,v in comp_Res.items():
        if any(v.values()):
            print(k, " : ", v)