
from abc import ABC, abstractmethod  
import os,sys
import datetime
from typing import Any
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(curr_dir))
from event_class.event_class import event
from create_ticket_database.user_class import User


def compare_two_dicts_of_shows(dict_of_shows: dict[tuple[str,str],dict[str,int]], \
                               dict_of_shows_ref: dict[tuple[str,str],dict[str,int]])->\
                               dict[tuple[str,str],bool]:
    '''
    Universal function comparing two dicts of shows
    and returning a dict with True if new tickets have pop-up for a given show
    '''
    new_ticket_dict={}
    for k,v in dict_of_shows.items(): #iterate over shows
        send_notification=False
        #skip unnceessary comparisons if there are no tickets
        if v['free seats total']==0: 
            continue

        if k in dict_of_shows_ref:# both DB have the same show -> compare the total of free seats dict
            
            #quick test if there is more tickets now then previusly
            if v['free seats total'] > dict_of_shows_ref[k]['free seats total']:
                send_notification=True

            elif v['free seats total'] == dict_of_shows_ref[k]['free seats total']:
                #compare sector-by=sector to not skip when free seats moved
                for sec_DB,sec_DB_ref in zip(v.items(),dict_of_shows_ref[k].items()):
                    if sec_DB[1] > sec_DB_ref[1]:
                        send_notification=True
                        break # no need to check for other
            else: 
                pass   #do nothing

        else: # new key = new show on the list so notify 
            send_notification=True
        
        new_ticket_dict[k]=send_notification
    return new_ticket_dict


## Here will be export of events to json/yml/xml database

class TicketDataBase(ABC):
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
        ->dict[tuple[str,str],bool] |None:
        '''
        This function compares two databases and exports
        a dict of boolian flags if more tickets are available
        now then previsly. 
        Useses compare two_dict function defined at the top
        Common method for any data base and used as starting
        point for their own update -> 
        NEED TO ADD REMOVAL OF OLD SHOWS !!!
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
               dict_of_new_tickets:dict[tuple[str,str],bool],
                 users_list: list[User],
                 dict_of_shows: dict[tuple[str,str],dict[str,int]]={})->bool:
        '''
        Some common method to notify people from mailing list of new tickets 
        By default don't need dict of shows, but for future
        when dict of shows will be passed to the notify function it will be
        needed
        '''
        if any(dict_of_new_tickets.values()):
            for subscribers in users_list:
                subscribers.notify(dict_of_new_tickets)
            print('\nAbout new tickets for: ')
            for k,v in dict_of_new_tickets.items():
                if v:
                    print(f'->{k}', end="")     
            print('\n')
            return True
        else:
            return False
        


import json
class TicketDBJSON(TicketDataBase):
    
    def exportDB(self, dict_of_shows : dict[tuple[str,str],dict[str,int]], out_f_name: str)->None:

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
        
        with open(out_f_name+'.json' , 'w') as f:
            json.dump(list_of_dicts,f,indent=4)
    
    def importDB(self,  f_name: str)-> dict[tuple[str,str],dict[str,int]]:
        with open(f_name+".json",'r') as f:
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
        ->dict[tuple[str,str],bool] | None:
        '''
        Overwrites the parent update 
        adds check if previous state DB exists
        and deciedes what to do 
        Retunrs the dict of show- available new tickets
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
    pass







    