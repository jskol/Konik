
from abc import ABC, abstractmethod  
import os,sys
import datetime
from typing import Any
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(curr_dir))
from event_class.event_class import event
from create_ticket_database.user_class import User

# Helper function for comparing two data bases in form of a dicts
def compare_two_dicts_of_shows(dict_of_shows: dict[tuple[str,str],dict[str,int]], \
                               dict_of_shows_ref: dict[tuple[str,str],dict[str,int]])->\
                               dict[tuple[str,str],dict[str,int]]:
    '''
    Universal function comparing two dicts of shows
    and returning a dict with location of the new tickets
    '''
    new_ticket_dict={}
    for k,v in dict_of_shows.items(): #iterate over shows
        #skip unnceessary comparisons if there are no tickets
        # just pass the basic dict (v) with free seast total=0
        if v['free seats total']==0: 
            temp_seating_dict=v

        else:# There is non-zero tickets for k-event in the most recent DB
            if k in dict_of_shows_ref.keys():# both DB have the same show -> compare the total of free seats dict
                print("Comparing two entries of ", k)
                temp_seating_dict={'free seats total':0}
                new_seats_total=0
                for sector_DB in list(v.items())[1:]: # trick to jump over the first item
                    try:
                        sector_DB_ref=dict_of_shows_ref[k]
                        new_seats=max(sector_DB[1]-sector_DB_ref[sector_DB[0]],0)

                    except KeyError:
                        new_seats=sector_DB[1]

                    temp_seating_dict[sector_DB[0]]=new_seats                        
                    new_seats_total+= new_seats
                #update the total number of free seats    
                temp_seating_dict['free seats total']=new_seats_total

            else: # if k is not int DB_ref pass all tickets there are in DB
                temp_seating_dict=v      

        new_ticket_dict[k]=temp_seating_dict

    return new_ticket_dict


## Here will be export of events to json/yml/xml database

class TicketDataBase(ABC):
    def __init__(self):
        self._extension=None

    @abstractmethod
    def exportDB(self, dict_of_shows: dict[tuple[str,str],dict[str,int]], out_f_name: str)->None:
        '''
        This function will export a dict contating information about the shows and tickets
        to a given type of datastorage and save it in out_f_name file, 
        NO CHECK IF FILE (ALREADY) EXISTS ALREADY -> on purpouse becuase this function will be used in update
        '''
        pass

    @abstractmethod
    def importDB(self,  f_name: str)-> dict[tuple[str,str],dict[str,int]]:
        '''
        Read database from a file and recat it
        back to a python dict with tuple as key
        '''
        pass

    def update(self,\
               dict_of_shows : dict[tuple[str,str],dict[str,int]], \
               ref_DB : dict[tuple[str,str],dict[str,int]])\
        ->dict[tuple[str,str],dict[str,int]] |None:
        '''
        This function compares two databases and exports
        a dict of boolian flags if more tickets are available
        now then previsly. 
        Useses compare two_dict function defined at the top
        Common method for any data base and used as starting
        point for their own update 
        '''
        dict_of_new_tickets=compare_two_dicts_of_shows(dict_of_shows,ref_DB) 

        # Remove outdated shows (for sanity of the DB)
        curr_date=datetime.datetime.now()
        for key_tup in list(dict_of_new_tickets.keys()):
            event_time=datetime.datetime.strptime(key_tup[1], '%d/%m/%Y %H:%M')
            if event_time - curr_date < datetime.timedelta(0):
                 dict_of_new_tickets.pop(key_tup)
        return dict_of_new_tickets


    def notify(self, 
               dict_of_new_tickets:dict[tuple[str,str],dict[str,int]],
                users_list: list[User]
                )->bool:
        '''
        Some common method to notify people from mailing list of new tickets 
        By default don't need dict of shows, but for future
        when dict of shows will be passed to the notify function it will be
        needed
        '''
        new_tickets={k:v for k,v in dict_of_new_tickets.items() if any(v.values())}
        if len(new_tickets): # There are tickets to be notify about
            for subscribers in users_list:
                subscribers.notify(dict_of_new_tickets)
            print('\nAbout new tickets for: ')
            for k,layout in new_tickets.items():
                print(f'->{k} in :\n\t', end="")
                for name, tickets in layout.items():
                    if tickets>0:
                        print(f'{name} - {tickets}')
            print('\n')
            return True
        else:
            return False
        
        


import json
class TicketDBJSON(TicketDataBase):
    def __init__(self):
        super().__init__()
        self._extension="json"


    def exportDB(self, dict_of_shows : dict[tuple[str,str],dict[str,int]], out_f_name: str)->None:
        '''
        Exports a dict of shows with seats
        into a proper file with extenstion
        automatically added->do not pass it
        inot the out_f_name
        '''
        list_of_dicts=[]
        #reacast to a list of dicts
        # JSON does not allow for tuple keys
        
        curr_date=datetime.datetime.now()
        for k,v in dict_of_shows.items():
            
            #Additional step to skip some events that passed
            #but did not got cought beforehand
            event_time=datetime.datetime.strptime(k[1], '%d/%m/%Y %H:%M')
            if event_time - curr_date < datetime.timedelta(0):
                continue

            temp_dict={'Title': k[0] , 'Date': k[1]}
            for k_1,v_1 in v.items():
                temp_dict[k_1]=v_1
            list_of_dicts.append(temp_dict)
        
        with open(out_f_name+f'.{self._extension}' , 'w') as f:
            json.dump(list_of_dicts,f,indent=4)
    
    def importDB(self,  f_name: str)-> dict[tuple[str,str],dict[str,int]]:
        '''
        Imports DB from f_name and transforms it
        back to the dict of tuple of (show name, date)
        and keys being dicts of seats,
        The extension is read from the property of the class
        so do not pass it in f_name
        '''

        with open(f_name+f'.{self._extension}','r') as f:
            legacy_DB=json.load(f)
        # Recast back to a dictonary wit tuple key
        legacy_DB_dict={}
        for entry in legacy_DB:
            key_tuple=(entry.pop('Title'),entry.pop('Date'))
            legacy_DB_dict[key_tuple]= entry
        return legacy_DB_dict

    def update(self, 
               dict_of_shows: dict[tuple[str,str],dict[str,int]],
               out_f_name :str,
               )\
        ->dict[tuple[str,str],dict[str,int]] | None:
        '''
        -> Overwrites the parent update !!!!
        -> adds check if previous state DB exists
            and if it does not then just exports the DB 
        Returns the dict of show- available new tickets
        '''
        try:
            ref_DB= self.importDB(out_f_name)
            dict_of_new_tickets = super().update(dict_of_shows, ref_DB)
            self.exportDB(dict_of_shows, out_f_name)
            return dict_of_new_tickets
        
        except FileNotFoundError: #if file does not exist just print the dict
            print("No history")
            self.exportDB(dict_of_shows,out_f_name)


class TicketDBXML(TicketDataBase):
    def __init__(self):
        super().__init__()
        self._extension="xml"

    pass







    