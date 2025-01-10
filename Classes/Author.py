class Author:
    """
    Classe représentant un auteur et sa production documentaire.
    """

    def __init__(self, name):
        """
        Initialise un auteur avec un nom, un compteur de documents, et une liste de productions.

        Args:
            name (str): Nom de l'auteur.
        """
        self.name = name
        self.ndoc = 0
        self.production = []

    def add(self, production):
        """
        Ajoute une production documentaire à l'auteur.

        Args:
            production: Un document produit par l'auteur.
        """
        self.ndoc += 1
        self.production.append(production)

    def display_stats(self):
        """
        Affiche des statistiques sur les documents produits par l'auteur :
        - Nombre total de documents.
        - Taille moyenne (en mots) des documents.
        """
        valid_texts = [doc.text for doc in self.production if isinstance(doc.text, str)]
        average_docs_size = (
            sum(len(text.split()) for text in valid_texts) / len(valid_texts)
            if valid_texts
            else 0
        )
        print(f"Statistiques pour {self.name} :")
        print(f"  Nombre de documents produits : {self.ndoc}")
        print(f"  Taille moyenne des documents : {average_docs_size:.0f} mots")

    def __str__(self):
        """
        Renvoie une représentation textuelle de l'auteur, incluant son nom et
        le nombre de documents produits.

        Returns:
            str: Représentation textuelle de l'auteur.
        """
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"