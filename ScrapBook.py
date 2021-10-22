import os
import requests
from bs4 import BeautifulSoup
import csv


class Scrapbook:

    _category_name = []
    _book_dicts = [] 
    _url='http://books.toscrape.com/'

    def __init__(self):

        """Extract categorys"""
        soup = self._scrap(self._url)
        categorys = soup[0].find('ul', class_='nav nav-list').find('ul').find_all('a')

        """Foreach category"""
        for category in categorys:

            soup_category = self._category_scrap(category)
            self._pagination(soup_category)



    def _scrap(self, url):
        """ Funtion scrap to url """
        """ return @array Soup content and url """

        r = requests.get(url)

        if r.ok:
            page = r.content
            return [BeautifulSoup(page, 'html.parser', from_encoding="utf-8"), r.url]
        else:
            return r.status_code


    def _strip_string(self, soup_string):
        """ Function strip a string """
        """ return @string """

        string = soup_string.text
        return string.replace('\n', '').strip()


    def _category_scrap(self, tag_category):
        """ Function scrap category page """
        """ return @array Soup content and url """

        # Get category name
        category_str = self._strip_string(tag_category)
        self._category_name.append(category_str)
        
        # Get url category
        url_category = self._url + tag_category.get('href')
        url_category = url_category.replace('index.html', '')
        return self._scrap(url_category)


    def _book_scrap(self, soup_category):
        """ Function scrap book in page and collect information """

        # Get tag for all book in page
        books = soup_category[0].find_all('div', class_="image_container")

        """Foreach book"""
        for book in books:

            # Containing for all information of a book
            book_dictionnary = {}

            # Get content HTML of a book
            book_url = soup_category[1] + book.find('a').get('href')
            soup_book = self._scrap(book_url)

            # Collected all information of a book in dictionnary
            book_dictionnary['product_page_url'] = soup_book[1]
            product_information = soup_book[0].find('table', class_="table table-striped").find_all('td')
            book_dictionnary['universal_product_code (upc)'] = self._strip_string(product_information[0])
            book_dictionnary['title'] = self._strip_string(soup_book[0].find('h1'))
            book_dictionnary['price_including_tax'] = self._strip_string(product_information[3])
            book_dictionnary['price_excluding_tax'] = self._strip_string(product_information[2])
            book_dictionnary['number_available'] = self._strip_string(product_information[5])
            if soup_book[0].find('div', class_="sub-header").find_next_sibling('p'):
                book_dictionnary['product_description'] = self._strip_string(soup_book[0].find('div', class_="sub-header").find_next_sibling('p'))
            book_dictionnary['category'] = self._category_name[-1]
            book_dictionnary['review_rating'] = self._strip_string(product_information[6])
            img_url = self._file_image(book_dictionnary['title'], book_url.replace('index.html', '') + soup_book[0].find('div', class_="item active").find('img').get('src'))
            book_dictionnary['image_url'] = img_url

            self._book_dicts.append(book_dictionnary)


    def _file_image(self, title, url):
        """ Function write file image in media directory """
        """ return @string """

        # print(url)
        current_dir = os.getcwd()
        files_dir = '/media'
        if os.path.exists(current_dir + files_dir) == False:
            os.mkdir(current_dir + files_dir)

        title = title.replace(' ', '_').replace(':', '').replace('/', '_').replace('\\', '_').replace('"', '').replace('*', '').replace('.', '').replace('?', '').replace('\'', '')
        with open(f'{current_dir + files_dir}/{title}.jpg', mode="wb") as file_img:
            response = requests.get(url)
            file_img.write(response.content)

        return response.url


    def _pagination(self, soup_category):
        """ Function scrap pagination """

        # print(len(soup_category))
        self._book_scrap(soup_category)
        quant_result = soup_category[0].find('form', class_='form-horizontal').find_all('strong')

        if len(quant_result) > 1:

            # Rounded whole number
            tot_result = int(self._strip_string(quant_result[0]))
            filtr_number = int(self._strip_string(quant_result[-1]))
            number_pages = int(tot_result // filtr_number + (1 if tot_result % filtr_number > 0 else 0))

            # Foreach page
            for i in range(2, number_pages+1):

                soup = self._scrap(soup_category[1] + f'page-{i}.html')
                soup[1] = soup[1].replace(f'page-{i}.html', '')
                self._book_scrap(soup)

        self.convert_to_csv()

    def convert_to_csv(self):
        """ Function convert dictionnary to a CSV """

        current_dir = os.getcwd()
        files_dir = '/files_csv'
        if os.path.exists(current_dir + files_dir) == False:
            os.mkdir(current_dir + files_dir)

        with open(f'{current_dir + files_dir}/{self._category_name[-1]}.csv', mode="w", newline="", encoding="utf8") as file_out:

            fieldnames = ['product_page_url','universal_product_code (upc)','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']
            result = csv.DictWriter(file_out, fieldnames=fieldnames, delimiter='|')
            result.writeheader()
            result.writerows(self._book_dicts)
        
        self._book_dicts = []

