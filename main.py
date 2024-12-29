from Classes.Corpus import Corpus
import os

csv_filename = "data.csv"

# Création d'un corpus 
corpus = Corpus("Corpus COVID")

if os.path.exists(csv_filename):
    print("Le fichier CSV existe, chargement des données...")
    corpus.load_from_csv(csv_filename)
else:
    print("Le fichier CSV n'existe pas. Interrogation des APIs...")
    corpus.generate_corpus()  
    corpus.save_to_csv(csv_filename)

# Affichage des statistiques d'un auteur
# name = input("Entrez le nom de l'auteur pour afficher les statistiques : ")
# if name in corpus.authors:
#     corpus.authors[name].display_stats()
# else:
#     print(f"Auteur '{name}' inconnu.")

print(corpus)