import os,sys
import copy

from typing import Any
from abc import ABC,abstractmethod


cur_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from event_class.event_class import event


class User(ABC):
    '''
    An abstract user class that holds
    the name,surname and eventually some
    criteria for tickets of interest
    '''
    def __init__(self,name:str, surname:str):
        self.name=name
        self.surname=surname
        self.criteria={"sector_exclude": None, 
                       "sector_include":None,
                       "price_min":None, 
                       "price_max":None
                    } 

    def intersted_in(self,
                     list_of_excluded_sectors:list[str]=None,
                      list_of_included_sectors:list[str]=None,
                      price_min: int = None,
                      price_max:int=None
                      )->None:
        '''
        here will be all criterions 
        the user has for the new tickets
        to be interested in them
        !!! If NO criteria is passed ALL tickets
        will be returned
        '''
        if list_of_included_sectors:
            self.criteria["sector_include"]=list_of_included_sectors
        if list_of_excluded_sectors:
            self.criteria["sector_exclude"]=list_of_excluded_sectors
        if price_max:
            self.criteria["price_max"]=price_max
        if price_min:
            self.criteria["price_min"]=price_min

    
    def return_intersting_seats(self,list_of_events:dict[tuple[str,str],dict[str,int]])->dict[tuple[str,str],dict[str,int]]:
                
        if self.criteria["sector_exclude"]: # one gave list of sectors to avoid
            interesting_events=copy.deepcopy(list_of_events) #make a DEEP!copy of list of events to work on
            for _,seats in interesting_events.items(): #iterate over all events
                #print(seats)
                for remove_sector in self.criteria["sector_exclude"]: #iterate over sectors to remove
                    #update number of free seats
                    seat_num=seats['free seats total']
                    try: # try to find if remove sector is in keys of seats
                        seats['free seats total'] = seat_num\
                        - seats[remove_sector]
                        #and remove this sector
                        seats.pop(remove_sector)
                    except KeyError:    
                        continue

        elif self.criteria["sector_include"]:
            #interesting_events=copy.deepcopy(list_of_events)
            interesting_events={} #create a new dict from the ground up
            for event_key,seats in interesting_events.items(): #iterate over all events
                new_seat_dict={}
                new_seat_dict['free seats total']=0
                for sector in self.criteria["sector_include"]:
                    try: # try if the sector is in the keys of seats
                        if seats[sector]:
                            new_seat_dict['free seats total'] += seats[sector]
                            new_seat_dict[sector] = seats[sector]
                    except KeyError:
                        continue
                interesting_events[event_key]=new_seat_dict
        else:
            interesting_events=copy.deepcopy(list_of_events) #return a DEEP copy to work on later 
        
        return interesting_events
    
    @abstractmethod
    def notify(self,list_of_events : dict[tuple[str,str],dict[str,int]])->None:
        pass


class User_Email(User):

    def __init__(self,name:str,surname:str, address:str):
        super().__init__(name,surname)
        self.address=address
    
    def notify(self, list_of_events : dict[tuple[str,str],dict[str,int]])->None:
        intersting_events=self.return_intersting_seats(list_of_events)
        if len(intersting_events)>0:
            print(f'Sending email to {self.name} {self.surname} at {self.address}')
            for k,v in intersting_events.items():
                print(f'\t{k[0]} @ {k[1]}')
                #print("Problematic v: ", v)
                for k2,v2 in v.items():
                    if v2 >0:
                        print(f'\t\t {k2}: {v2}')
        pass


class User_Phone(User):
    def __init__(self,name:str,surname:str, phone_number:str):
        super().__init__(name,surname)
        self.phone_number=phone_number

    def notify(self,list_of_events:dict[tuple[str,str],dict[str,int]])->None:
        intersting_events=super().notify(list_of_events)
        if len(intersting_events)>0:
            print(f'Sending an SMS to {self.name} {self.surname} at {self.phone_number}')
        pass
    
    

