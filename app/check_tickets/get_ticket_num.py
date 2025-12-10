import requests
import re
def get_ticket_num(link:str)->int:
    session=requests.Session()
    init_resp=session.get(link)
    #if init_resp.url != link:
    #    raise Exception("Page was redirected")
    
    url_for_ticketer="https://butik.teatrwielki.pl/rezerwacja/miejsca-wolne.html"
    try:
        '''
        construct the payload
        '''
        keys_ticketer=["wiz_id","wiz_idt","ter_id","ter_idt","cen_id"]
        payload={}
        for key_names in keys_ticketer:
            key_str='%s=.*?;'%key_names
            text=re.search(key_str, init_resp.text)
            val= re.sub('\'','',text.group().rstrip(';')).split('=')[-1]
            payload[key_names]=val
        repsonse=requests.post(url_for_ticketer,params=payload)
        repsonse.raise_for_status()
        num_of_seats=0
        for seat in repsonse.json().get('miejsca'):
            if seat['class'] != 'z' and seat['class'] != 'x':
                num_of_seats +=1
        return num_of_seats
    except requests.exceptions.HTTPError:
        print("Page is missing")
    


def get_number_of_sections(link : str)->list[dict[str, str | int]]:
        tag=link.split('?')[-1]
        url_for_layout = "https://butik.teatrwielki.pl/rezerwacja/numerowane.html"
        url_for_layout += "?"+tag
        url_for_layout += "&json=true&jsonType=wizualizacje"
        try:
            session=requests.Session()
            init_resp=session.get(url_for_layout)
            init_resp.raise_for_status()
            room_layout=[]
            for ent in init_resp.json().get('data'):
                room_layout.append(ent)
            
            return room_layout
        except requests.exceptions.HTTPError:
            print("Page is missing")



def iterate_over_room_layout(link : str)->int:
    layout = get_number_of_sections(link)
    total_ticket_num=0
    for sections in layout:
        sec_id=sections['id_wizualizacji']
        new_link=re.sub('&wiz_id=\d{1,3}','&wiz_id=%s'%(sec_id),link)
        ticket_num=get_ticket_num(new_link)
        total_ticket_num += ticket_num
        print("sector %i has %i tickets in %s"%(sec_id,ticket_num,sections['nazwa_wizualizacji']))
    print(total_ticket_num)
    return total_ticket_num



