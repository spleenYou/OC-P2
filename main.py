from transform import transform_informations
import save
import extract
import os

categories_save = 0
fieldnames = ['universal_product_code',
                      'title',
                      'price_including_tax',
                      'price_excluding_tax',
                      'number_available',
                      'product_description',
                      'category',
                      'review_rating',
                      'image_url']
path_csv = "csv/"

site_url = "https://books.toscrape.com/index.html"
print("---------------------------------------------------")
print(f"Bienvenue sur l'extracteur d'informations du site : {site_url}")
print("---------------------------------------------------")
print('Extraction lancée')
print("---------------------------------------------------")
# Recherche des categories et leurs adresses
product_categories_urls = extract.extract_categories(site_url)
categories_number = len(product_categories_urls)
print(f"{str(categories_number)} catégories trouvées")
for product_category in product_categories_urls:
    categories_save += 1
    print("---------------------------------------------------")
    # Pour chaque catégorie, recherche les adresses des livres
    print(f"Catégorie {product_category["category"]} ({categories_save}/{categories_number})")
    print(f"Démarrage de l'extraction")
    product_page_urls = extract.extract_urls(product_category["link"])
    # Extraction des informations de chaque livres de la catégorie
    print("Transformation des données reçues")
    product_informations = transform_informations(product_page_urls)
    # Enregistrement dans un fichier csv
    print(f"Création du fichier csv/{product_category["category"]}.csv")
    save.save_to_csv(product_informations, product_category["category"], fieldnames, path_csv)
    # Adaptation du texte selon le nombre de livre(s) trouvé(s)
    if len(product_informations) > 1:
        print(f"{str(len(product_informations))} livres ont été trouvés")
    else:
        print(f"{str(len(product_informations))} livre a été trouvé")
    
    print("Démarrage du téléchargement des photos")
    # Téléchargement des images correspondantes
    # Si le dossier "images" n'existe pas, il est créé
    if not os.path.exists("images"):
        os.mkdir("images")
    # Répertoire pour les images de la categorie en cours
    path_image = f"images/{product_category['category']}"
    # Si le dossier n'existe pas, il est créé
    if not os.path.exists(path_image):
        os.mkdir(path_image)
    for book in product_informations:
        # Récupération de l'image en ligne
        image_content = extract.requests_content(book["image_url"])
        #nommage du fichier de l'image
        name_image = f"{book['universal_product_code']}.{book['image_url'][-3:]}"
        # Ecriture de l'image
        save.save_image(path_image, name_image, image_content)

    # Adaptation du texte selon le nombre d'image(s) créé(es)
    image_count = len(product_informations)
    if image_count == 1:
        print(f"{image_count} image a été téléchargée")
    else:
        print(f"{image_count} images ont été téléchargées")
    print(f"Répertoire des photos images/{product_category["category"]}/")
    print("Extraction terminée pour cette catégorie")
print("Travail terminé")