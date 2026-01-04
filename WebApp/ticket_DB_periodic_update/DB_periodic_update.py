import os,sys

curr_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(curr_dir)
sys.path.append(os.path.dirname(parent_dir))
sys.path.append(parent_dir)
#Update bazy danych w tle co 24h
from app.event_dict.gen_dict import gen_event_dict
from app.event_dict.update_dict import update_shows_dict
from app.event_dict.export_event_dict import export_dict
from app.create_ticket_database.data_base import TicketDataBase
from app.main import event_type_list
import datetime
import asyncio,shutil
from HF_download import upload_to_hf

async def do_DB_update(
    DB_type: TicketDataBase,
    months_in_advance:int,
    wait_time:int =60*60*24 #by default for a day
)->None:
    '''
    This function runs in the background
    and checks available tickets 
    for "monts_in_advance" monts in the future
    and does it every wait_time to do it again
    '''
    curr_dir=os.path.dirname(os.path.abspath(__file__))
    root_dir=os.path.dirname(os.path.dirname(curr_dir))
    while True:
        curr_date=datetime.datetime.now()
        date_str=curr_date.strftime("%d/%m/%Y %H:%M:%S")
        print(f'Ruszam z aktualizacją {date_str}')
        for event_it, event_type in enumerate(event_type_list):
            DB_loc=os.path.join(root_dir,'Ticket_DB',f'DB_event_{event_it}')
            # generate a dict of plays 12 months in advance
            event_dict=gen_event_dict(months_in_advance,event_type,False)
           
            # Nice trick to run asynchronously
            # run a function that returns None
            # in this case in-place changes to
            # an event dict
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None,update_shows_dict,event_dict)
             
            final_dict=export_dict(event_dict)
            #Make a legacy version
            src=DB_loc+f'.{DB_type._extension}'
            src_copy=DB_loc+f'_OLD.{DB_type._extension}'
            if os.path.exists(src):
                curr_date=datetime.datetime.now()
                date_str=curr_date.strftime("%d/%m/%Y %H:%M:%S")
                print(f"Robię kopię DB {src}->{src_copy} o {date_str}")
                try:
                    shutil.copyfile(
                        src,
                        src_copy
                    )
                except FileNotFoundError:
                    print(f'Nie powiodło się tworzenie {src_copy}')
                    
            # Do a two step swap of the DB
            DB_type.exportDB(final_dict,DB_loc)
            upload_to_hf_flag=bool(int(os.getenv("UPLOAD_TO_HF")))
            if upload_to_hf_flag:
                upload_to_hf(src)
        print("Biletowa baza danych jest aktualna")
        
        await asyncio.sleep(wait_time)