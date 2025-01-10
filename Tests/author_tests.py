from Classes.Author import Author
from Classes.Document import RedditDocument

### Tests pour la classe Author ###
def test_author_initialization():
    author = Author("Test Author")
    assert author.name == "Test Author"
    assert author.ndoc == 0
    assert author.production == []


def test_author_add_production():
    author = Author("Test Author")
    doc = RedditDocument(
        "Test Title", "Test Author", "2022/01/01", "http://test.url", "Test text", 5
    )
    author.add(doc)
    assert author.ndoc == 1
    assert len(author.production) == 1
    assert author.production[0] == doc


def test_author_display_stats(capsys):
    author = Author("Test Author")
    doc1 = RedditDocument(
        "Title 1", "Test Author", "2022/01/01", "http://url1", "Some short text", 5
    )
    doc2 = RedditDocument(
        "Title 2",
        "Test Author",
        "2022/01/02",
        "http://url2",
        "Another longer text here",
        10,
    )
    author.add(doc1)
    author.add(doc2)
    author.display_stats()
    captured = capsys.readouterr()
    assert "Nombre de documents produits : 2" in captured.out
    assert "Taille moyenne des documents : 4 mots" in captured.out


def test_author_str():
    author = Author("Test Author")
    assert str(author) == "Auteur : Test Author\t# productions : 0"