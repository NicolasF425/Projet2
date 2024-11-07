## Programme de demonstration de scrapping sur le site https://books.toscrape.com/ dans le cadre d'une formation Python

### Description du contexte

Dans le cadre d'une analyse de marché, on souhaite réaliser une démonstration de scrapping avec utilisation du processus ETL (Extract Transform Load) ;

Nous allons récupérer le code html du site (Extract), extraire et formater les données recherchées (Transform) puis les écrire dans des fichiers Load)

**Pour chaque livre, on extrait les informations suivantes :**
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

Les données seront ensuite inscrites dans des fichiers csv et les images sauvegardées.

### **Prérequis :** 

+ Un environnement de développement (VSCode, Pycharm...)
+ Python 3.X
+ avoir installé pip (gestionnaire de packages pour python) s'il n'est pas présent


### **Pour récuperer les fichiers du projet :**

exécuter : git clone https://github.com/NicolasF425/Projet2.git

### **Pour créer l'environnement virtuel _env_**

Dans le répertoire du projet exécuter : python -m venv env

Pour activer l'environnement virtuel, Utilisez la commande selon votre système d'exploitation.

**Activation sur Windows** :

dans env/Scripts exécuter _activate_

**Activation sur MacOS/Linux** :

exécuter à partir du répertoire projet: source env/bin/activate

### **Pour installer les dépendances :**

Aller dans le répertoire _env_ puis exécuter : pip install -r requirements.txt

Le fichier requirements.txt doit être présent dans le dossier du projet

### **Execution du programme :**

_python main.py_

Le programme va créer un répertoire csv et un répertoire img

Inscrit les informations à raison d'un livre par ligne,  dans un fichier csv par catégories.

Télécharge également les images pour tous les livres.



