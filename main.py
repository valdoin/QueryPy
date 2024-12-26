from Classes.Document import Document
from Classes.Author import Author
import praw
import urllib.request
import xmltodict
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

# On voit si le fichier csv existe déjà

csv_filename = "data.csv"
id2doc = {}  

if os.path.exists(csv_filename):
    df = pd.read_csv(csv_filename, sep="\t")
    print("Données chargées depuis le fichier CSV.")
    print(df.head())
else:
    print("Le fichier CSV n'existe pas. Interrogation des APIs...")

    # Chargement des variables d'environnement

    load_dotenv()
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT')

    doc_counter = 0

    # Chargement des données Reddit

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    subr = reddit.subreddit('Coronavirus')

    for post in subr.hot(limit=20):
        # Création de l'objet Document pour chaque post
        title = post.title
        author = post.author.name
        date = datetime.fromtimestamp(post.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com" + post.permalink 
        text = post.selftext
        text = text.replace("\n", " ")
        
        # génération d'un identifiant unique pour chaque document
        id2doc[doc_counter] = Document(title, author, date, url, text)
        doc_counter += 1
        
        print(id2doc)

    # Chargement des données Arxiv

    query = "covid"
    url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=20'
    url_read = urllib.request.urlopen(url).read()
    data = url_read.decode()
    dico = xmltodict.parse(data)
    entries = dico['feed']['entry']

    for e in entries:
        # Création de l'objet Document pour chaque article Arxiv
        title = e['title']
        # Vérification du format de la liste d'auteurs
        authors = e.get('author', [])
        if isinstance(authors, list): # si c'est une liste, on extrait les noms
            authors = ", ".join([a.get("name", "Inconnu") for a in authors])
        elif isinstance(authors, dict): # si c'est un dictionnaire (un seul auteur), on prend directement son nom
            authors = authors.get("name", "Inconnu")
        date = datetime.strptime(e["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")
        url = e['id']
        text = e['summary']
        text = text.replace("\n", " ")

        id2doc[doc_counter] = Document(title, authors, date, url, text)
        doc_counter += 1

    # Manipulation du corpus de documents

    print(f"Le corpus contient {len(id2doc)} documents.")

    # Affichage du nombre de mots et de phrases pour chaque document
    for doc_id, doc in id2doc.items():
        words_nb = len(doc.text.split())
        phrases_nb = len(doc.text.split('.'))
        print(f"Document {doc_id} : {words_nb} mots, {phrases_nb} phrases.")

    # Suppression des documents trop petits (moins de 20 caractères)

    # id2doc = {doc_id: doc for doc_id, doc in id2doc.items() if len(doc.texte) > 20}
    # print(f"Après suppression des documents trop petits, le corpus contient {len(id2doc)} documents.")

    str_corpus = " ".join([doc.text for doc in id2doc.values()])

    # Sauvegarde CSV

    docs_data = [(doc_id, doc.title, doc.author, doc.date, doc.url, doc.text) for doc_id, doc in id2doc.items()]
    df = pd.DataFrame(docs_data, columns=["id", "titre", "auteur", "date", "url", "texte"])
    df.to_csv(csv_filename, sep="\t", index=False)
    print(f"Données sauvegardées dans le fichier {csv_filename}")