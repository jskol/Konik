from urllib.request import urlopen
import re

url = "http://olympus.realpython.org/profiles/aphrodite"

page=urlopen(url)
print(page)

html=page.read().decode("utf-8") #reads the content and trasfroms it from bytes to utf-8
print(html) #-> html olds the full html source code of the page
title_ind_start=html.find("<title>")+len("<title>") # holds in which line one can find <title>
title_ind_end=html.find("</title>") # holds in which line one can find <title>
title=html[title_ind_start:title_ind_end]
print(title)


new_url = "http://olympus.realpython.org/profiles/poseidon"
page=urlopen(new_url)
html=page.read().decode("utf-8")
print(html)

pattern="<title.*?>.*?</title.*?>"
match_res=re.search(pattern,html,re.IGNORECASE ) # gives a Match-object
print(match_res)
print(match_res.group())
new_title=re.sub("<.*?>","",match_res.group())
print("new title : %s "%new_title)

from bs4 import BeautifulSoup
soup = BeautifulSoup(html,"html.parser")
print(re.sub(r'\n+',r'\n',soup.get_text()))
pics=soup.find_all("img")
print("there is/are %i pic(s)"%len(pics))
for pic in pics:
    print(pic.name, " @ ",pic["src"])
