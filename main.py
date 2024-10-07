from bs4 import BeautifulSoup
import requests
import csv

def bs_parser(url_to_parser):
    page_product_request = requests.get(url_to_parser)
    url_content = BeautifulSoup(page_product_request.content.decode("utf-8"), 'html.parser')
    return url_content

def extract_informations(product_page_urls):
    product_informations = []
    for product_page_url in product_page_urls:
        url_content = bs_parser(product_page_url)
        match url_content.find_all("p", class_="star-rating")[0].get('class')[1]:
            case"One":
                rating = 1
            case "Two":
                rating = 2
            case "Three":
                rating = 3
            case "Four":
                rating = 4
            case "Five":
                rating = 5
            case _:
                rating = 0
        product_information = {}
        product_information["universal_product_code"] = url_content.find(class_="table-striped").find_all("td")[0].string
        product_information["title"] = url_content.find(class_="col-sm-6 product_main").find('h1').string
        product_information["price_including_tax"] = float(url_content.find(class_="table-striped").find_all("td")[3].string.replace("£", ""))
        product_information["price_excluding_tax"] = float(url_content.find(class_="table-striped").find_all("td")[2].string.replace("£", ""))
        product_information["number_available"] = url_content.find(class_="table-striped").find_all("td")[5].string.replace("In stock (", "").replace(" available)", "")
        product_information["product_description"] = url_content.find(class_="sub-header").find_next_sibling("p").string
        product_information["category"] = url_content.find(class_="table-striped").find_all("td")[1].string
        product_information["review_rating"] = rating
        product_information["image_url"] = product_page_url + "/" + url_content.find(class_="carousel-inner").img['src'].replace("../../", "")
        product_informations.append(product_information)
    return product_informations

def extract_urls(url_category):
    urls_parser = bs_parser(url_category)
    list_urls = []
    for i in urls_parser.find("ol", class_="row").find_all("h3"):
        list_urls.append(i.find("a").attrs['href'].replace("../../..", "https://books.toscrape.com/catalogue"))
    return list_urls

def save_to_csv(data_to_save):
    with open('output.csv', mode='w', newline='', encoding="utf-8") as file:
        fieldnames = ['universal_product_code',
                      'title',
                      'price_including_tax',
                      'price_excluding_tax',
                      'number_available',
                      'product_description',
                      'category',
                      'review_rating',
                      'image_url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_to_save:
            writer.writerow(data)

product_category_url = "https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html"
product_page_urls = extract_urls(product_category_url)
product_informations = extract_informations(product_page_urls)
save_to_csv(product_informations)