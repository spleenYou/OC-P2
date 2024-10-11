import os
import csv

def save_to_csv(data_to_save, file_name, fieldnames, path_csv):
    '''
    Enregistrement dans un fichier csv

    Parameters
    ----------
    data_to_save : dictionnaire des informations à sauvegarder
    file_name : nom du fichier à écrire
    fieldnames : liste des noms de champs
    path_csv : chemin du répertoire du csv à créer

    Returns
    -------
    none
    '''
    
    # Si le dossier "csv" n'existe pas, il est créé
    if not os.path.exists(path_csv):
        os.makedirs(path_csv)
    # Ecriture du fichier csv
    with open(path_csv +file_name + '.csv', mode='w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_to_save:
            writer.writerow(data)

def save_image(path, name_image, image_content):
    """
    Sauvegarde de l'image d'un livre

    Parameters
    ----------
    path : emplacement du fichier à sauvegarder
    name_image : nom de l'image à sauvegarder
    image_content : contenu de l'image à sauvegarder
    """
    with open (f"{path}/{name_image}", 'wb') as image:
        image.write(image_content)