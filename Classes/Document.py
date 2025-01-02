class Document:
    def __init__(self, title="", author="", date="", url="", text=""):
        self.title = title
        self.author = author
        self.date = date
        self.url = url
        self.text = text

    def __repr__(self):
        return f"title : {self.title}\tauthor : {self.author}\tDate : {self.date}\tURL : {self.url}\ttext : {self.text}\t"

    def __str__(self):
        return f"{self.title}, par {self.author}"
    

class DocumentFactory:
    @staticmethod
    def create_document(doc_type, **kwargs):
        if doc_type == "Reddit":
            return RedditDocument(
                title=kwargs.get("title", ""),
                author=kwargs.get("author", ""),
                date=kwargs.get("date", ""),
                url=kwargs.get("url", ""),
                text=kwargs.get("text", ""),
                num_comments=kwargs.get("num_comments", 0),
            )
        elif doc_type == "Arxiv":
            return ArxivDocument(
                title=kwargs.get("title", ""),
                author=kwargs.get("main_author", ""),
                co_authors=kwargs.get("co_authors", []),
                date=kwargs.get("date", ""),
                url=kwargs.get("url", ""),
                text=kwargs.get("text", ""),
            )
        else:
            raise ValueError(f"Type de document inconnu : {doc_type}")


class RedditDocument(Document):
    def __init__(self, title="", author="", date="", url="", text="", num_comments=0):
        super().__init__(title, author, date, url, text)
        self.num_comments = num_comments

    def get_type(self):
        return "Reddit"

    def get_num_comments(self):
        return self.num_comments

    def set_num_comments(self, num_comments):
        if isinstance(num_comments, int):
            self.num_comments = num_comments
        else:
            raise ValueError("num_comments doit être un entier.")

    def __str__(self):
        return f"{super().__str__()} | Nombre de commentaires : {self.num_comments}"


class ArxivDocument(Document):
    def __init__(self, title, author, co_authors, date, url, text):
        super().__init__(title, author, date, url, text)
        self.co_authors = co_authors

    def get_type(self):
        return "Arxiv"
    
    def get_co_authors(self):
        return self._co_authors

    def set_co_authors(self, co_authors):
        if isinstance(co_authors, list):
            self._co_authors = co_authors
        else:
            raise ValueError("co_authors doit être une liste de noms.")

    def __repr__(self):
        co_authors_str = ", ".join(self.co_authors) if self.co_authors else "Aucun"
        return (
            f"title : {self.title}\tmain_author : {self.author}\tco_authors : {co_authors_str}\t"
            f"Date : {self.date}\tURL : {self.url}\ttext : {self.text}\t"
        )