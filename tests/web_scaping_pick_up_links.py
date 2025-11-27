import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


address="http://olympus.realpython.org/profiles"
html=urlopen(address).read().decode("utf-8")
#print(html)
soup=BeautifulSoup(html,"html.parser")
print(type(soup))
links=soup.find_all("a")
base_url="/".join(address.split("/")[:-1])
for link in links:
    print(base_url+link["href"])


