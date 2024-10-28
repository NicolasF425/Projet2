# IMPORTS
from bs4 import BeautifulSoup as bs
import requests as rq
from p2_phase1 import write_header_csv
from p2_phase2 import books_infos_by_category

url_site = "https://books.toscrape.com/"

header = "product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description," \
            "category,review_rating,image_url\n"

# 
def all_books_infos(url):
    
    page = rq.get(url)

    if page.status_code == 200:   # code 200 = récup OK
        
        # pour recherche dans le code html
        soup = bs(page.content, 'html.parser')

        balise_div = soup.find("div", class_="side_categories")
        balises_a = balise_div.find_all("a")
        liste_url_cat = []
        for a in balises_a:
            #print(url_site+a["href"])
            liste_url_cat.append(url_site+a["href"])
        
        # 1er à ignorer
        first = True
        for url_cat in liste_url_cat:
            if  first == False:
                print(url_cat)
                books_infos_by_category(url)
            else:
                first = False
        
    else:
        print("page site non trouvée")

write_header_csv(header)
all_books_infos(url_site)

