import pytest,json,random
import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent dir
sys.path.append(parent_dir)

from app.main import event_type_list
from app.event_dict.gen_dict import gen_event_dict
from app.event_dict.update_dict import update_shows_dict
from app.event_dict.export_event_dict import export_dict

from app.create_ticket_database.data_base import TicketDBJSON,compare_two_dicts_of_shows
DB=TicketDBJSON()



from app.create_ticket_database.user_class import User_Email
#Create list of users
U1=User_Email('John','Doe','johndoe@gmail.com')
U2=User_Email('Jane','Doe','janedoe@gmail.com')
U3=User_Email('Foo', 'Bar','FooBar@gmail.com')
list_of_subscribers=[U1,U2,U3]

@pytest.mark.parametrize("num_of_monts,list_of_users",[(1,list_of_subscribers)])
def test_the_notification_functionality(num_of_monts,list_of_users):
    DB_name=os.path.join(curr_dir,f'DB_{num_of_monts}')
    if not os.path.isfile(DB_name+'.json'):
        '''
        If DB is missing-> make it
        '''
        ballet_dict=gen_event_dict(num_of_monts,event_type_list[0],False) # generate a dict of plays
        update_shows_dict(ballet_dict)
        final_dict=export_dict(ballet_dict)
        DB.exportDB(final_dict,DB_name)

    # make the alternate versions with different number of seats
    DB_alternates=list(map(
            lambda x: os.path.join(curr_dir,x),
            [f'{DB_name}_more',f'{DB_name}_less',f'{DB_name}_same_but_different']
        ))
    diff=[4,-4]
    for it,DB_alt in enumerate(DB_alternates):
        if not os.path.isfile(DB_alt+'.json'):
            with open(DB_name+".json",'r') as f:
                data=json.load(f)
            
            update_made=False
            while not update_made:
                ev_num=random.randint(0,len(data)-1)
                ev_dict=data[ev_num]
                ev_keys=list(ev_dict.keys())
                if len(ev_dict)>3:
                    
                    sector=random.randint(3,len(ev_dict)-1)
                    sec_name=ev_keys[sector]
                    seat_num=ev_dict[sec_name]
                    
                    if it !=2:
                        ev_dict[sec_name]=seat_num+diff[it]
                        free_seats=ev_dict['free seats total']
                        ev_dict['free seats total']=free_seats+diff[it]
                    else:
                        sector_2=random.randint(3,len(ev_dict))
                        if sector_2==sector: # percusion to not update the same sector
                            while sector_2 == sector:
                                sector_2=random.randint(3,len(ev_dict)-1)
                        
                        sec_name_2=ev_keys[sector_2]
                        seat_num_2=ev_dict[sec_name_2]
                        
                        ev_dict[sec_name]=seat_num+3
                        ev_dict[sec_name_2]=seat_num_2-3
                    
                    update_made=True


            with open(f'{DB_alt}.json','w') as f:
                json.dump(data,f,indent=4)

    dict1=DB.importDB(DB_name)
    for DB_alt in DB_alternates:        
        dict2=DB.importDB(DB_alt)
        new_ticket_dict=compare_two_dicts_of_shows(dict1,dict2)
        notification_sent= DB.notify(new_ticket_dict,list_of_users)
  
        if notification_sent:
            assert notification_sent
        else:
            assert not notification_sent


# For quick chec-up on the testing procedures
if __name__=="__main__":
    num_of_monts=1
    with open(f'DB_{num_of_monts}.json','r') as f:
        data=json.load(f)
    for entry in data:
        print(entry)    
    print(len(data))
    test_the_notification_functionality(num_of_monts,list_of_subscribers)