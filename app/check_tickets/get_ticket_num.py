import requests


def get_ticket_num(payload: dict[str,str])-> int:
    url_for_ticketer="https://butik.teatrwielki.pl/rezerwacja/miejsca-wolne.html"
    try:

        repsonse=requests.post(url_for_ticketer,params=payload)
        repsonse.raise_for_status()
        #print(repsonse.json().get('miejsca'))
        num_of_seats=0
        for seat in repsonse.json().get('miejsca'):
            if seat['class']!= 'z' and seat['class'] != 'x':
                #print(seat)
                num_of_seats +=1
        return num_of_seats
    except requests.exceptions.HTTPError:
        print("Page is missing")
    
