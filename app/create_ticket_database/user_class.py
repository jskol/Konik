import os,sys

from typing import Any
from abc import ABC,abstractmethod


cur_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from event_class.event_class import event

class User(ABC):

    def __init__(self,name:str, surname:str):
        self.name=name
        self.surname=surname
        self.criteria={}

    def intersted_in(self,criteria: dict[str,Any])->None:
        '''
        here will be all criterions 
        the user has for the new tickets
        to be interested in them
        '''
        self.criteria= criteria
        

    @abstractmethod
    def notify(self,list_of_events:list[event]):
        pass


class User_Email(User):

    def __init__(self,name:str,surname:str, address:str):
        super().__init__(name,surname)
        self.address=address
    
    def notify(self,list_of_events:list[event]):
        intersting_events=list_of_events.copy()
        for crit in self.criteria.items():
            '''
            Do some checks for the interest
            '''
        if len(intersting_events)>0:
            print(f'Sending email to {self.name} {self.surname} at {self.address}')
        pass


class User_Phone(User):
    def __init__(self,name:str,surname:str, phone_number:str):
        super().__init__(name,surname)
        self.phone_number=phone_number

    def notify(self,list_of_events:list[event]):
        print(f'Sending an SMS to {self.name} {self.surname} at {self.phone_number}')
        pass
    
    

