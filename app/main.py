
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
event_type_list=[
    "Balet","Opera"
]

from event_dict.gen_dict import gen_event_dict
from event_dict.update_dict import update_shows_dict
from event_dict.export_event_dict import export_dict

if __name__=="__main__":
    print("Czesc ! \n\
           Jaki typ przedstawienia cię interesuje?")
    for it, name in enumerate(event_type_list):
        print( f'{it} -> {name}')
    # Read in the event type
    event=None
    while not event:
        try:
            event=event_type_list[int(input("Ktore wybierasz?"))]
        except :
            print(f'Mozliwe tylko liczyby 0-{len(event_type_list)-1}->Sprobuj jeszcze raz')
    months=None
    while not months:
        try:
            months=int(input("Na ile miesiecy w przod wsprawdzic?") )
            if months<1:
                print("Mozliwe tylko dodatnie liczby >=1, Sprobuj jeszcze raz")
                months=None
        except:
            print(f'Mozliwe tylko liczyby -> Sprobuj jeszcze raz')
            
    event_dict=gen_event_dict(months,event,False) # generate a dict of plays and be verbose
    update_shows_dict(event_dict)
    final_dict=export_dict(event_dict)

    for k,v in final_dict.items():
        if v['free seats total'] >0:
            print(f'{k[0]} @ {k[1]}')
            for v_key,v_val in v.items():
                print(f'\t{v_key} : {v_val}')

            




