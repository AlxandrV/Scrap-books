import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"
r = requests.get(url)
page = r.content

soup = BeautifulSoup(page, "html.parser")

nodes = soup.find("ul", class_="nav nav-list").find("li").find_all("a")

# print(nodes.string)
array = []
for node in nodes:
    node_str = node.text
    node_str = node_str.replace('\n', '')
    array.append(node_str.strip())

print(array)