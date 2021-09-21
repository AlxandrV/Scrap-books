import requests
from bs4 import BeautifulSoup

"""
Funtion scrap to url

url to scrap
param @url

query to find in content
param @q_find

return @array
"""
def scrap(url, q_find):
    r = requests.get(url)
    page = r.content

    soup = BeautifulSoup(page, "html.parser")

    nodes = q_find

    array = []
    for node in nodes:
        node_str = node.text
        node_str = node_str.replace('\n', '')
        array.append(node_str.strip())

    return array

"""Category"""
url = "http://books.toscrape.com/"
query = soup.find("ul", class_="nav nav-list").find("li").find_all("a")
categorys = scrap(url, query)

print(categorys)