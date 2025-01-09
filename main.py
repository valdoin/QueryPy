from Classes.Corpus import Corpus
from Classes.SearchEngine import SearchEngine
import os

json_filename = "data.json"

# Création d'un corpus
corpus = Corpus("Corpus COVID")

if os.path.exists(json_filename):
    print("Le fichier JSON existe, chargement des données...")
    corpus.load_from_json(json_filename)
else:
    print("Le fichier JSON n'existe pas. Interrogation des APIs...")
    corpus.generate_corpus()
    corpus.save_to_json(json_filename)

print(corpus)

# TD4 question 2.4
"""Affichage des statistiques d'un auteur 
name = input("Entrez le nom de l'auteur pour afficher les statistiques : ")
if name in corpus.authors:
    corpus.authors[name].display_stats()
else:
    print(f"Auteur '{name}' inconnu.")"""

# TD6 / Tests des fonctions d'analyse du contenu textuel
"""query = input("Entrez un mot clé correspondant à votre recherche : ")
corpus.search(query)
corpus.concorde(query,30)
corpus.stats(10)"""

# TD7 / Moteur de recherche
# Initialisation du moteur de recherche
print("Initialisation du moteur de recherche...")
search_engine = SearchEngine(corpus)

# Boucle de recherche
while True:
    query = input(
        "Entrez vos mots-clés pour effectuer une recherche (ou tapez 'exit' pour quitter) : "
    )
    if query.lower() == "exit":
        break

    query_keywords = query.lower().split()

    print("Recherche en cours...")
    results = search_engine.search(query_keywords, top_n=10) # on retourne 10 documents

    if not results.empty:
        print("\nRésultats de la recherche :")
        print(results[["Document ID", "Score", "Texte"]])
    else:
        print("Aucun résultat trouvé.")