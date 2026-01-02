from huggingface_hub import HfApi
from os import environ,path

def upload_to_hf(local_file):
    token = environ.get("HF_TOKEN")
    if not token:
        print("Błąd: Brak HF_TOKEN w Secretach!")
        return

    HF_api = HfApi()
    # Tutaj wpisz swoją nazwę użytkownika i nazwę Space
    repo_id = "jskol87/Konik" 
    
    print(f"Wysyłam {local_file} do {repo_id}...")
    try:
        response=HF_api.upload_file(
            path_or_fileobj=local_file,
            path_in_repo=f'Ticket_DB/{path.basename(local_file)}', # repo-path always from root
            repo_id=repo_id,
            repo_type="space",
            token=token
        )
        print(f"Wysłano pomyślnie na {response}!")
    except Exception as e:
        print(f"Błąd podaczas wysyłania: {e}")