# IMPORTS
from bs4 import BeautifulSoup as bs
import requests as rq
from p2_phase1 import get_book_infos, write_header_csv, write_book_csv

url_category_test1 = "https://books.toscrape.com/catalogue/category/books/romance_8/index.html"

header_test = "product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description," \
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
                filename = write_header_csv(header_test, category)
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
    print(str(total_articles) + " traités")

          
# CODE POUR TEST
#books_infos_by_category(url_category_test1)





