import praw
import urllib.request
import xmltodict
import pandas as pd
import os
from dotenv import load_dotenv

# On voit si le fichier csv existe déjà

csv_filename = "data.csv"
if os.path.exists(csv_filename):
    df = pd.read_csv(csv_filename, sep="\t")
    print("Données chargées depuis le fichier CSV.")
else:
    print("Le fichier CSV n'existe pas. Interrogation des APIs...")

    # Chargement des variables d'environnement

    load_dotenv()
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT')

    # Chargement des données Reddit

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    subr = reddit.subreddit('Coronavirus')
    docs = []
    sources = []

    for post in subr.hot(limit=100):
        text = post.title + ". " + post.selftext  # titre + contenu textuel d'un post
        text = text.replace("\n", " ")
        docs.append(text)
        sources.append("Reddit")

    # Chargement des données Arxiv

    query = "covid"
    url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
    url_read = urllib.request.urlopen(url).read()
    data = url_read.decode()
    dico = xmltodict.parse(data)
    entries = dico['feed']['entry']

    for e in entries:
        text = e['title'] + ". " + e['summary']  # titre + résumé d'un post
        text = text.replace("\n", " ")
        docs.append(text)
        sources.append("Arxiv")

    # Création du DataFrame

    df = pd.DataFrame({
        "id": range(len(docs)),
        "text": docs,
        "source": sources
    })
    #print(df.head())

    # Sauvegarde dans un fichier CSV

    df.to_csv(csv_filename, sep="\t", index=False)
    print(f"Données sauvegardées dans le fichier {csv_filename}")