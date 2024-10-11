from bs4 import BeautifulSoup
import requests

def requests_content(url_to_request):
    '''
    Fait une requète HTTP pour récupérer le code de la page demandée

    Parameters
    ----------
    url_to_request : url de la page

    Returns
    -------
    contenu de la page
    '''
    page_request = requests.get(url_to_request)
    page_content = page_request.content
    return page_content

def page_parser(content_to_parse):
    '''
    Parser d'url

    Parameters
    ----------
    content_to_parse : contenu à parser

    Returns
    -------
    contenu parser en html et décoder en UTF-8
    '''
    url_content = BeautifulSoup(content_to_parse.decode("utf-8"), 'html.parser')
    return url_content

def extract_urls(url_to_extract):
    '''
    Liste les urls des livres de la catégorie

    Parameters
    ----------
    url_to_extract : lien de la catégorie à parcourir

    Returns
    -------
    liste des URLs des livres parser
    '''

    list_urls = []
    pages_to_parse = True
    # Répétition de l'extraction tant qu'un lien "next" est trouvé
    while pages_to_parse:
        content = requests_content(url_to_extract)
        url_parser = page_parser(content)
        # Extraction des livres présents sur la page
        for url in url_parser.find("ol", class_="row").find_all("h3"):
            list_urls.append(url.find("a").attrs['href'].replace("../../..", "https://books.toscrape.com/catalogue"))
        # Recherche si un lien "next" est présent
        next_page = url_parser.find(class_="next")
        if next_page:
            # Suppression de la fin de l'url
            url = url_to_extract.split("/")
            del url[-1]
            for part in url:
                if "http" in part:
                    url_to_extract = "https:/"
                else:
                    url_to_extract += part + "/"
            # Rajout de l'adresse du lien "next" pour avoir la prochaine url a parser
            url_to_extract += next_page.find("a").attrs["href"]
        else:
            # Si pas de lien "next" on arrête la boucle
            pages_to_parse = False
    urls_parser = []
    for url in list_urls:
        urls_parser.append(page_parser(requests_content(url)))
    return urls_parser

def extract_categories(site_url):
    '''
    Extraction des catégories

    Parameters
    ----------
    site_url : adresse du site

    Returns
    -------
    liste de toutes les catégories du sites
    '''
    list_category = []
    # Analyse de l'adresse
    url_content = requests_content(site_url)
    content = page_parser(url_content)
    all_a = content.find(class_="side_categories").find_all('a')
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
