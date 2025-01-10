from Classes.Corpus import Corpus
from Classes.SearchEngine import SearchEngine
from Classes.Document import RedditDocument

### Tests pour la classe SearchEngine ###
def test_search_engine_initialization():
    Corpus.reset_instance()
    corpus = Corpus("Test Corpus")
    doc = RedditDocument(
        "Test Title", "Test Author", "2022/01/01", "http://test.url", "Test text", 5
    )
    corpus.add_document(doc)
    search_engine = SearchEngine(corpus)
    assert len(search_engine.vocab) > 0
    assert search_engine.mat_TF.shape[0] == 1


def test_search_engine_build_tfidf_matrix():
    Corpus.reset_instance()
    corpus = Corpus("Test Corpus")
    doc = RedditDocument(
        "Test Title",
        "Test Author",
        "2022/01/01",
        "http://test.url",
        "Text with repeated words words words",
        5,
    )
    corpus.add_document(doc)
    search_engine = SearchEngine(corpus)
    assert search_engine.mat_TFxIDF.shape[0] == 1
    assert search_engine.mat_TFxIDF.shape[1] > 0


def test_search_engine_search():
    Corpus.reset_instance()
    corpus = Corpus("Test Corpus")
    doc1 = RedditDocument(
        "Title 1", "Author 1", "2022/01/01", "http://url1", "Text about AI and ML", 5
    )
    doc2 = RedditDocument(
        "Title 2", "Author 2", "2022/01/02", "http://url2", "More about AI", 10
    )
    corpus.add_document(doc1)
    corpus.add_document(doc2)
    search_engine = SearchEngine(corpus)
    results = search_engine.search(["AI"])
    assert len(results) == 2
    assert "AI" in results.iloc[0]["Texte"]


def test_search_engine_with_filters():
    Corpus.reset_instance()
    corpus = Corpus("Test Corpus")
    doc1 = RedditDocument(
        "Title 1", "Author 1", "2022/01/01", "http://url1", "Text about AI", 5
    )
    doc2 = RedditDocument(
        "Title 2", "Author 2", "2023/01/01", "http://url2", "More about AI", 10
    )
    corpus.add_document(doc1)
    corpus.add_document(doc2)
    search_engine = SearchEngine(corpus)
    results = search_engine.search(["AI"], author_filter="Author 1", year_filter=2022)
    assert len(results) == 1
    assert results.iloc[0]["Auteur"] == "Author 1"
    assert results.iloc[0]["Date"] == "2022/01/01"