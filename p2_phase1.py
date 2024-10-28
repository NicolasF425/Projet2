# IMPORTS
from bs4 import BeautifulSoup as bs
import requests as rq


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
# PARAMETRE : l'url du produit
# RETOUR : une liste des elements demandes
def get_book_infos(url):
    # récupère les données html de la page
    page = rq.get(url)

    if page.status_code == 200:   # code 200 = récup OK
        
        # pour recherche dans le code html
        soup = bs(page.content, 'html.parser')

        # recheche sur la balise <li> et la classe "active" car combinaison unique sur la page
        # puis on ne garde que le contenu utile (texte)
        title = soup.find("li", class_="active").get_text()

        # recherche et recuperation de l'UPC, du prix HT et du prix TTC 
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


        # récuperation du descriptif du livre
        balises_p = soup.find_all("p")
        balises = []
        for balise in balises_p:
            balises.append(balise.get_text())   # suppression des balises dans la chaine de caracteres
        # le descriptif est la quatrieme balise de la liste + ajout des guillements pour gestion des virgules
        book_desc = '"' + balises[3] + '"' 
        
        # recherche et recuperation de la categorie
        # selection de la balise <ul> et de la classe "breadcrumb" car combinaison unique sur la page
        search = soup.find("ul", class_="breadcrumb")
        # recheche des balises <a> dans cette recherche
        liste_a = search.find_all("a")
        liste_str = []
        for i in liste_a:
            liste_str.append(i.get_text())
        category = liste_str[2]

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
        
        # creation de la liste avec les infos du livres
        # on commence par l'url et on ajoute les autres infos
        liste_infos_livre = []
        liste_infos_livre.append(url)
        liste_infos_livre.append(UPC)
        liste_infos_livre.append(title)
        liste_infos_livre.append(price_exc_tax)
        liste_infos_livre.append(price_inc_tax)
        liste_infos_livre.append(number_available)
        liste_infos_livre.append(book_desc)
        liste_infos_livre.append(category)
        liste_infos_livre.append(str(nombre_etoiles))
        liste_infos_livre.append(image_url)
        
        # on renvoit la liste des infos
        return liste_infos_livre

    else:
        print("Page livre non trouvée")


# ecrit le header du fichier csv
def write_header_csv(string_header):
    
    # ouvre un fichier livre.csv en écriture ou le créé
    f = open('livre.csv', 'w')
    
    # ecrit le header du fichier csv
    f.write(string_header)

    
# ecrit les infos sur un livre dans un fichier
def write_book_csv(liste_infos):

    # ouvre un fichier livre.csv en écriture ou le créé
    f = open('livre.csv', 'a')
    
    # insertion du separateur ,
    ligne = ""
    for i in liste_infos:
        ligne += i
        ligne += ","
    # suppression de la virgule de fin et remplacement par \n
    ligne = ligne[:-1]+"\n"

    # ecriture dans le fichier des infos sur le livre
    f.write(ligne)




    

