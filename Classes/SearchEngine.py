import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from utils import remove_stopwords


class SearchEngine:
    """
    Classe implémentant un moteur de recherche basé sur un corpus.
    """

    def __init__(self, corpus):
        """
        Initialise le moteur de recherche avec un corpus donné.

        Args:
            corpus (Corpus): Le corpus à utiliser pour la recherche.
        """
        self.corpus = corpus
        self.vocab, self.mat_TF = self.build_term_document_matrix()
        self.mat_TFxIDF = self.build_tfidf_matrix()

    def build_term_document_matrix(self):
        """
        Construit une matrice terme-document (TF) à partir du corpus.

        Returns:
            tuple:
                - vocab (dict): Dictionnaire associant chaque mot à un index unique.
                - mat_TF (csr_matrix): Matrice sparse représentant les fréquences des mots dans les documents.
        """
        vocab = {}
        rows, cols, data = [], [], []

        for doc_id, doc in self.corpus.id2doc.items():
            word_counts = {}
            words = remove_stopwords(doc.text.lower()).split()

            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1

            for word, count in word_counts.items():
                if word not in vocab:
                    vocab[word] = len(vocab)
                rows.append(doc_id)
                cols.append(vocab[word])
                data.append(count)

        mat_TF = csr_matrix(
            (data, (rows, cols)), shape=(len(self.corpus.id2doc), len(vocab))
        )
        return vocab, mat_TF

    def build_tfidf_matrix(self):
        """
        Construit une matrice TF-IDF à partir de la matrice TF.

        Returns:
            csr_matrix: Matrice sparse représentant les scores TF-IDF.
        """
        doc_count = np.array((self.mat_TF > 0).sum(axis=0)).flatten()
        idf = np.log((1 + self.mat_TF.shape[0]) / (1 + doc_count)) + 1
        tf = self.mat_TF.copy().toarray()
        tfidf = tf * idf
        return csr_matrix(tfidf)

    def search(self, query_keywords, top_n=10, author_filter=None, year_filter=None):
        """
        Recherche les documents les plus pertinents en fonction de mots-clés et de filtres optionnels.

        Args:
            query_keywords (list): Liste de mots-clés pour la recherche.
            top_n (int, optional): Nombre maximum de documents à retourner. Par défaut, 10.
            author_filter (str, optional): Filtrer les résultats par auteur. Par défaut, aucun filtre.
            year_filter (int, optional): Filtrer les résultats par année. Par défaut, aucun filtre.

        Returns:
            pd.DataFrame: Résultats de la recherche sous forme de DataFrame contenant les colonnes :
                          - "Document ID"
                          - "Score"
                          - "Auteur"
                          - "Date"
                          - "Texte"
        """
        query_vector = np.zeros(len(self.vocab))
        for word in query_keywords:
            if word in self.vocab:
                query_vector[self.vocab[word]] = 1

        similarities = cosine_similarity(
            self.mat_TFxIDF, query_vector.reshape(1, -1)
        ).flatten()
        top_indices = similarities.argsort()[-top_n:][::-1]
        results = []

        for idx in top_indices:
            doc = self.corpus.id2doc[idx]
            if author_filter and author_filter.lower() not in doc.author.lower():
                continue
            if year_filter:
                doc_year = int(doc.date.split("/")[0])
                if doc_year != year_filter:
                    continue

            results.append(
                {
                    "Document ID": idx,
                    "Score": similarities[idx],
                    "Auteur": doc.author,
                    "Date": doc.date,
                    "Texte": doc.text,
                }
            )

        return pd.DataFrame(results)