import pytest
import requests,re
import bs4

import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent
sys.path.append(parent_dir)
from app.check_tickets.get_ticket_num import get_ticket_num,get_number_of_sections,iterate_over_room_layout

link_new="https://butik.teatrwielki.pl/rezerwacja/numerowane.html?ter_id=5221&ter_idt=c786a44f3958219af47be498ce294949&extid=73075&wiz_id=26"
link_2="https://butik.teatrwielki.pl/rezerwacja/numerowane.html?ter_id=5302&ter_idt=25b701a821ca02e80ebfa9b077411133&extid=73066&wiz_id=0&id_strefy=&zniz=7"
link_3="https://butik.teatrwielki.pl/rezerwacja/numerowane.html?ter_id=5864&ter_idt=7a0bb7fdcb5ef326679793ff47225650&extid=74007&wiz_id=0&zniz=7"
link_5="https://butik.teatrwielki.pl/rezerwacja/numerowane.html?ter_id=5864&ter_idt=7a0bb7fdcb5ef326679793ff47225650&extid=74007&wiz_id=469"
for link in [link_new,link_2,link_3][-1::]:
    #print(get_ticket_num(link))
    iterate_over_room_layout(link_5)
