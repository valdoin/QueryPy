class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []

    def add(self, production):
        self.ndoc += 1
        self.production.append(production)

    def display_stats(self):
        valid_texts = [doc.text for doc in self.production if isinstance(doc.text, str)]
        average_docs_size = (
            sum(len(text.split()) for text in valid_texts) / len(valid_texts)
            if valid_texts else 0
        )
        print(f"Statistiques pour {self.name} :")
        print(f"  Nombre de documents produits : {self.ndoc}")
        print(f"  Taille moyenne des documents : {average_docs_size:.0f} mots")

    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"
