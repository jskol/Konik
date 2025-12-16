import datetime
import bs4 as bs
import os,sys

from dataclasses import dataclass,field

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from get_available_tickets import get_available_tickets

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web_page_details import page_details

@dataclass
class event:
    '''
    The main building block of the code
    a dataclass that holds the details of each event
    defined by :
    1) title
    2) location (venue)
    3) date
    4) link to its web page
    5) short description (teaser)
    6) number of free seats
    7) a dictionary holding information 
        on the number of free seats in each
        sector of the venue
    '''


    title:str
    location:str
    time: datetime.datetime
    link:str
    teaser: str| None = None
    free_seats: int =0
    seats_dict: dict[str,int]=field(default_factory=dict)
    
    def __init__(self, html_piece:bs.ResultSet):
        line=html_piece.find("a")
        self.link=line["href"]
        self.title=line.text
        self.location=html_piece.find("span",{"class":"hall"}).text
        self.time=html_piece.find("span",{"class":"hour"}).text
        # Extract the date from the link
        date=line["href"].split("/")[-2].split("_")
        self.time=datetime.datetime(
            year=int(date[0].split('-')[0]),
            month=int(date[0].split('-')[1]),
            day=int(date[0].split('-')[2]),
            hour=int(date[1].split('-')[0]),
            minute=int(date[1].split('-')[1])
            )
        teaser=html_piece.find("p",{"class":"teaser"})
        if teaser is not None:
            self.teaser=teaser.text

    def __repr__(self)->str:
        dni=["Pon","Wt","Śr","Czw", "Pt","Sb","Nd"]
        str_to_print= "Title: %s\n Location: %s \n Time: %s (%s)"%(self.title,self.location,self.time, dni[self.time.weekday()])
        if self.free_seats > 0:
            str_to_print += "\n Free seats: %i"%(self.free_seats)
        else:
            str_to_print += " No free seats available"
        return str_to_print

    def update_ticket_num(self)->None:
        print(f'Updating tickets for {self.title} on {self.time.strftime("%d/%m/%Y")}', end="")
        tickets_num,tickets_dict=get_available_tickets(self.time, self.link)
        self.free_seats=tickets_num
        self.seats_dict=tickets_dict
        print(f' -> {self.free_seats} seats left')
    def print_seats_dict(self)->None:
        for k,v in self.seats_dict.items():
            print(f'{k} has {v} seats')

    def export_as_dict(self)->dict[tuple[str,str],dict[str, int]]:
        '''
        Export event instance to a dict with:
        key - tuple of name and date
        value - dict of seats
        '''
        event_as_dict={}
        temp_key=(self.title,self.time.strftime("%d/%m/%Y %H:%M"))
        #create a dict with first key holding total number of free seats
        temp_val={'free seats total':self.free_seats}
        #and all pairs from the seats_dict 
        for k,v in self.seats_dict.items():
            temp_val[k]=v
        event_as_dict[temp_key]=temp_val

        return event_as_dict

    