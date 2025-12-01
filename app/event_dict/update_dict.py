



import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent to import some subrutines
sys.path.append(parent_dir)
from check_tickets.check_tickets import check_for_tickets
from event_class.event_class import event


def update_shows_dict(shows_dict: dict[str,list[event]], base_url:str )->None:
    '''
    In-place update of shows in the calendar
    '''
    for event_name in list(shows_dict.keys()):
        event_list=shows_dict[event_name]
        updated_event_list=[event_it for event_it in event_list if check_for_tickets(base_url,event_it,False)>0]
        if len(updated_event_list)>0:
            shows_dict.update({event_name:updated_event_list})
        else:
            shows_dict.pop(event_name)


