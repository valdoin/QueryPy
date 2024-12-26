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
