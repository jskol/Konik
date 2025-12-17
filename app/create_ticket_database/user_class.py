import os,sys

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
        '''
        if list_of_included_sectors:
            self.criteria["sector_include"]=list_of_included_sectors
        if list_of_excluded_sectors:
            self.criteria["sector_exclude"]=list_of_excluded_sectors
        if price_max:
            self.criteria["price_max"]=price_max
        if price_min:
            self.criteria["price_min"]=price_min

    
    def notify(self,list_of_events:dict[tuple[str,str],dict[str,int]])->dict[tuple[str,str],dict[str,int]]:
        intersting_events=list_of_events.copy() #make a copy of list of events to work on
        if self.criteria["sector_exclude"]: # one gave list of sectros to avoid
            for _,seats in intersting_events.items(): #iterate over all events
                for remove_sector in self.criteria["sector_exclude"]: #iterate over sectors to remove
                    seats.pop(remove_sector)
        
        if self.criteria["sector_include"]:
            for _,seats in intersting_events.items(): #iterate over all events
                for keys in seats.keys():
                    if keys not in self.criteria["sector_include"] and keys != 'free seats total':
                        seats.pop(keys)
                
        # Do some testing of this functionality
        return intersting_events


class User_Email(User):

    def __init__(self,name:str,surname:str, address:str):
        super().__init__(name,surname)
        self.address=address
    
    def notify(self, list_of_events : dict[tuple[str,str],dict[str,int]])->None:
        intersting_events=super().notify(list_of_events)
        if len(intersting_events)>0:
            print(f'Sending email to {self.name} {self.surname} at {self.address}')
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
    
    

