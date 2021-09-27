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


"""
Function scrap category page

Soup tag to scrap
param @tag_category

Return soup page
return @scrap(url_category)
"""
def category_scrap(tag_category):
    # Get category name
    category_str = strip_string(tag_category)
    category_name.append(category_str)
    
    # Get url category
    url_category = url + tag_category.get('href')
    url_category = url_category.replace('index.html', '')
    return scrap(url_category)


"""Extract categorys"""
url = 'http://books.toscrape.com/'
soup = scrap(url)
categorys = soup.find('ul', class_='nav nav-list').find('ul').find_all('a')

category_name = []
book_url = []

# 17 pour test pagination
soup_category = category_scrap(categorys[17])
quant_result = soup_category.find('form', class_='form-horizontal').find_all('strong')

if len(quant_result) > 1:

    # Rounded whole number
    tot_result = int(strip_string(quant_result[0]))
    filtr_number = int(strip_string(quant_result[-1]))
    number_pages = int(tot_result // filtr_number + (1 if tot_result % filtr_number > 0 else 0))
    print(number_pages)

"""Foreach category"""
# for category in categorys:

#     soup_category = category_scrap(category)

#     # Get page number
#     page = soup_category.find()
#     print(soup_category)


# print(48 // 20 + (1 if 48 % 20 > 0 else 0))

    # books = soup_category.find_all('div', class_="image_container")

    # """Foreach book"""
    # for book in books:
    #     book = book.find('a').get('href')
    #     book_url.append(book)

# print(len(book_url))