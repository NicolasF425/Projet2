# IMPORTS
from bs4 import BeautifulSoup as bs
import requests as rq


# URL de la page qui nous intéresse
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"



# RECUPERE LES INFOS SUR UN LIVRE
# product_page_url
# universal_ product_code (upc)
# title
# price_including_tax
# price_excluding_tax
# number_available
# product_description
# category
# review_rating
# image_url
# PARAMETRE : l'url du produit
def get_book_infos(url):
    liste_infos_livre = [""]
    # récupère les données html de la page
    page = rq.get(url)

    if page.status_code == 200:   # code 200 = OK
        
        # pour recherche dans le code html
        soup = bs(page.content, 'html.parser')

        # recheche sur la balise <li> et la classe "active"
        # car combinaison unique sur la page
        # puis on ne garde que le contenu utile
        titre_livre = soup.find("li", class_="active").get_text()

        # recheche sur la balise <p> et la classe "price_color"
        # car combinaison unique sur la page
        # puis on ne garde que le contenu utile
        prix_livre = soup.find("p", class_="price_color").get_text()
        # suppression de la monnaie utilisée
        prix_livre = prix_livre[1:len(prix_livre)-1]

        # creation de la liste avec les infos du livres
        # on commence par l'url et on ajoute les autres infos
        liste_infos_livre[0] = url
        liste_infos_livre.append(titre_livre)
        liste_infos_livre.append(prix_livre)

        return liste_infos_livre

    else:
        print("Erreur")

# test d'ecriture avec un livre
def write_book_csv(liste_infos):
    header = "product_page_url,UPC,title,price_including_tax,price_excluding_tax,number_available,product_description," \
            "category,review_rating,image_url\n"

    # ouvre un fichier livre.csv en écriture ou le créé
    f = open('livre.csv', 'w')
    
    # ecrit le header du fichier csv
    f.write(header)

    # écrit les données d'un livre sur une ligne dans le fichier livre.csv
    ligne = ""
    for i in liste_infos:
        ligne += i
        ligne += ","
    f.write(ligne)


liste_infos = get_book_infos(url)
write_book_csv(liste_infos)