import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

import mechanicalsoup
browser=mechanicalsoup.Browser()

url = "http://olympus.realpython.org/login"
page = browser.get(url)
assert page.status_code==200
soup=page.soup
forms=soup.select("form")[0] # "[0]" because there is only one form and we pick it

forms.select("input")[0]["value"]="zeus"
forms.select("input")[1]["value"]="ThunderDude"

profiles_page = browser.submit(forms, page.url)
print(profiles_page.url)

