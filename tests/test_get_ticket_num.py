import pytest
import requests

import os, sys
curr_dir=os.path.dirname(os.path.abspath(__file__)) #
parent_dir = os.path.dirname(curr_dir) #get parent
sys.path.append(parent_dir)
from app.check_tickets.get_ticket_num import get_ticket_num


link="https://butik.teatrwielki.pl/rezerwacja/numerowane.html?ter_id=5219&ter_idt=55062d9bff871acec270d2cf48853062&extid=73073&wiz_id=26"

link_list=link.split('?')[-1].split('&')
print(link_list)

payload={
    "wiz_id": "26",
    "wiz_idt":"42619486f92ea73aa3d87b34e143544",
    "ter_id":"5219",
    "ter_idt":"55062d9bff871acec270d2cf48853062",
    "cen_id":"356"
}

print(get_ticket_num(payload))
