# IMPORTS
from bs4 import BeautifulSoup as bs
import requests as rq

titre_livre = ""
prix_livre = 0

# URL de la page qui nous intéresse
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"


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

    print("Titre du livre : ", titre_livre)
    print("Prix : ", prix_livre)
 
    # ouvre un fichier source.txt en écriture ou le créé
    #f = open('livre.txt', 'w')
    # écrit les données de la page dans le fichier source.txt
    #f.write(page.content)

else:
    print ("Erreur")




