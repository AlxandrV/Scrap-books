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
        return BeautifulSoup(page, 'html.parser')
    else:
        return r.status_code


"""
Function strip a string

string to strip
param @string

Return strip to string
return @string
"""
def strip_string(string):
    string = string.text
    return string.replace('\n', '').strip()



"""Extract categorys"""
url = 'http://books.toscrape.com/'
soup = scrap(url)
categorys = soup.find('ul', class_='nav nav-list').find('li').find_all('a')

category_name = []
book_url = []

"""Foreach category"""
for category in categorys:
    # Get category name
    category_str = strip_string(category)
    # category_str = category_str.replace('\n', '').strip()
    category_name.append(category_str)

    # Get url category
    url_category = url + category.get('href')
    url_category = url_category.replace('index.html', '')
    soup_category = scrap(url_category)

    # Get page number
    page = soup_category.find('li', class_='current')
    if page != None:
        page = strip_string(page)
        page = int(page[-2:].strip())

        """Foreach page"""
        i = 1
        while i <= page:
            soup_page = scrap(url_category + f'page-{i}.html')
            print(soup_page)
            i += 1





    # books = soup_category.find_all('div', class_="image_container")

    # """Foreach book"""
    # for book in books:
    #     book = book.find('a').get('href')
    #     book_url.append(book)

print(len(book_url))