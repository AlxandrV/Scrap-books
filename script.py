import requests
from bs4 import BeautifulSoup


"""
Funtion scrap to url

url to scrap
param @string

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
param @Beautiful object

Return strip to string
return @string
"""
def strip_string(string):
    string = string.text
    return string.replace('\n', '').strip()


"""
Function scrap category page

Soup tag to scrap
param @Beautiful object

Return soup page and url
return @array
"""
def category_scrap(tag_category):
    # Get category name
    category_str = strip_string(tag_category)
    category_name.append(category_str)
    
    # Get url category
    url_category = url + tag_category.get('href')
    url_category = url_category.replace('index.html', '')
    return [scrap(url_category), url_category]


"""
Function scrap book in page

Soup to category page
param @Beautiful object
"""
def book_scrap(array_category):
    books = array_category[0].find_all('div', class_="image_container")

    """Foreach book"""
    for book in books:
        book_url = array_category[1] + book.find('a').get('href')
        book_dict['product_page_url'].append(book_url)
        
        soup_book = scrap(book_url)
        product_information = soup_book.find('table', class_="table table-striped").find_all('td')
        # print(product_information)
        book_dict['universal_product_code (upc)'].append(strip_string(product_information[0]))
        book_dict['title'].append(strip_string(soup_book.find('h1')))
        book_dict['price_including_tax'].append(strip_string(product_information[3]))
        book_dict['price_excluding_tax'].append(strip_string(product_information[2]))
        book_dict['number_available'].append(strip_string(product_information[5]))
        book_dict['product_description'].append(strip_string(soup_book.find('div', class_="sub-header").find_next_sibling('p')))
        book_dict['category'].append(category_name[-1])
        book_dict['review_rating'].append(strip_string(product_information[6]))
        book_dict['image_url'].append(book_url.replace('index.html', '') + soup_book.find('div', class_="item active").find('img').get('src'))
        # print(book_dict['image_url'])



"""
Function scrap pagination

Soup to category page and url
param @array
"""
def pagination(array_category):
    book_scrap(array_category)
    quant_result = array_category[0].find('form', class_='form-horizontal').find_all('strong')

    if len(quant_result) > 1:

        # Rounded whole number
        tot_result = int(strip_string(quant_result[0]))
        filtr_number = int(strip_string(quant_result[-1]))
        number_pages = int(tot_result // filtr_number + (1 if tot_result % filtr_number > 0 else 0))

        # Foreach page
        for i in range(2, number_pages+1):

            soup = scrap(array_category[1] + f'page-{i}.html')
            book_scrap([soup, array_category[1]])



"""Extract categorys"""
url = 'http://books.toscrape.com/'
soup = scrap(url)
categorys = soup.find('ul', class_='nav nav-list').find('ul').find_all('a')

category_name = []
book_url = []
book_dict = {
    'product_page_url':[],
    'universal_product_code (upc)': [],
    'title': [],
    'price_including_tax': [],
    'price_excluding_tax': [],
    'number_available': [],
    'product_description': [],
    'category': [],
    'review_rating': [],
    'image_url': []
}

# 17 for pagination, 5 for not pagination
soup_category = category_scrap(categorys[5])
pagination(soup_category)

# """Foreach category"""
# for category in categorys:

#     soup_category = category_scrap(category)
#     pagination(soup_category)


print(book_dict['category'])