from p2_phase1 import get_book_infos, write_book_csv, write_header_csv

# URL de la page qui nous intéresse
url1 = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

url2 = "https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"

# header pour le fichier csv des livres
header = "product_page_url,UPC,title,price_including_tax,price_excluding_tax,number_available,product_description," \
            "category,review_rating,image_url\n"


# EXECUTION DU PROGRAMME pour 1 livre
liste_infos = get_book_infos(url2)
write_header_csv(header)
write_book_csv(liste_infos)
