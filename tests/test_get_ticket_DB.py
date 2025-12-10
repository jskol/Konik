import pytest
import requests,re
import bs4

import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent
sys.path.append(parent_dir)
from app.create_ticket_database.iterate_over_room_layout import iterate_over_room_layout_DB

import yaml
import unicodedata

link_5="https://butik.teatrwielki.pl/rezerwacja/numerowane.html?ter_id=5864&ter_idt=7a0bb7fdcb5ef326679793ff47225650&extid=74007&wiz_id=469"

if __name__=="__main__":
    dict_of_seats=iterate_over_room_layout_DB(link_5)
    print(dict_of_seats)
    yaml_out= yaml.dump(dict_of_seats)
    with open('test_DB.yml','x') as f:
        f.write(yaml_out)