import bs4 as bs
import mechanicalsoup as ms
import datetime,re
import requests

import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent
sys.path.append(parent_dir)
from event_class.event_class import event
from check_tickets.get_ticket_num import iterate_over_room_layout

def check_for_tickets( url_main:str, event_instance: event, print_res:bool=True) -> int: 
    #This function will in future return the number of tikets left hence return int
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
            return 0
        else:
            if print_res:
                print("Są bilety na %s (%s)"%(event_instance.title,date_str))
                print(subpage_check.url)
            num_of_tickets=iterate_over_room_layout(subpage_check.url)
            return num_of_tickets
        
    except requests.exceptions.HTTPError as err:
        print("Błąd w dostępnie do strony z biletami dla tego wydarzenia")



def analize_availability(ballet_dict: dict[str, list[event]], base_url:str, print_info:bool=True)-> None:
    event_num=1
    for ballet_name in list(ballet_dict.keys()):
        for ev in ballet_dict[ballet_name]:
            check_for_tickets(base_url, ev,print_info)
            event_num+=1