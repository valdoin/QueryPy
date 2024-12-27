from Classes.Document import Document
from Classes.Author import Author
import praw
import urllib.request
import xmltodict
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime


# FONCTIONS

# Générer le corpus de documents
def generate_corpus():
    id2doc = {}
    doc_counter = 0

    load_dotenv()
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT')

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    subr = reddit.subreddit('Coronavirus')

    # Extraction des données Reddit
    for post in subr.hot(limit=20):
        title = post.title
        author = post.author.name if post.author else "Inconnu"
        date = datetime.fromtimestamp(post.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com" + post.permalink
        text = post.selftext.replace("\n", " ")

        doc = Document(title, author, date, url, text)
        id2doc[doc_counter] = doc
        doc_counter += 1

    # Extraction des données Arxiv
    query = "covid"
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=20'
    url_read = urllib.request.urlopen(url).read()
    data = url_read.decode()
    dico = xmltodict.parse(data)
    entries = dico['feed']['entry']

    for e in entries:
        title = e['title']
        authors = e.get('author', [])
        if isinstance(authors, list):
            authors = ", ".join([a.get("name", "Inconnu") for a in authors])
        elif isinstance(authors, dict):
            authors = authors.get("name", "Inconnu")
        date = datetime.strptime(e["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")
        url = e['id']
        text = e['summary'].replace("\n", " ")

        doc = Document(title, authors, date, url, text)
        id2doc[doc_counter] = doc
        doc_counter += 1

    return id2doc

# Sauvegarder le corpus dans un fichier CSV
def save_to_csv(id2doc, csv_filename):
    docs_data = [(doc_id, doc.title, doc.author, doc.date, doc.url, doc.text) for doc_id, doc in id2doc.items()]
    df = pd.DataFrame(docs_data, columns=["id", "titre", "auteur", "date", "url", "texte"])
    df.to_csv(csv_filename, sep="\t", index=False)
    print(f"Données sauvegardées dans le fichier {csv_filename}")

# Charger `id2doc` depuis un fichier CSV
def manage_docs_from_csv(csv_filename):
    id2doc = {}
    try:
        df = pd.read_csv(csv_filename, sep="\t")
        for _, row in df.iterrows():
            doc = Document(row['titre'], row['auteur'], row['date'], row['url'], row['texte'])
            id2doc[int(row['id'])] = doc
    except Exception as e:
        print(f"Erreur lors du chargement de {csv_filename} : {e}")
    return id2doc

# Gestion des auteurs à partir d'i2doc
def manage_authors(id2doc):
    id2aut = {}
    for doc in id2doc.values():
        authors = doc.author.split(", ") if ", " in doc.author else [doc.author]
        for author in authors:
            if author not in id2aut:
                id2aut[author] = Author(author)
            id2aut[author].add(doc)
    return id2aut

# Affichage des stats d'un auteur
def display_author_stats(author_name):
    if author_name in id2aut:
        author = id2aut[author_name]
        valid_texts = [doc.text for doc in author.production if isinstance(doc.text, str)]
        average_docs_size = (
            sum(len(text.split()) for text in valid_texts) / len(valid_texts)
            if valid_texts else 0
        )
        print(f"Statistiques pour {author_name} :")
        print(f"  Nombre de documents produits : {author.ndoc}")
        print(f"  Taille moyenne des documents : {average_docs_size:.0f} mots")
    else:
        print(f"Auteur '{author_name}' inconnu.")

# MAIN

# Chargement / génération des données
csv_filename = "data.csv"
id2doc = {}
id2aut = {}

if os.path.exists(csv_filename):
    print("Le fichier CSV existe, chargement des données...")
    id2doc = manage_docs_from_csv(csv_filename)
else:
    print("Le fichier CSV n'existe pas. Interrogation des APIs...")
    id2doc = generate_corpus()
    save_to_csv(id2doc, csv_filename)

id2aut = manage_authors(id2doc)
name = input("Entrez le nom de l'auteur pour afficher les statistiques : ")
display_author_stats(name)