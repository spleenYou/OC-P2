def transform_informations(product_page_urls_parser):
    '''
    Transformation des informations des livres d'une catégorie

    Parameters
    ----------
    product_page_urls_parser : liste avec les urls parser dont les informations doivent être extraites
    Returns
    -------
    Une liste contenant un dictionnaire par livre avec les informations demandées
    '''

    product_informations = []
    for product_page_url_parser in product_page_urls_parser:
        url_content = product_page_url_parser['url_parse']
        url_page = product_page_url_parser['product_page_url']
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
        product_information["product_page_url"] = url_page
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