import requests
from bs4 import BeautifulSoup

def check_ballet_tickets(url):
    """
    Sprawdza, czy dostępne są bilety na balet na stronie teatru.
    """
    try:
        # Ustawienie nagłówków, aby strona traktowała nas jak standardową przeglądarkę
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Sprawdź, czy wystąpił błąd HTTP

        soup = BeautifulSoup(response.content, 'html.parser')
        
        ballet_events = []
        # Znalezienie wszystkich wydarzeń w kalendarium
        # Struktura strony może się zmieniać, ten selektor jest przykładowy
        events = soup.find_all('div', class_='views-row') 

        for event in events:
            title_tag = event.find('h3', class_='twon-title')
            event_type_tag = event.find('div', class_='views-field-field-event-type')
            ticket_link = event.find('a', string="Kup bilet")
            
            if title_tag and event_type_tag and "Balet" in event_type_tag.get_text(strip=True):
                title = title_tag.get_text(strip=True)
                date_tag = event.find('div', class_='views-field-field-event-date-open')
                date = date_tag.get_text(strip=True) if date_tag else "Brak daty"
                
                status = "Brak linku do zakupu online"
                if ticket_link:
                    # Jeśli link "Kup bilet" istnieje, sprzedaż jest aktywna
                    status = f"Bilety Dostępne Online: {ticket_link['href']}"
                elif "SPEKTAKL ZAMKNIĘTY" in event.get_text(strip=True):
                     status = "Spektakl Zamknięty/Wyprzedany"

                ballet_events.append(f"{date} - {title}: {status}")

        return ballet_events

    except requests.exceptions.RequestException as e:
        return [f"Błąd podczas łączenia ze stroną: {e}"]
    except Exception as e:
        return [f"Wystąpił błąd parsowania: {e}"]

# Adres URL do kalendarium Teatru Wielkiego (polska wersja językowa)
url = "