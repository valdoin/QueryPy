class Document:
    """
    Classe de base représentant un document général.
    """

    def __init__(self, title="", author="", date="", url="", text=""):
        """
        Initialise un document avec un titre, un auteur, une date, une URL et un texte.

        Args:
            title (str): Titre du document.
            author (str): Auteur principal du document.
            date (str): Date de création ou publication du document (format YYYY/MM/DD).
            url (str): Lien URL du document.
            text (str): Contenu textuel du document.
        """
        self.title = title
        self.author = author
        self.date = date
        self.url = url
        self.text = text

    def __repr__(self):
        """
        Renvoie une représentation détaillée et formatée du document.

        Returns:
            str: Représentation détaillée du document.
        """
        return f"title : {self.title}\tauthor : {self.author}\tDate : {self.date}\tURL : {self.url}\ttext : {self.text}\t"

    def __str__(self):
        """
        Renvoie une représentation courte et lisible du document.

        Returns:
            str: Représentation courte (titre et auteur) du document.
        """
        return f"{self.title}, par {self.author}"


class DocumentFactory:
    """
    Fabrique de documents permettant de créer des instances de types spécifiques
    comme `RedditDocument` ou `ArxivDocument`.
    """

    @staticmethod
    def create_document(doc_type, **kwargs):
        """
        Crée un document spécifique en fonction du type fourni.

        Args:
            doc_type (str): Type de document à créer ("Reddit" ou "Arxiv").
            **kwargs: Attributs spécifiques pour initialiser le document.

        Returns:
            Document: Instance de document créée.

        Raises:
            ValueError: Si le type de document est inconnu.
        """
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
    """
    Classe représentant un document provenant de Reddit, avec un compteur de commentaires.
    """

    def __init__(self, title="", author="", date="", url="", text="", num_comments=0):
        """
        Initialise un document Reddit avec des attributs spécifiques.

        Args:
            title (str): Titre du document.
            author (str): Auteur du document.
            date (str): Date de création (format YYYY/MM/DD).
            url (str): Lien URL du document.
            text (str): Contenu textuel du document.
            num_comments (int): Nombre de commentaires sur le post Reddit.
        """
        super().__init__(title, author, date, url, text)
        self.num_comments = num_comments

    def get_type(self):
        """
        Retourne le type du document.

        Returns:
            str: Type "Reddit".
        """
        return "Reddit"

    def get_num_comments(self):
        """
        Retourne le nombre de commentaires du document.

        Returns:
            int: Nombre de commentaires.
        """
        return self.num_comments

    def set_num_comments(self, num_comments):
        """
        Définit le nombre de commentaires du document.

        Args:
            num_comments (int): Nouveau nombre de commentaires.

        Raises:
            ValueError: Si `num_comments` n'est pas un entier.
        """
        if isinstance(num_comments, int):
            self.num_comments = num_comments
        else:
            raise ValueError("num_comments doit être un entier.")

    def __str__(self):
        """
        Renvoie une représentation courte du document Reddit.

        Returns:
            str: Titre, auteur et nombre de commentaires.
        """
        return f"{super().__str__()} | Nombre de commentaires : {self.num_comments}"


class ArxivDocument(Document):
    """
    Classe représentant un document provenant d'ArXiv, avec des co-auteurs.
    """

    def __init__(self, title, author, co_authors, date, url, text):
        """
        Initialise un document ArXiv avec des attributs spécifiques.

        Args:
            title (str): Titre du document.
            author (str): Auteur principal du document.
            co_authors (list): Liste des co-auteurs.
            date (str): Date de publication (format YYYY/MM/DD).
            url (str): Lien URL du document.
            text (str): Contenu textuel du document.
        """
        super().__init__(title, author, date, url, text)
        self.co_authors = co_authors

    def get_type(self):
        """
        Retourne le type du document.

        Returns:
            str: Type "Arxiv".
        """
        return "Arxiv"

    def get_co_authors(self):
        """
        Retourne la liste des co-auteurs.

        Returns:
            list: Liste des co-auteurs.
        """
        return self.co_authors

    def set_co_authors(self, co_authors):
        """
        Définit la liste des co-auteurs.

        Args:
            co_authors (list): Nouvelle liste de co-auteurs.

        Raises:
            ValueError: Si `co_authors` n'est pas une liste.
        """
        if isinstance(co_authors, list):
            self.co_authors = co_authors
        else:
            raise ValueError("co_authors doit être une liste de noms.")

    def __repr__(self):
        """
        Renvoie une représentation détaillée du document ArXiv.

        Returns:
            str: Représentation détaillée avec co-auteurs et autres attributs.
        """
        co_authors_str = ", ".join(self.co_authors) if self.co_authors else "Aucun"
        return (
            f"Titre : {self.title}\tAuteur : {self.author}\tCo-auteurs : {co_authors_str}\t"
            f"Date : {self.date}\tURL : {self.url}\tTexte : {self.text}\t"
        )