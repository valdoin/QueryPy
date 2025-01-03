from Classes.Corpus import Corpus
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

# Affichage des statistiques d'un auteur
# name = input("Entrez le nom de l'auteur pour afficher les statistiques : ")
# if name in corpus.authors:
#     corpus.authors[name].display_stats()
# else:
#     print(f"Auteur '{name}' inconnu.")

# query = input("Entrez un mot clé correspondant à votre recherche : ")
# corpus.search(query)
# corpus.concorde(query,30)
corpus.stats(10)