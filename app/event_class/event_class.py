import datetime
import bs4 as bs
from dataclasses import dataclass

@dataclass
class event:
    title:str
    location:str
    time: datetime.datetime
    link:str
    teaser: str| None = None
    free_seats: int =0
    
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
        return str_to_print

    def update_ticket_num(self,tickets_left:int)->None:
        self.free_seats=tickets_left