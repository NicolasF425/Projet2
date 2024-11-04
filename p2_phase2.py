# IMPORTS
from bs4 import BeautifulSoup as bs
import requests as rq
from p2_phase1 import get_book_infos, write_book_csv
import os
from datetime import datetime as dt
from p2_phase1 import get_book_infos, write_book_csv
import os
from datetime import datetime as dt

# 
header = "product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description," \
            "category,review_rating,image_url\n"


# ECRIT LES INFOS DES LIVRES D'UNE CATEGORIE
# PARAMETRE : l'url de la page de la categorie concernee
def books_infos_by_category(url):
    next = True         # booleen pour détection du bouton next
    first = True        # booleen pour recuperation de la categorie et creation du fichier à la première boucle

    category = ""
    filename = ""

    total_articles = 0

    base_url = url[:-10]
    
    while next:
        page = rq.get(url)

        if page.status_code == 200:   # code 200 = récup OK
            # pour recherche dans le code html
            soup = bs(page.content, 'html.parser')

            articles = soup.find_all("article")

            # si premiere boucle on recupere la categorie et on cree le fichier avec le header
            if first:
                category = soup.find("li", class_="active").get_text()
                filename = write_header_csv(header, category)
                first = False
                print("En cours de traitement : " + category)
            
            balises_a = []
            for a in articles:
                # recherche sur la balise <h3> car unique par article
                tmp = a.find("h3")
                balises_a.append(tmp.find("a"))

            liste_url = []
            for balise in balises_a:
                # concatene l'url de base avec le lien dans la balise moins les 9 premiers caracteres            
                liste_url.append("https://books.toscrape.com/catalogue/"+balise["href"][9:])    

            # pour chaque url / article on recupere les infos et on ecrit dans le fichier
            for url in liste_url:
                book_infos = get_book_infos(url, category)
                write_book_csv(book_infos, filename)
                total_articles += 1

            li_next = soup.find("li", class_="next")
            # si bouton next on créé une nouvelle url et on boucle
            if li_next != None:
                next_url_end = li_next.find("a")["href"]
                url = base_url + next_url_end
            else:  # sinon on termine la boucle while
                next = False

        else:
            print("Page categorie " + url + "non trouvée")
    print(str(total_articles) + " elements")


# CREE LE FICHIER ET ECRIT LE HEADER
# PARAMETRES : chaines de caracteres du header et de la categorie
# RETOURNE : le nom du fichier créé
def write_header_csv(string_header, category):
    filename = category # nom par défaut

    # Creation repertoire csv si besoin
    dir_csv = "csv"
    isExist = os.path.exists(dir_csv)
    if not isExist:
        os.makedirs(dir_csv)
        print("creation du repertoire " + dir_csv)
    
    # ajout horodatage du fichier
    horodatage = dt.now()
    horodatage = horodatage.strftime('-%Y-%m-%d')
    filename = dir_csv + "/" + filename + horodatage + ".csv"

    # ouvre un fichier livre.csv en écriture ou le créé
    f = open(filename, 'w', encoding='utf-8')
    
    # ecrit le header du fichier csv
    f.write(string_header)

    # ferme le fichier
    f.close()

    return filename