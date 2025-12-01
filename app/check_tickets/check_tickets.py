import bs4 as bs
import mechanicalsoup as ms
import datetime,re
import requests

import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent
sys.path.append(parent_dir)
from event_class.event_class import event


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
        
        evet_sec=subpage.find("div", {"class":"slider slider-3-dates content-box"}).find_all("li")
        # #access the slider menu with tickets and get all the events
        for event in evet_sec:
            temp_time=event.find('small').text.split()[-1]
            if(
                event.find('time',{'datetime':date_str})
                and temp_time==date_hour
                ):
                
                check_link=event.find('a')["href"]
                subpage_check=requests.get(check_link)
                #there is a redirection build-in
                #so one needs to check if the rediration
                #is to the error page, and not if the
                # target and opened page urls match
                error_link="%i&termtoscroll"%event_instance.time.year           
                avaiability_str=None
               
                if re.search(error_link, subpage_check.url):
                    avaiability_str="Brak biletów"
                    ticket_num=0
                else:
                    avaiability_str="Są bilety"
                    ticket_num=1
                    event_instance.update_ticket_num(ticket_num)

                if avaiability_str is not None:
                    if print_res:
                        print(event_instance.title, " o ", event_instance.time, "-> ", avaiability_str )
                    return ticket_num
                
                else:
                    print("Strange behavior @: ", subpage_check.url)
                
                
    except requests.exceptions.HTTPError as err:
        print("Błąd w dostępnie do strony z biletami dla tego wydarzenia")



def analize_availability(ballet_dict: dict[str, list[event]], base_url:str, print_info:bool=True)-> None:
    event_num=1
    for ballet_name in list(ballet_dict.keys()):
        for ev in ballet_dict[ballet_name]:
            check_for_tickets(base_url, ev,print_info)
            event_num+=1