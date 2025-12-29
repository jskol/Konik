import re



def fix_name(event_type_name:str)->str:
    '''
    Deal with the wonders of polish language (flexion)
    '''
    event_name_str=event_type_name
    event_name_str=re.sub('a$','', event_name_str)
    event_name_str += 'y'
    return event_name_str

import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(curr_dir)
sys.path.append(parent_dir)
from app.create_ticket_database.data_base import TicketDataBase
from tests.helper_functions import create_DB_if_missing
import pathlib,datetime


def read_DB(
    DB:TicketDataBase,
    event_num:int
    )->tuple[
        dict[tuple[str,str],dict[str,int]],
        str
        ]:
    '''
    Read the database and check the date 
    of its last modification
    return tuple of:
    1) event dict shows name and seats available
    2) string with date of the last modifiaction
    of the DB file
    '''
    curr_dir=os.path.dirname(os.path.abspath(__file__))
    parent_dir=os.path.dirname(curr_dir)
    DB_location=os.path.join(parent_dir,'Ticket_DB',f'DB_event_{event_num}')
    #create_DB_if_missing(DB,DB_location,num_of_months=2,event_type_in_list=event_num)
    #Get last update time
    path=pathlib.Path(DB_location+f'.{DB._extension}')
    time=path.stat().st_mtime
    date_str=datetime.datetime.fromtimestamp(time).strftime("%d/%m/%Y @ %H:%M")
    event_dict=DB.importDB(DB_location)
    return event_dict, date_str
    
import calendar
import datetime

def create_calendar(event_dict:dict[tuple[str,str],dict[str,int]])-> dict[str,str|int]:
    ''''
    Function creating a calendar from now till the final month in the database
    '''
    #get calendar
    cal = calendar.Calendar(firstweekday=0) # Week starts from monday
    
    # find current date and the date of 
    # the last show in the ticket DB
    # plus create a list of dates for
    # which there are tickets left
    
    current_date=datetime.datetime.now()
    last_event=current_date
    list_of_dates=[]
    for event in event_dict.keys():
        event_date=datetime.datetime.strptime(event[1],'%d/%m/%Y %H:%M')
        if any(event_dict[event].values()):
            list_of_dates.append(
                datetime.datetime(
                    event_date.year,
                    event_date.month, 
                    event_date.day
                    )
                )
        if event_date> last_event:
            last_event=event_date
    

    full_year = []
    temp_year=current_date.year
    temp_month=current_date.month
    
    while temp_year <= last_event.year:
        max_month=13 if temp_year < last_event.year else last_event.month 
        for month in range(temp_month, max_month):
            month_name = calendar.month_name[month]
            month_days =cal.monthdayscalendar(temp_year, month)
            # above creates a list of weeks with either 0 or the day number
            # depending on if it fits the mon-sun scheme
            #below we extend values of this this list
            # into tuples with the value and if this date is 
            # in the list of dates with an event with tickets
            
            new_month_days=[]
            for week in month_days:
                temp_week=[]
                for day in week:
                    if day ==0:
                        temp_week.append((0, False))
                    else:
                        temp_date=datetime.datetime.strptime(f'{day} {month} {temp_year}','%d %m %Y')
                        temp_week.append((day,bool(list_of_dates.count(temp_date))))
                new_month_days.append(temp_week)               
            
            
            full_year.append({
                "year": temp_year,
                "name": month_name,
                "weeks": new_month_days
            })
        temp_year+=1
        temp_month=1
        
    return full_year
        
    