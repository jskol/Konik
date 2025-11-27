import datetime,sys,os
import bs4 as bs

curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent
sys.path.append(parent_dir)

from event_class.event_class import event
def pick_eventtype_name(events: list[bs.ResultSet],event_type_name:str ="Balet") -> list[event]:
    ballets=[]
    current_day=datetime.datetime.now()
    for ballet in events:
        event_type=ballet.find("span", {"class":"category"})
        if event_type and event_type.text==event_type_name:
            temp_ev=event(ballet)
            if temp_ev.time >= current_day:
                ballets.append(temp_ev)

    return ballets