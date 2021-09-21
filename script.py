import requests
from bs4 import BeautifulSoup


"""
Funtion scrap to url

url to scrap
param @url

return content html
return @Beautiful object
"""
def scrap(url):
    url = "http://books.toscrape.com/"
    r = requests.get(url)
    page = r.content

    return BeautifulSoup(page, "html.parser")


"""Category"""
url = "http://books.toscrape.com/"
soup = scrap(url)
nodes = soup.find("ul", class_="nav nav-list").find("li").find_all("a")

array = []
for node in nodes:
    node_str = node.text
    node_str = node_str.replace('\n', '')
    array.append(node_str.strip())

print(array)
