from Classes.Corpus import Corpus
from Classes.Document import RedditDocument

### Tests pour la classe Corpus ###
def test_corpus_initialization():
    Corpus.reset_instance()
    corpus = Corpus("Test Corpus")
    assert corpus.name == "Test Corpus"
    assert corpus.ndoc == 0
    assert corpus.naut == 0
    assert corpus.authors == {}


def test_corpus_add_document():
    Corpus.reset_instance()
    corpus = Corpus("Test Corpus")
    doc = RedditDocument(
        "Test Title", "Test Author", "2022/01/01", "http://test.url", "Test text", 5
    )
    corpus.add_document(doc)
    assert corpus.ndoc == 1
    assert "Test Author" in corpus.authors
    assert corpus.authors["Test Author"].ndoc == 1


def test_corpus_save_and_load_json(tmp_path):
    Corpus.reset_instance()
    corpus = Corpus("Test Corpus")
    doc = RedditDocument(
        "Test Title", "Test Author", "2022/01/01", "http://test.url", "Test text", 5
    )
    corpus.add_document(doc)
    json_file = tmp_path / "test_corpus.json"
    corpus.save_to_json(json_file)
    Corpus.reset_instance()
    new_corpus = Corpus("New Corpus")
    new_corpus.load_from_json(json_file)
    assert new_corpus.ndoc == 1
    assert "Test Author" in new_corpus.authors


def test_corpus_display_sorted_by_date(capsys):
    Corpus.reset_instance()
    corpus = Corpus("Test Corpus")
    doc1 = RedditDocument(
        "Title 1", "Author 1", "2023/01/01", "http://url1", "Text 1", 5
    )
    doc2 = RedditDocument(
        "Title 2", "Author 2", "2022/01/01", "http://url2", "Text 2", 5
    )
    corpus.add_document(doc1)
    corpus.add_document(doc2)
    corpus.display_sorted_by_date()
    captured = capsys.readouterr()
    assert "2023/01/01 - Title 1" in captured.out
    assert "2022/01/01 - Title 2" in captured.out