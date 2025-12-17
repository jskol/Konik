import pytest
import os,sys
cur_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(cur_dir))

from app.create_ticket_database.data_base import TicketDBJSON
DB=TicketDBJSON()


if __name__=="__main__":
    read_DB=DB.importDB('DB_1_OLD')
    print(read_DB)
    print(DB.update(read_DB,'DB_1')) #Do with caution it overwrites the data
    print(read_DB)