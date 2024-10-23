from bs4 import BeautifulSoup as bs
import requests as rq


# URL de la page qui nous intéresse
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# récupère les données html de la page
result = rq.get(url)


if result.status_code == 200:   # code 200 = OK
    
    # affichage du code source de la page
    print (result.text)
    
    # ouvre un fichier source.txt en écriture ou le créé
    f = open('source.txt', 'w')
    # écrit les données de la page dans le fichier source.txt
    f.write(result.text)

else:
    print ("Erreur")

