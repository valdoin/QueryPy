import ipywidgets as widgets
from IPython.display import display, clear_output


class SearchInterface:
    def __init__(self, search_engine):
        self.search_engine = search_engine
        self.label = widgets.Label("Moteur de recherche")
        self.text_input = widgets.Text(placeholder="Entrez vos mots-clés")
        self.author_input = widgets.Text(placeholder="Filtrer par auteur (optionnel)")
        self.year_input = widgets.Text(placeholder="Filtrer par année (optionnel, ex: 2023)")
        self.int_slider = widgets.IntSlider(
            value=10, min=1, max=30, step=1, description="Résultats"
        )
        self.button = widgets.Button(description="Rechercher")
        self.output = widgets.Output()

        self.interface = widgets.VBox(
            [
                self.label,
                self.text_input,
                self.author_input,
                self.year_input,
                self.int_slider,
                self.button,
                self.output,
            ]
        )

        self.button.on_click(self.click_button)

    def display(self):
        display(self.interface)

    def click_button(self, _):
        with self.output:
            clear_output()

            keywords = self.text_input.value.lower().split()
            top_n = self.int_slider.value
            author_filter = self.author_input.value
            year_filter = self.year_input.value
            year_filter = int(year_filter) if year_filter.isdigit() else None

            if keywords:
                print(f"Recherche pour les mots-clés : {keywords}")
                if author_filter:
                    print(f"Filtre d'auteur : {author_filter}")
                if year_filter:
                    print(f"Filtre d'année : {year_filter}")

                results = self.search_engine.search(
                    query_keywords=keywords,
                    top_n=top_n,
                    author_filter=author_filter,
                    year_filter=year_filter,
                )

                if not results.empty:
                    print("\nRésultats de la recherche :")
                    display(results[["Document ID", "Score", "Auteur", "Date", "Texte"]])
                else:
                    print("Aucun résultat trouvé.")
            else:
                print("Veuillez entrer des mots-clés.")