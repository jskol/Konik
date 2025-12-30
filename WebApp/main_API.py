# use lifespan to have processes running in the background
#such as DB updates etc.
import asyncio
from ticket_DB_periodic_update.DB_periodic_update import do_DB_update # one of the background processes

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request,Form
from concurrent.futures import ThreadPoolExecutor

def create_lifespan( run_background_process :bool ):
    @asynccontextmanager
    async def lifespan(app : FastAPI):
        #Start updating the ticket DB
              
        if run_background_process:
            print("starting the DB update...")
            DB=TicketDBJSON()
            executor = ThreadPoolExecutor(max_workers=2)
            bg_task = asyncio.create_task(do_DB_update(DB,12,4*3600)) # This will run in the background 
            # In future also notification option will
            # be added to this part 
        else:
            print("No background process")
            
        yield # contiunue interaction with the webpage
        
        ## clean-up needed
        if run_background_process:
            bg_task.cancel()
            executor.shutdown(wait=True)
            await bg_task
    return lifespan
    
#Start the API
webapp_lifespan=create_lifespan(False)
webapp=FastAPI(lifespan=webapp_lifespan)

import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))

# Mount location of static data like pictures etc. ...
from fastapi.staticfiles import StaticFiles
webapp.mount("/static",
             StaticFiles(directory=os.path.join(curr_dir,"static")),
             name="static"
             )

#Mount the templates for subpages 
# All handled by Jinja2
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(
    directory=os.path.join(curr_dir,"page_templates")
    )


### HOME PAGE #####
# import list of show types
parent_dir=os.path.dirname(curr_dir)
sys.path.append(parent_dir)
from app.main import event_type_list
from fastapi.responses import HTMLResponse # import HTML respose

@webapp.get("/",response_class=HTMLResponse)
async def welcome_page(request: Request):
    return templates.TemplateResponse("home.html",
                                      {"request": request,
                                       "event_list": event_type_list
                                       })

### Redirect to ticketing subpages
### depending on the decission that the 
### user made
from fastapi.responses import RedirectResponse
@webapp.post("/pick_event")
async def handle_event_pick(request:Request,
                            event_num: int=Form(...)):
    #Przekierowanie do strony z biletami na dany rodzaj wydarzenia
    url_to_pass=request.url_for("print_tickets",event_num=event_num)
    return RedirectResponse(url=url_to_pass, status_code=303)


### Ticketing subpage
from tickets_helpers import fix_name,read_DB,create_calendar
# Import DataBase format
from app.create_ticket_database.data_base import TicketDBJSON
# Functionality for hangling the calndar option


@webapp.get("/tickets/{event_num}",response_class=HTMLResponse)
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


    