Programme de demonstration de scrapping sur le site https://books.toscrape.com/ dans le cadre d'une formation Python

Pour chaque livre, extrait les informations suivantes :
 + product_page_url
 + universal_ product_code (upc)
 + title
 + price_including_tax
 + price_excluding_tax
 + number_available
 + product_description
 + category
 + review_rating
 + image_url

Prérequis : 

+ Python 3 ou supérieur
+ Packages :  BeautifulSoup4, Requests

**Pour créer l'environnement virtuel _env_ :**
Dans le répertoire du projet exécuter : python -m venv env
Puis dans .../env/Scripts exécuter _activate_

**Pour installer les 2 packages requis :**

Aller dans le répertoire _env_ puis exécuter :

pip install requests

pip install beautifulsoup4


**Execution du programme :**

python main.py

Créé un répertoire csv et un répertoire img

Inscrit les livres dans un fichier csv par catégories;

Télécharge également les images pour tous les livres.


