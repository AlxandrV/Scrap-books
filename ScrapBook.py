from os import remove
import requests
from bs4 import BeautifulSoup
import csv


class Scrapbook:

    category_name = []
    book_url = []
    book_dicts = [] 
    url='http://books.toscrape.com/'

    def __init__(self):

        """Extract categorys"""
        soup = self._scrap(self.url)
        categorys = soup.find('ul', class_='nav nav-list').find('ul').find_all('a')

        """Foreach category"""
        for category in categorys[0:2]:

            soup_category = self._category_scrap(category)
            self._pagination(soup_category)



    def _scrap(self, url):
        """ Funtion scrap to url

        url to scrap
        param @string

        return content html
        return @Beautiful object """

        r = requests.get(url)

        if r.ok:
            page = r.content
            return BeautifulSoup(page, 'html.parser')
        else:
            return r.status_code


    def _strip_string(self, soup_string):
        """ Function strip a string

        string to strip
        param @Beautiful object

        Return strip to string
        return @string """

        string = soup_string.text
        return string.replace('\n', '').strip()


    def _category_scrap(self, tag_category):
        """ Function scrap category page

        Soup tag to scrap
        param @Beautiful object

        Return soup page and url
        return @array """
        # Get category name
        category_str = self._strip_string(tag_category)
        self.category_name.append(category_str)
        
        # Get url category
        url_category = self.url + tag_category.get('href')
        url_category = url_category.replace('index.html', '')
        return [self._scrap(url_category), url_category]


    def _book_scrap(self, array_category):
        """ Function scrap book in page and collect information

        Soup to category page
        param @Beautiful object """

        books = array_category[0].find_all('div', class_="image_container")

        """Foreach book"""
        for book in books:

            book_dictionnary = {}
            book_url = array_category[1] + book.find('a').get('href')
            book_dictionnary['product_page_url'] = book_url
            
            soup_book = self._scrap(book_url)
            product_information = soup_book.find('table', class_="table table-striped").find_all('td')
            # print(product_information)
            book_dictionnary['universal_product_code (upc)'] = self._strip_string(product_information[0])
            book_dictionnary['title'] = self._strip_string(soup_book.find('h1'))
            book_dictionnary['price_including_tax'] = self._strip_string(product_information[3])
            book_dictionnary['price_excluding_tax'] = self._strip_string(product_information[2])
            book_dictionnary['number_available'] = self._strip_string(product_information[5])
            book_dictionnary['product_description'] = self._strip_string(soup_book.find('div', class_="sub-header").find_next_sibling('p'))
            book_dictionnary['category'] = self.category_name[-1]
            book_dictionnary['review_rating'] = self._strip_string(product_information[6])
            book_dictionnary['image_url'] = book_url.replace('index.html', '') + soup_book.find('div', class_="item active").find('img').get('src')
            # print(book_dictionnary)

            self.book_dicts.append(book_dictionnary)



    def _pagination(self, array_category):
        """ Function scrap pagination

        Soup to category page and url
        param @array """

        self._book_scrap(array_category)
        quant_result = array_category[0].find('form', class_='form-horizontal').find_all('strong')

        if len(quant_result) > 1:

            # Rounded whole number
            tot_result = int(self._strip_string(quant_result[0]))
            filtr_number = int(self._strip_string(quant_result[-1]))
            number_pages = int(tot_result // filtr_number + (1 if tot_result % filtr_number > 0 else 0))

            # Foreach page
            for i in range(2, number_pages+1):

                soup = self._scrap(array_category[1] + f'page-{i}.html')
                self._book_scrap([soup, array_category[1]])

        self.convert_to_csv(self.book_dicts)

    def convert_to_csv(self, dictionnary):
        """ Function convert dictionnary to a CSV

        Dictionnary to convert
        param @dict """

        with open(f'{self.category_name[-1]}.csv', mode="w") as file_out:

            fieldnames = ['product_page_url','universal_product_code (upc)','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']
            result = csv.DictWriter(file_out, fieldnames=fieldnames)
            result.writeheader()
                # result = csv.writer(file_out)

            for row in dictionnary:
                result.writerow(row)

