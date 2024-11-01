# IMPORTS
from bs4 import BeautifulSoup as bs
import requests as rq
import re
import os


# RECUPERE LES INFOS SUR UN LIVRE
# product_page_url
# universal_product_code (upc)
# title
# price_including_tax
# price_excluding_tax
# number_available
# product_description
# category
# review_rating
# image_url
# PARAMETRES : l'url du produit et la categorie de ce produit
# RETOURNE : une liste des elements demandes
def get_book_infos(url, category):
    # récupère les données html de la page
    page = rq.get(url)

    if page.status_code == 200:   # code 200 = récup OK
        
        # pour recherche dans le code html
        soup = bs(page.content, 'html.parser')

        # recheche sur la balise <li> et la classe "active" car combinaison unique sur la page
        # puis on ne garde que le contenu utile (texte)
        title = '"'+soup.find("li", class_="active").get_text()+'"'

        # RECHERCHE ET RECUPERATION DE L'UPC, DU PRIX HT ET DU PRIX TTC
        ###

        # selection de la balise <table> et de la classe "table table-striped" car combinaison unique sur la page
        infos_brut = soup.find("table", class_="table table-striped")

        # recherche des balise <td> contenant les infos
        infos_liste = infos_brut.findAll("td")
        # suppression des balises
        liste_textes = []
        for info in infos_liste:
            liste_textes.append(info.get_text())
        
        # affectation des infos
        # UPC, prix HT, prix TTC et nombre disponible
        UPC = liste_textes[0]
        price_exc_tax = liste_textes[2]
        price_exc_tax = price_exc_tax[1:len(price_exc_tax)-1]   # suppression du texte de la monnaie
        price_inc_tax = liste_textes[3]
        price_inc_tax = price_inc_tax[1:len(price_inc_tax)-1]   # suppression du texte de la monnaie
        number_available = liste_textes[5]

        numbers_available = re.findall(r'\d+', number_available)    # recherche de la quantite dans le chaine de caracteres
        if numbers_available:
            number_available = numbers_available[0]
        else:
            number_available = "0"
        ###

        # récuperation du descriptif du livre
        balises_p = soup.find_all("p")
        balises = []
        for balise in balises_p:
            balises.append(balise.get_text())   # suppression des balises dans la chaine de caracteres
        # le descriptif est la quatrieme balise de la liste + ajout des guillements pour gestion des virgules
        book_desc = '"' + balises[3] + '"' 

        # recherche et récupération de nombre d'étoile
        liste_nombre_etoile = ["One","Two","Three","Four","Five"]
        nombre_etoiles = 1
        for n in liste_nombre_etoile:
            if soup.find("p", class_="star-rating " + n) != None: # None = pas d'élément correspondant
                break
            nombre_etoiles += 1

        # recherche et récupération de l'url de l'image
        # selection de la balise <img> car unique sur la page
        search_url_image  = soup.find("img")
        # concatenation de l'url de base avec l'extraction de la source moins les 6 premiers caractères
        image_url = "https://books.toscrape.com/" + search_url_image['src'][6:]
        ext_img = image_url[-4:]

        # création du repertoire/dossier img si besoin et enregistrement de l'image
        dir_img = "img"
        isExist = os.path.exists(dir_img)
        if not isExist:
            os.makedirs(dir_img)
            print("creation du repertoire " + dir_img)
        r = rq.get(image_url, allow_redirects=True)
        open(dir_img + "/" + UPC + ext_img, 'wb').write(r.content)
        
        # creation de la liste avec les infos du livres
        # on commence par l'url et on ajoute les autres infos
        liste_infos_livre = []
        liste_infos_livre.append(url)
        liste_infos_livre.append(UPC)
        liste_infos_livre.append(title)
        liste_infos_livre.append(price_inc_tax)
        liste_infos_livre.append(price_exc_tax)   
        liste_infos_livre.append(number_available)
        liste_infos_livre.append(book_desc)
        liste_infos_livre.append(category)
        liste_infos_livre.append(str(nombre_etoiles))
        liste_infos_livre.append(image_url)
        
        # on renvoit la liste des infos
        return liste_infos_livre

    else:
        print("Page infos livre non trouvée")

    
# ecrit les infos sur un livre dans un fichier
# PARAMETRES : la liste des infos pour un livre, le nom du fichier
# RETOURNE : aucun retour
def write_book_csv(liste_infos, filename):

    # ouvre un fichier livre.csv en écriture ou le créé
    f = open(filename, 'a', encoding='utf-8')

    # insertion du separateur ,
    ligne = ""
    for i in liste_infos:
        ligne += i
        ligne += ","
    # suppression de la virgule de fin et remplacement par \n
    ligne = ligne[:-1]+"\n"

    # ecriture dans le fichier des infos sur le livre
    f.write(ligne)
