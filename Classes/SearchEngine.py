import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from utils import remove_stopwords


class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus
        self.vocab, self.mat_TF = self.build_term_document_matrix()
        self.mat_TFxIDF = self.build_tfidf_matrix()

    def build_term_document_matrix(self):
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
        doc_count = np.array((self.mat_TF > 0).sum(axis=0)).flatten()
        idf = np.log((1 + self.mat_TF.shape[0]) / (1 + doc_count)) + 1
        tf = self.mat_TF.copy().toarray()
        tfidf = tf * idf
        return csr_matrix(tfidf)

    def search(self, query_keywords, top_n=10):
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
            results.append(
                {
                    "Document ID": idx,
                    "Score": similarities[idx],
                    "Texte": self.corpus.id2doc[idx].text,
                }
            )

        return pd.DataFrame(results)