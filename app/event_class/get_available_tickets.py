import requests
import re
import unicodedata
import os,sys
import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from check_link import check_link,NoTickets


def get_number_of_sections(link : str)->list[dict[str, str | int]]:
        '''
        This function extracts the number of
        sections that the venue is split into
        '''
        tag=link.split('?')[-1]
        url_for_layout = "https://butik.teatrwielki.pl/rezerwacja/numerowane.html"
        url_for_layout += "?"+tag
        url_for_layout += "&json=true&jsonType=wizualizacje"
        try:
            session=requests.Session()
            init_resp=session.get(url_for_layout)
            init_resp.raise_for_status()
            room_layout=[]
            for ent in init_resp.json().get('data'):
                room_layout.append(ent)
            
            return room_layout
        except requests.exceptions.HTTPError:
            print("Page is missing")

def get_ticket_num_in_sector(link:str)->int|None:
    '''
    Extracts the number of tickets in each sector of the venue
    '''
    session=requests.Session()
    init_resp=session.get(link)
    
    url_for_ticketer="https://butik.teatrwielki.pl/rezerwacja/miejsca-wolne.html" # location of the ticketing page
    try:
        '''
        construct the payload to pass to the ticketing page
        '''
        keys_ticketer=["wiz_id","wiz_idt","ter_id","ter_idt","cen_id"]
        payload={}
        for key_names in keys_ticketer:
            key_str='%s=.*?;'%key_names
            text=re.search(key_str, init_resp.text)
            val= re.sub('\'','',text.group().rstrip(';')).split('=')[-1]
            payload[key_names]=val
        repsonse=requests.post(url_for_ticketer,params=payload)
        repsonse.raise_for_status()
        num_of_seats=0
        for seat in repsonse.json().get('miejsca'):
            if seat['class'] != 'z' and seat['class'] != 'x':
                num_of_seats +=1
        return num_of_seats
    except requests.exceptions.HTTPError:
        print("Page is missing")
    

def get_available_tickets(date: datetime.datetime, link : str,  verbose:bool=False)->tuple[int,dict[str,int]]:
    '''
    Function returns the tickets to a certain event
    accepts the link to the event and returns a tuple
    with total number of free seats and
    a dict of free seats in sectors
    '''
    try:
        redirected_link=check_link(date,link,verbose)
        seat_dict={}
        layout = get_number_of_sections(redirected_link)
        total_ticket_num=0
        for sections in layout:
            sec_id=sections['id_wizualizacji']
            #new_link=re.sub('&wiz_id=\d{1,3}','&wiz_id=%s'%(sec_id),redirected_link)
            new_link=re.sub(r'&wiz_id=\d{1,3}','&wiz_id=%s'%(sec_id),redirected_link)
            ticket_num=get_ticket_num_in_sector(new_link)
            total_ticket_num += ticket_num
            #Trick to substitute the polish letters 
            # with standard english equivalents
            name_temp=unicodedata.normalize('NFKD',sections['nazwa_wizualizacji'])
            name_temp=name_temp.encode('ASCII','ignore').decode('ASCII')
            ########
            seat_dict[name_temp]= ticket_num
            if verbose:
                print("sector %i has %i tickets in %s"%(sec_id,ticket_num,sections['nazwa_wizualizacji']))
        if verbose:
            print(f'overall ticket number is {total_ticket_num}')
        
        return total_ticket_num,seat_dict

    except NoTickets: # special error imported from check link module
        return 0,{} # returns 0 (number of tickets) and an empty dict of seats


