from bs4 import BeautifulSoup
import requests
import csv
import os

def bs_parser(url_to_parse):
    '''
    Parser d'url
    '''
    
    page_product_request = requests.get(url_to_parse)
    url_content = BeautifulSoup(page_product_request.content.decode("utf-8"), 'html.parser')
    return url_content

def transform_informations(product_page_urls):
    '''
    Transformation des informations d'un livre
    '''

    product_informations = []
    for product_page_url in product_page_urls:
        url_content = bs_parser(product_page_url)
        # Recherche du contenu de la classe, elle contient la note
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
        # Mise en dictionnaire des informations
        product_information = {}
        product_information["universal_product_code"] = url_content.find(class_="table-striped").find_all("td")[0].string
        product_information["title"] = url_content.find(class_="col-sm-6 product_main").find('h1').string
        product_information["price_including_tax"] = url_content.find(class_="table-striped").find_all("td")[3].string.replace("£", "")
        product_information["price_excluding_tax"] = url_content.find(class_="table-striped").find_all("td")[2].string.replace("£", "")
        product_information["number_available"] = url_content.find(class_="table-striped").find_all("td")[5].string.replace("In stock (", "").replace(" available)", "")
        # Test pour le cas ou certains livres n'auraient pas de description
        try:
            product_information["product_description"] = url_content.find(class_="sub-header").find_next_sibling("p").string
        except:
            product_information["product_description"] = ""
        product_information["category"] = url_content.find(class_="table-striped").find_all("td")[1].string
        product_information["review_rating"] = rating
        product_information["image_url"] = "https://books.toscrape.com/" + url_content.find(class_="carousel-inner").img['src'].replace("../../", "")
        product_informations.append(product_information)
    return product_informations

def extract_urls(urls_to_parse):
    '''
    Liste les urls des livres de la catégorie
    '''

    list_urls = []
    pages_to_parse = True
    # Répétition de l'extraction tant qu'un lien "next" est trouvé
    while pages_to_parse:
        urls_parser = bs_parser(urls_to_parse)
        # Extraction des livres présents sur la page
        for url in urls_parser.find("ol", class_="row").find_all("h3"):
            list_urls.append(url.find("a").attrs['href'].replace("../../..", "https://books.toscrape.com/catalogue"))
        # Recherche si un lien "next" est présent
        next_page = urls_parser.find(class_="next")
        if next_page:
            # Suppression de la fin de l'url
            url = urls_to_parse.split("/")
            del url[-1]
            for part in url:
                if "http" in part:
                    urls_to_parse = "https:/"
                else:
                    urls_to_parse += part + "/"
            # Rajout de l'adresse du lien "next" pour avoir la prochaine url a parser
            urls_to_parse += next_page.find("a").attrs["href"]
        else:
            # Si pas de lien "next" on arrête la boucle
            pages_to_parse = False
    return list_urls

def extract_categories(site_urls):
    '''
    Extraction des catégories
    '''
    list_category = []
    # Analyse de l'adresse
    url_parser = bs_parser(site_url)
    all_a = url_parser.find(class_="side_categories").find_all('a')
    # Recherche des catégories
    for a in all_a:
        if "books_1" not in a.attrs['href']:
            name_category = ""
            # création d'un tableau pour récupérer le nom de la catégorie en présevant l'espace entre les mots si besoin
            name_table = a.text.replace("\n", "").split(" ")
            for name in name_table:
                if name != "":
                    name_category += name + " "
            # Suppression du dernier espace
            name_category = name_category[:-1]
            list_category.append({"category": name_category, "link": "https://books.toscrape.com/" + a.attrs['href']})
    return list_category

def save_to_csv(data_to_save, file_name):
    '''
    Enregistrement dans des fichiers csv
    '''
    
    # Si le dossier "csv" n'existe pas, il est créé
    if not os.path.exists("csv"):
        os.makedirs("csv")
    # Ecriture du fichier csv
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
    '''
    Démarrage de l'extraction des catégories puis des livres
    '''

    print('Extraction lancée')
    # Recherche des categories et leurs adresses
    product_categories_urls = extract_categories(site_url)
    print(f"{str(len(product_categories_urls))} catégories trouvées")
    for product_category in product_categories_urls:
        # Pour chaque catégorie, recherche les adresses des livres
        product_page_urls = extract_urls(product_category['link'])
        # Extraction des informations de chaque livres de la catégorie
        product_informations = transform_informations(product_page_urls)
        # Enregistrement dans un fichier csv
        save_to_csv(product_informations, product_category['category'])
        # Adaptation du texte selon le nombre de livre(s) trouvé(s)
        if len(product_informations) > 1:
            print(f"Pour la categorie {product_category['category']}, {str(len(product_informations))} livres ont été trouvés et sauvegardés")
        else:
            print(f"Pour la categorie {product_category['category']}, {str(len(product_informations))} livre a été trouvé et sauvegardé")

def download_images():
    '''
    Téléchargement des images des livres
    '''

    # Si le dossier "images" n'existe pas, il est créé
    if not os.path.exists("images"):
        os.mkdir("images")
    # Listage des fichier csv
    files_category = os.listdir("csv")
    for file_category in files_category:
        # Répertoire pour les images de la categorie en cours
        path = f"images/{file_category[:-4]}"
        # Si le dossier n'existe pas, il est créé
        if not os.path.exists(path):
            os.mkdir(path)
        # Lecture du fichier csv pour récupération des urls des images
        with open(f"csv/{file_category}", 'r', encoding="utf-8") as file:
            books = csv.DictReader(file)
            # Nombre d'image(s) créé(es)
            image_count = 0
            for book in books:
                # Récupération de l'image en ligne
                get_image = requests.get(book["image_url"]).content
                # Ecriture de l'image
                with open (f"{path}/{book['universal_product_code']}.{book['image_url'][-3:]}", 'wb') as image:
                    image_count += 1
                    image.write(get_image)
        # Adaptation du texte selon le nombre d'image(s) créé(es)
        if image_count == 1:
            print(f"Pour la catégorie {file_category[:-4]}, {image_count} image a été téléchargée")
        else:
            print(f"Pour la catégorie {file_category[:-4]}, {image_count} images ont été téléchargées")

site_url = "https://books.toscrape.com/index.html"
print(f"Bienvenue sur l'extracteur d'informations du site : {site_url}")
start_extract(site_url)
print("Extraction finie")
print("Démarrage du téléchargement des photos")
download_images()
print("Fin du téléchargement des photos")