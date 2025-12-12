from dataclasses import dataclass
'''
Now this is a singleton implementation
'''

@dataclass
class web_page:
    _instance=None
    base_url :str= "https://teatrwielki.pl"

    def __new__(self):
        if self._instance is None:
            web_page._instance=super().__new__(web_page)
        
        return self._instance
    
    def update_base_url(self, new_url:str) -> None:
        self.base_url=new_url
        

page_details=web_page() # Its a singleton