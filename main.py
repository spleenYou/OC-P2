from bs4 import BeautifulSoup
import requests
import csv

product_informations = []

def extract_information(product_page_url):
    page_product_request = requests.get(product_page_url)
    url_content = BeautifulSoup(page_product_request.content, 'html.parser')
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
    return product_information

def save_to_csv(data_to_save):
    with open('output.csv', mode='w', newline='') as file:
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

product_page_url = "https://books.toscrape.com/catalogue/the-project_856/index.html"
product_informations.append(extract_information(product_page_url))
save_to_csv(product_information)