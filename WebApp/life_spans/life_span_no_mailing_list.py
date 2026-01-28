
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor

import sys
from main_API import root_dir
sys.path.append(root_dir)
from app.create_ticket_database.data_base import TicketDBJSON
from ticket_DB_periodic_update.DB_periodic_update import do_DB_update # one of the background processes



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
