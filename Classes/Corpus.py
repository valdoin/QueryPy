import pandas as pd
from Classes.Document import Document
from Classes.Author import Author
from datetime import datetime
import os
from dotenv import load_dotenv
import praw
import urllib.request
import xmltodict

class Corpus:
    def __init__(self, name):
        self.name = name
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add_document(self, document):
        self.id2doc[self.ndoc] = document
        self.ndoc += 1

        authors = document.author.split(", ") if ", " in document.author else [document.author]
        for author_name in authors:
            if author_name not in self.authors:
                self.authors[author_name] = Author(author_name)
                self.naut += 1
            self.authors[author_name].add(document)


    def generate_corpus(self):
        load_dotenv()
        client_id = os.getenv('REDDIT_CLIENT_ID')
        client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        user_agent = os.getenv('REDDIT_USER_AGENT')

        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        subreddit_name = "Coronavirus"
        subr = reddit.subreddit(subreddit_name)

        # Extraction des données Reddit
        print("Extraction des données depuis Reddit...")
        for post in subr.hot(limit=20):
            title = post.title
            author = post.author.name if post.author else "Inconnu"
            date = datetime.fromtimestamp(post.created).strftime("%Y/%m/%d")
            url = "https://www.reddit.com" + post.permalink
            text = post.selftext.replace("\n", " ")

            doc = Document(title, author, date, url, text)
            self.add_document(doc)

        # Extraction des données ArXiv
        print("Extraction des données depuis ArXiv...")
        query = "covid"
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=20"
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
            self.add_document(doc)

        print(f"Corpus généré avec succès : {self.ndoc} documents ajoutés.")

    def load_from_csv(self, csv_filename):
        try:
            df = pd.read_csv(csv_filename, sep="\t")
            for _, row in df.iterrows():
                doc = Document(row['titre'], row['auteur'], row['date'], row['url'], row['texte'])
                self.add_document(doc)
            print(f"Corpus chargé avec succès depuis {csv_filename}.")
        except Exception as e:
            print(f"Erreur lors du chargement de {csv_filename} : {e}")

    def save_to_csv(self, csv_filename):
        try:
            data = [
                {"id": doc_id, "titre": doc.title, "auteur": doc.author, "date": doc.date, "url": doc.url, "texte": doc.text}
                for doc_id, doc in self.id2doc.items()
            ]
            df = pd.DataFrame(data)
            df.to_csv(csv_filename, sep="\t", index=False)
            print(f"Corpus sauvegardé avec succès dans {csv_filename}.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde dans {csv_filename} : {e}")

    def display_sorted_by_date(self, n=None):
        sorted_docs = sorted(self.id2doc.values(), key=lambda doc: datetime.strptime(doc.date, "%Y/%m/%d"), reverse=True)
        for doc in sorted_docs[:n]:
            print(f"{doc.date} - {doc.title} (Auteur(s) : {doc.author})")

    def display_sorted_by_title(self, n=None):
        sorted_docs = sorted(self.id2doc.values(), key=lambda doc: doc.title)
        for doc in sorted_docs[:n]:
            print(f"{doc.title} - {doc.date} (Auteur(s) : {doc.author})")

    def __repr__(self):
        return (
            f"Corpus '{self.name}':\n"
            f"  - Nombre de documents : {self.ndoc}\n"
            f"  - Nombre d'auteurs : {self.naut}\n"
        )