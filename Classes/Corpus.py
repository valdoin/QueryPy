from Classes.Document import RedditDocument, ArxivDocument
from Classes.Author import Author
from datetime import datetime
import pandas as pd
import json
import re
import os
from dotenv import load_dotenv
import praw
import urllib.request
import xmltodict
from utils import (
    count_document_frequency,
    build_vocabulary,
    count_occurrences,
    remove_stopwords,
)


class SingletonMeta(type):
    """
    Métaclasse pour implémenter le patron de conception Singleton.
    Garantit qu'une seule instance d'une classe utilisant cette métaclasse
    sera créée.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Retourne l'instance existante si elle existe, sinon en crée une nouvelle.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Corpus(metaclass=SingletonMeta):
    """
    Classe représentant un corpus contenant un ensemble de documents.
    Implémente un singleton pour éviter la duplication d'instances.
    """

    def __init__(self, name):
        """
        Initialise un corpus avec un nom, des auteurs, et des documents.

        Args:
            name (str): Nom du corpus.
        """
        if not hasattr(self, "initialized"):
            self.name = name
            self.authors = {}
            self.id2doc = {}
            self.ndoc = 0
            self.naut = 0
            self.full_text = None
            self.initialized = True

    @classmethod
    def reset_instance(cls):
        """
        Réinitialise l'instance du singleton.
        Utilisé principalement pour faciliter les tests unitaires.
        """
        if cls in cls._instances:
            del cls._instances[cls]

    def add_document(self, document):
        """
        Ajoute un document au corpus et met à jour les informations des auteurs.

        Args:
            document (Document): Document à ajouter.
        """
        self.id2doc[self.ndoc] = document
        self.ndoc += 1

        authors = [document.author]
        if isinstance(document, ArxivDocument):
            authors += document.co_authors

        for author_name in authors:
            if author_name not in self.authors:
                self.authors[author_name] = Author(author_name)
                self.naut += 1
            self.authors[author_name].add(document)

    def generate_corpus(self, user_query):
        """
        Génère un corpus à partir de données provenant de Reddit et ArXiv.

        Args:
            user_query (str): Sujet ou requête utilisateur pour filtrer les données.
        """
        load_dotenv()
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT")

        reddit = praw.Reddit(
            client_id=client_id, client_secret=client_secret, user_agent=user_agent
        )
        subreddit_name = user_query
        subr = reddit.subreddit(subreddit_name)

        print("Extraction des données depuis Reddit...")
        for post in subr.hot(limit=50):
            title = post.title
            author = post.author.name if post.author else "Inconnu"
            date = datetime.fromtimestamp(post.created).strftime("%Y/%m/%d")
            url = "https://www.reddit.com" + post.permalink
            text = post.selftext.replace("\n", " ")
            num_comments = post.num_comments
            doc = RedditDocument(title, author, date, url, text, num_comments)
            self.add_document(doc)

        print("Extraction des données depuis ArXiv...")
        query = user_query
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=50"
        url_read = urllib.request.urlopen(url).read()
        data = url_read.decode()
        dico = xmltodict.parse(data)
        entries = dico["feed"]["entry"]

        for e in entries:
            title = e["title"]
            authors = e.get("author", [])
            if isinstance(authors, list):
                authors = [a.get("name", "Inconnu") for a in authors]
            elif isinstance(authors, dict):
                authors = [authors.get("name", "Inconnu")]
            main_author = authors[0] if authors else "Inconnu"
            co_authors = authors[1:] if len(authors) > 1 else []
            date = datetime.strptime(e["published"], "%Y-%m-%dT%H:%M:%SZ").strftime(
                "%Y/%m/%d"
            )
            url = e["id"]
            text = e["summary"].replace("\n", " ")
            doc = ArxivDocument(title, main_author, co_authors, date, url, text)
            self.add_document(doc)

        print(f"Corpus généré avec succès : {self.ndoc} documents ajoutés.")

    def save_to_json(self, json_filename):
        """
        Sauvegarde le corpus dans un fichier JSON.

        Args:
            json_filename (str): Nom du fichier JSON.
        """
        try:
            data = {"Reddit": [], "Arxiv": []}

            for doc_id, doc in self.id2doc.items():
                if doc.get_type() == "Reddit":
                    data["Reddit"].append(
                        {
                            "id": doc_id,
                            "title": doc.title,
                            "author": doc.author,
                            "date": doc.date,
                            "url": doc.url,
                            "text": doc.text,
                            "num_comments": doc.num_comments,
                        }
                    )
                elif doc.get_type() == "Arxiv":
                    data["Arxiv"].append(
                        {
                            "id": doc_id,
                            "title": doc.title,
                            "main_author": doc.author,
                            "co_authors": doc.co_authors,
                            "date": doc.date,
                            "url": doc.url,
                            "text": doc.text,
                        }
                    )

                with open(json_filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Corpus sauvegardé avec succès dans {json_filename}.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde dans {json_filename} : {e}")

    def load_from_json(self, json_filename):
        """
        Charge un corpus à partir d'un fichier JSON.

        Args:
            json_filename (str): Nom du fichier JSON.
        """
        try:
            with open(json_filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "Reddit" in data:
                for row in data["Reddit"]:
                    doc = RedditDocument(
                        title=row["title"],
                        author=row["author"],
                        date=row["date"],
                        url=row["url"],
                        text=row["text"],
                        num_comments=row["num_comments"],
                    )
                    self.add_document(doc)

            if "Arxiv" in data:
                for row in data["Arxiv"]:
                    doc = ArxivDocument(
                        title=row["title"],
                        author=row["main_author"],
                        co_authors=row["co_authors"],
                        date=row["date"],
                        url=row["url"],
                        text=row["text"],
                    )
                    self.add_document(doc)

            print(f"Corpus chargé avec succès depuis {json_filename}.")
        except Exception as e:
            print(f"Erreur lors du chargement depuis {json_filename} : {e}")

    def display_sorted_by_date(self, n=None):
        """
        Affiche les documents du corpus triés par date.

        Args:
            n (int, optional): Nombre de documents à afficher. Affiche tous les documents si None.
        """
        sorted_docs = sorted(
            self.id2doc.values(),
            key=lambda doc: datetime.strptime(doc.date, "%Y/%m/%d"),
            reverse=True,
        )
        for doc in sorted_docs[:n]:
            print(f"{doc.date} - {doc.title} (Auteur(s) : {doc.author})")

    def display_sorted_by_title(self, n=None):
        """
        Affiche les documents du corpus triés par titre.

        Args:
            n (int, optional): Nombre de documents à afficher. Affiche tous les documents si None.
        """
        sorted_docs = sorted(self.id2doc.values(), key=lambda doc: doc.title)
        for doc in sorted_docs[:n]:
            print(f"{doc.title} - {doc.date} (Auteur(s) : {doc.author})")

    def search(self, keyword):
        """
        Recherche des occurrences d'un mot-clé dans le corpus.

        Args:
            keyword (str): Mot-clé à rechercher.
        """
        if not self.full_text:
            self.full_text = "\n".join(doc.text for doc in self.id2doc.values())

        pattern = rf"(.{{0,30}}{re.escape(keyword)}.{{0,30}})"
        matches = re.findall(pattern, self.full_text, re.IGNORECASE)

        if matches:
            print(f"{len(matches)} occurence(s) trouvée(s) pour '{keyword}':\n")
            for match in matches:
                print(f"...{match}...")
        else:
            print(f"Aucune occurrence trouvée pour '{keyword}'.")

    def concorde(self, keyword, context_size=15):
        """
        Génère un concordancier pour un mot-clé.

        Args:
            keyword (str): Mot-clé à analyser.
            context_size (int): Taille du contexte autour du mot-clé.
        """
        concordances = []

        if not self.full_text:
            self.full_text = "\n".join(doc.text for doc in self.id2doc.values())

        pattern = re.compile(
            rf"(.{{0,{context_size}}})({re.escape(keyword)})(.{{0,{context_size}}})"
        )

        for match in pattern.finditer(self.full_text):
            left_context = match.group(1).strip()
            found_keyword = match.group(2)
            right_context = match.group(3).strip()

            concordances.append(
                {
                    "Contexte gauche": "..." + left_context,
                    "Motif trouvé": found_keyword,
                    "Contexte droit": right_context + "...",
                }
            )

        df_concordancier = pd.DataFrame(concordances)
        print("\nConcordancier :")
        print(df_concordancier)

    def stats(self, n=10):
        """
        Affiche des statistiques textuelles sur le corpus.

        Args:
            n (int): Nombre de mots les plus fréquents à afficher.
        """
        if not self.full_text:
            self.full_text = "\n".join(doc.text for doc in self.id2doc.values())

        filtered_text = remove_stopwords(self.full_text)
        vocabulary = build_vocabulary(filtered_text)
        occurrences = count_occurrences(filtered_text)
        print(
            f"Nombre de mots différents dans le corpus (sans stop words) : {len(vocabulary)}"
        )

        frequent_words = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)[
            :n
        ]
        print(f"Les {n} mots les plus fréquents (sans stop words) :")
        for word, freq in frequent_words:
            print(f"  - {word} : {freq} occurrences")

        documents = [remove_stopwords(doc.text) for doc in self.id2doc.values()]
        document_frequency = count_document_frequency(documents)

        tab = pd.DataFrame(
            {
                "Mot": list(occurrences.keys()),
                "Fréquence": list(occurrences.values()),
                "Fréquence de documents": [
                    document_frequency.get(word, 0) for word in occurrences.keys()
                ],
            }
        )

        tab = tab.sort_values(by="Fréquence", ascending=False)

        print("\nTableau des fréquences :")
        print(tab)

    def __repr__(self):
        """
        Représentation textuelle du corpus.

        Returns:
            str: Représentation textuelle.
        """
        return (
            f"Corpus '{self.name}':\n"
            f"  - Nombre de documents : {self.ndoc}\n"
            f"  - Nombre d'auteurs : {self.naut}\n"
        )