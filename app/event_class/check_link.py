import bs4 as bs
import mechanicalsoup as ms
import datetime,re
import requests


import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web_page_details import page_details

class NoTickets(Exception):
    """
    Custom error raised when there is no tickets 
    available for the show
    """
    def __init__(self, *args):
        super().__init__(*args)



def check_link( date : datetime.datetime, link:str, print_res:bool=True) -> str: 
    '''
    Funcja sprawdzająca przekierowanie linku do wydarzenia
    '''
    url_main=page_details.base_url
    date_str="%s-"%date.year + "{:0=2d}-".format(date.month)+"{:0=2d}".format(date.day)
    url=url_main+link
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
        #error_link="%i&termtoscroll"%date.year

        error_link="%i&termtoscroll"%date.year
        if re.search(error_link, subpage_check.url) or subpage_check.url == "https://butik.teatrwielki.pl/":
            raise NoTickets("Brak bietów na to wydarzanie")
        else:
            return subpage_check.url
        
    except requests.exceptions.HTTPError as err:
        print("Błąd w dostępnie do strony z biletami dla tego wydarzenia")

