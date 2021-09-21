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
    r = requests.get(url)

    if r.ok:
        page = r.content
        return BeautifulSoup(page, "html.parser")
    else:
        return r.status_code


"""Extract categorys"""
url = "http://books.toscrape.com/"
soup = scrap(url)
categorys = soup.find("ul", class_="nav nav-list").find("li").find_all("a")

category_name = []
book_url = []

"""Foreach category"""
for category in categorys:
    category_str = category.text
    category_str = category_str.replace('\n', '').strip()
    category_name.append(category_str)

    # Get url category
    url_category = url + category.get('href')
    url_category = url_category.replace('index.html', '')
    soup_category = scrap(url_category)
    books = soup_category.find_all('div', class_="image_container")

    """Foreach book"""
    for book in books:
        book = book.find('a').get('href')
        book_url.append(book)

print(len(book_url))