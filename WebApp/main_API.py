# use lifespan to have processes running in the background
#such as DB updates etc.
import asyncio
from ticket_DB_periodic_update.DB_periodic_update import do_DB_update # one of the background processes

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request,Form
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=2)
@asynccontextmanager
async def webapp_lifespan(app : FastAPI):
    #Start updating the ticket DB
    DB=TicketDBJSON()
    print("starting the DB update...")
    bg_task = asyncio.create_task(do_DB_update(DB,12,500)) # This will run in the background 
    # In future also notification option will
    # be added to this part 
    
    yield # contiunue interaction with the webpage
    
    ## clean-up needed
    bg_task.cancel()
    executor.shutdown(wait=True)
    await bg_task
    
#Start the API
webapp=FastAPI(lifespan=webapp_lifespan)
from fastapi.responses import HTMLResponse,RedirectResponse

# Mount location of static data like pictures etc.
from fastapi.staticfiles import StaticFiles
webapp.mount("/static",StaticFiles(directory="static"),name="static")

#Mount the templates for subpages
import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory=os.path.join(curr_dir,"page_templates"))

# import
# 1)list of show types
# 2) DataBase format
parent_dir=os.path.dirname(curr_dir)
sys.path.append(parent_dir)
from app.main import event_type_list
from app.create_ticket_database.data_base import TicketDBJSON


@webapp.get("/",response_class=HTMLResponse)
async def welcome_page(request: Request):
    return templates.TemplateResponse("home.html",
                                      {"request": request,
                                       "event_list": event_type_list
                                       })
@webapp.post("/pick_event")
async def handle_event_pick(event_num: int=Form(...)):
    #Przekierowanie do strony z biletami na dany rodzaj wydarzenia
    return RedirectResponse(url=f"/tickets/{event_num}", status_code=303)

from tickets_helpers import fix_name,read_DB

@webapp.get("/tickets/{event_num}",response_class=HTMLResponse)
async def print_tickets(request: Request,
                       event_num:int):
    event_name_str=fix_name(event_type_list[event_num])
    #Read the database
    DB=TicketDBJSON()
    event_dict,date_str=read_DB(DB,event_num)
    return templates.TemplateResponse("tickets.html",
                                      {"request": request,
                                       "event_type_name": event_name_str,
                                        "dict_of_events":event_dict,
                                        "last_modified":  date_str
                                       })


    