import bs4 as bs
import mechanicalsoup as ms
import datetime,re
import requests

import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent
sys.path.append(parent_dir)
from event_class.event_class import event


def check_for_tickets( url_main:str, event_instance: event) -> int:
    date=event_instance.time
    date_str="%s-"%date.year + "{:0=2d}-".format(date.month)+"{:0=2d}".format(date.day)
    date_hour=date.strftime("%H:%M")
    url=url_main+event_instance.link
    try:
        page_request=requests.get(url)
        page_request.raise_for_status()
        page=bs.BeautifulSoup(page_request.content,'html.parser')
        
        evet_sec=page.find("div", {"class":"slider slider-3-dates content-box"}).find_all("li")
        # #access the slider menu with tickets and get all the events
        for event in evet_sec:
            temp_time=event.find('small').text.split()[-1]
            if(
                event.find('time',{'datetime':date_str})
                and temp_time==date_hour
                ):
                
                check_link=event.find('a')["href"]
                page_check=requests.get(check_link)
                error_link="%i&termtoscroll"%event_instance.time.year           
                avaiability_str="Brak biletów" if re.search(error_link, page_check.url) else "Są bilety"
                '''
                if re.search(error_link, page_check.url):
                    avaiability_str="Brak biletów"
                else:
                    avaiability_str="Są bilety"
                '''
                print(event_instance.title, " o ", event_instance.time, "-> ", avaiability_str )
    except requests.exceptions.HTTPError as err:
        print("Błąd w dostępnie do strony z biletami dla tego wydarzenia")

