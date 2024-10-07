from bs4 import BeautifulSoup
import requests

product_page_url = "https://books.toscrape.com/catalogue/the-project_856/index.html"
page_product_request = requests.get(product_page_url)
url_content = BeautifulSoup(page_product_request.content, 'html.parser')

universal_product_code = url_content.find(class_="table-striped").find_all("td")[0].string
title = url_content.find(class_="col-sm-6 product_main").find('h1').string
price_including_tax = url_content.find(class_="table-striped").find_all("td")[3].string
price_excluding_tax = url_content.find(class_="table-striped").find_all("td")[2].string
number_available = url_content.find(class_="table-striped").find_all("td")[5].string
product_description = url_content.find(class_="sub-header").find_next_sibling("p").string
category = url_content.find(class_="table-striped").find_all("td")[1].string
review_rating = url_content.find(class_="table-striped").find_all("td")[6].string
image_url = url_content.find(class_="carousel-inner").img['src']