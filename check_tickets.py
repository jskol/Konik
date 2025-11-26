import bs4 as bs
import mechanicalsoup as ms
import datetime,re
import requests

from event_class import event


def check_for_tickets( url_main:str, event_instance: event) -> int:
    browser=ms.Browser()
    date=event_instance.time
    date_str="%s-"%date.year + "{:0=2d}-".format(date.month)+"%s"%date.day
    url=url_main+event_instance.link
    #print(url)
    page=browser.get(url).soup
    #print(page)
    evet_sec=page.find("div", {"class":"slider slider-3-dates content-box"}).find_all("li")
    #print(evet_sec)
    # #access the slider menu with tickets and get all the events
    for event in evet_sec:
        if(event.find('time',{'datetime':date_str})):
            check_link=event.find('a')["href"]
            page_check=requests.get(check_link)
            if check_link != page_check.url:
                print("Brak biletów")
            else: 
                print("Są bilety")        



