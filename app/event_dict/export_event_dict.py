import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from event_class.event_class import event

def export_dict(dict_of_shows : dict[str,list[event]])->dict[tuple[str,str],dict[str,int]]:
    '''
    From dict where events are strored in dict
    with name of the show as key and list of events as value
    to dict with a tuple name,date askey and dict of seats as value
    '''
    final_dict={}
    for _, list_of_shows in dict_of_shows.items():
        for shows in list_of_shows:
            temp=shows.export_as_dict()
            final_dict.update(temp)
    
    return final_dict

