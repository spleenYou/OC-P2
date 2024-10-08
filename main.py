from bs4 import BeautifulSoup
import requests
import csv

def bs_parser(url_to_parse):
    page_product_request = requests.get(url_to_parse)
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
        try:
            product_information["product_description"] = url_content.find(class_="sub-header").find_next_sibling("p").string
        except:
            product_information["product_description"] = ""
        product_information["category"] = url_content.find(class_="table-striped").find_all("td")[1].string
        product_information["review_rating"] = rating
        product_information["image_url"] = product_page_url + "/" + url_content.find(class_="carousel-inner").img['src'].replace("../../", "")
        product_informations.append(product_information)
    return product_informations

def extract_urls(urls_to_parse):
    list_urls = []
    pages_to_parse = True
    while pages_to_parse:
        urls_parser = bs_parser(urls_to_parse)
        for url in urls_parser.find("ol", class_="row").find_all("h3"):
            list_urls.append(url.find("a").attrs['href'].replace("../../..", "https://books.toscrape.com/catalogue"))

        next_page = urls_parser.find(class_="next")
        if next_page:
            url = urls_to_parse.split("/")
            del url[-1]
            for part in url:
                if "http" in part:
                    urls_to_parse = "https:/"
                else:
                    urls_to_parse += part + "/"
            urls_to_parse += next_page.find("a").attrs["href"]
        else:
            pages_to_parse = False
    return list_urls

def extract_categories(site_urls):
    list_category = []
    url_parser = bs_parser(site_url)
    all_a = url_parser.find(class_="side_categories").find_all('a')
    for a in all_a:
        if "books_1" not in a.attrs['href']:
            name_category = ""
            name_table = a.text.replace("\n", "").split(" ")
            for name in name_table:
                if name != "":
                    name_category += name + " "
            name_category = name_category[:-1]
            list_category.append({"category": name_category, "link": "https://books.toscrape.com/" + a.attrs['href']})
    return list_category

def save_to_csv(data_to_save, file_name):
    with open("csv/" +file_name + '.csv', mode='w', newline='', encoding="utf-8") as file:
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

def start_extract(site_url):
    print('Extraction lancée')
    product_categories_urls = extract_categories(site_url)
    print(f"{str(len(product_categories_urls))} catégories trouvées")
    for product_category in product_categories_urls:
        product_page_urls = extract_urls(product_category['link'])
        product_informations = extract_informations(product_page_urls)
        save_to_csv(product_informations, product_category['category'])
        if len(product_informations) > 1:
            print(f"Pour la categorie {product_category['category']}, {str(len(product_informations))} livres ont été trouvés et sauvegardés")
        else:
            print(f"Pour la categorie {product_category['category']}, {str(len(product_informations))} livre a été trouvé et sauvegardé")

if __name__ == "__main__":
    site_url = "https://books.toscrape.com/index.html"
    print(f"Bienvenue sur l'extracteur d'information du site : {site_url}")
    start_extract(site_url)
    print("Extraction finie")