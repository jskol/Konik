from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse

router=APIRouter(
    prefix="/tickets",
    tags=["Ticketing Subpage"]
)

# Import my logic
import sys,os
webapp_parent_dir=os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
sys.path.append(webapp_parent_dir)
from tickets_helpers import fix_name,read_DB,create_calendar
from main_API import root_dir
from main_API import templates # Connect to the webpage templates

sys.path.append(root_dir)
from app.main import event_type_list
from app.create_ticket_database.data_base import TicketDBJSON


@router.get("/{event_num}",response_class=HTMLResponse)
async def print_tickets(request: Request,
                       event_num:int):
    event_name_str=fix_name(event_type_list[event_num])
    #Read the database
    DB=TicketDBJSON()
    event_dict,date_str=read_DB(DB,event_num)
    calendar_dict=create_calendar(event_dict)
    # Create a dict to pass to the webpage
    new_event_dict={}
    for event,seats in list(event_dict.items()):
        if any(seats.values()):
            temp_dict={ 'wolne miejsca' if k=='free seats total' else k : v for k,v in seats.items() }
            new_event_dict[event]=temp_dict
    

    
    return templates.TemplateResponse("tickets.html",
                                      {"request": request,
                                       "event_type_name": event_name_str,
                                        "dict_of_events":new_event_dict,
                                        "last_modified":  date_str,
                                        "calendar_dict": calendar_dict
                                       })
