# IMPORTS
from bs4 import BeautifulSoup as bs
import requests as rq
from p2_phase1 import write_header_csv
from p2_phase2 import books_infos_by_category

#
base_url = "https://books.toscrape.com/"


# ECRIT LES FICHIERS CSV POURTOUS LES LIVRES
# PARAMETRE : L'url du site
# RETOURNE : aucun retour
def all_books_infos(url):
    first = True

    page = rq.get(url)

    if page.status_code == 200:   # code 200 = récup OK
        
        # pour recherche dans le code html
        soup = bs(page.content, 'html.parser')

        # recuperation des categories et des url des catégories par le menu gauche
        balise_div = soup.find("div", class_="side_categories")
        balises_a = balise_div.find_all("a")

        liste_cat_url = []
        for a in balises_a:
            liste_cat_url.append(base_url+a["href"])
        
        # 1er à ignorer (non pertinent, Books / index.html)
        for cat_url in liste_cat_url:
            if first == True:
                first = False
            else:
                books_infos_by_category(cat_url)
        
    else:
        print("page site non trouvée")

