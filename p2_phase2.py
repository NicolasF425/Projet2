# IMPORTS
from bs4 import BeautifulSoup as bs
import requests as rq
from p2_phase1 import get_book_infos, write_header_csv, write_book_csv

base_url_category = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"



def books_infos_by_category(url):
    
    next = True         # booleen pour détection du bouton next
    has_header = False  # booleen pour test si le header a deja ete ecrit

    base_url = url[:-10]
    
    while next:
        page = rq.get(url)

        if page.status_code == 200:   # code 200 = récup OK
            # pour recherche dans le code html
            soup = bs(page.content, 'html.parser')

            articles = soup.find_all("article")
            
            balises_a = []
            for a in articles:
                tmp = a.find("h3")
                balises_a.append(tmp.find("a"))

            liste_url = []
            for balise in balises_a:
                liste_url.append("https://books.toscrape.com/catalogue/"+balise["href"][9:])
            
            #if has_header == False:
            #   write_header_csv(header)
            #    has_header = True

            for url in liste_url:
                book_infos = get_book_infos(url)
                write_book_csv(book_infos)

            li_next = soup.find("li", class_="next")
            # si bouton next on créé une nouvelle url et on boucle
            if li_next != None:
                next_url_end = li_next.find("a")["href"]
                url = base_url + next_url_end
            else:  # sinon on termine la boucle while
                next = False

        else:
            print("Page categorie non trouvée")
            

books_infos_by_category(base_url_category)







