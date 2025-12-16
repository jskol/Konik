import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent to import some subrutines
sys.path.append(parent_dir)
from event_class.event_class import event


def update_shows_dict(shows_dict: dict[str,list[event]])->None:
    '''
    In-place update of shows in the calendar
    the update means mainly the ticket-situation
    '''
    for k,v in shows_dict.items():
        for show in v:
            show.update_ticket_num()
    
