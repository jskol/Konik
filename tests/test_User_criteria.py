'''
Testing the user specific feedback about the 
availibity of tickets
'''
import pytest

import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)
sys.path.append(os.path.dirname(curr_dir))

from helper_functions import create_DB_if_missing

from app.create_ticket_database.data_base import TicketDBJSON,compare_two_dicts_of_shows
DB=TicketDBJSON()

from app.create_ticket_database.user_class import User_Email,User
U1=User_Email('John','Doe','johndoe@gmail.com')
U1.intersted_in(list_of_excluded_sectors=['1. Plan gowny','Parter'])

U2=User_Email('Jane','Doe','janedoe@gmail.com')
U2.intersted_in(list_of_included_sectors=['1. Plan gowny','Parter'])

U3=User_Email('Parter','Guy','Parter_guy@gmail.com')
U3.intersted_in(list_of_included_sectors=['Parter'])

U4=User_Email('Take-All','Guy','Take-All_Guy@gmail.com')
U4.intersted_in(list_of_excluded_sectors=[])



DB_path=os.path.join(curr_dir,'DB_1')


@pytest.mark.parametrize('DB_path_param,user,ref_val',
                         
                         ids=[
                            'Exclude test',
                            'Include 2 sectors',
                            'Include 1 sector',
                            'Take all tickets'       
                         ],
                         argvalues=[
                            (DB_path,U1,0),
                            (DB_path,U2,1),
                            (DB_path,U3,1),
                            (DB_path,U3,2)
                          ])
def test_custom_notification_functionality(DB_path_param:str,user:User,ref_val:int)->None:
    create_DB_if_missing(DB,DB_path_param,1,0)
    DB_to_test=DB.importDB(DB_path_param)
    return_DB=user.return_intersting_seats(DB_to_test)
    for show_key,show_val in return_DB.items():
        match ref_val:
            case 1:
                len(show_val)-1 <= len(user.criteria["sector_include"])
            case 2:
                len(show_val) == len(DB_to_test[show_key])
            case _:
                len(show_val)-1 >= len(user.criteria["sector_exclude"])


if __name__=="__main__":
        
    test_custom_notification_functionality('DB_test',U1)
    test_custom_notification_functionality('DB_test',U2)
    test_custom_notification_functionality('DB_test',U3)