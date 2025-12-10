

import unicodedata
import re 
import os,sys
from typing import Any
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(curr_dir))
from check_tickets.get_ticket_num import get_number_of_sections, get_ticket_num
from event_class.event_class import event

def iterate_over_room_layout_DB(link : str)->dict[str,int]:    
    resulting_dict={}
    layout = get_number_of_sections(link)
    total_ticket_num=0
    for sections in layout:
        sec_id=sections['id_wizualizacji']
        new_link=re.sub('&wiz_id=\d{1,3}','&wiz_id=%s'%(sec_id),link)
        ticket_num=get_ticket_num(new_link)
        total_ticket_num += ticket_num
        name_temp=unicodedata.normalize('NFKD',sections['nazwa_wizualizacji'])
        name_temp=name_temp.encode('ASCII','ignore').decode('ASCII')
        resulting_dict[name_temp]= ticket_num
    return resulting_dict


#TODO:START HERE!
def check_for_tickets_DB( url_main:str, event_instance: event, print_res:bool=True) -> None | dict[str, Any]: 
    date=event_instance.time
    date_str="%s-"%date.year + "{:0=2d}-".format(date.month)+"{:0=2d}".format(date.day)
    date_hour=date.strftime("%H:%M")
    url=url_main+event_instance.link
    try:
        subpage_request=requests.get(url)
        subpage_request.raise_for_status()
        subpage=bs.BeautifulSoup(subpage_request.content,'html.parser')  
        event_sec=subpage.find('time',{'datetime':date_str})
        
        link_to_check=event_sec.find_parent("li").find('a')['href']
        subpage_check=requests.get(link_to_check)
        #there is a redirection build-in the webpage
        #so one needs to check if the redirection
        #is to the error page, and not if the
        # target and opened page urls match
        error_link="%i&termtoscroll"%event_instance.time.year
        if re.search(error_link, subpage_check.url):
            if print_res:
                print("Brak biletów na %s (%s)"%(event_instance.title,date_str))
            return None
        else:
            if print_res:
                print(subpage_check.url)
            print("Bilety na %s (%s)"%(event_instance.title,date_str))  
            return_dict={}
            entry_name=(event.title, date_str)
            return_dict[entry_name]=iterate_over_room_layout_DB(subpage_check.url)
            return return_dict
        
    except requests.exceptions.HTTPError as err:
        print("Błąd w dostępnie do strony z biletami dla tego wydarzenia")



def shows_dict_to_DB(shows_dict: dict[str,list[event]], base_url:str)-> dict[dict[str,Any]]:
    DB_dict={}
    for event_name in list(shows_dict.keys()):
        event_list=shows_dict[event_name]
        updated_event_list=[event_it for event_it in event_list if check_for_tickets_DB(base_url,event_it,False)>0]
        if len(updated_event_list)>0:
            shows_dict.update({event_name:updated_event_list})
        else:
            shows_dict.pop(event_name)