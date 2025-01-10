# QueryPy

## Description du projet

Cette application permet d'explorer et d'analyser un corpus de documents provenant de Reddit et d'Arxiv. L'objectif principal est de fournir une plateforme intuitive pour rechercher, filtrer, et analyser des contenus textuels à l'aide d'une interface interactive basée sur Jupyter Notebook.

---

## Configuration initiale

Avant d'utiliser l'application, vous devez configurer un fichier `.env` dans le répertoire racine pour permettre l'accès à l'API Reddit. Voici un exemple de fichier `.env` :

```
REDDIT_CLIENT_ID=xxxx
REDDIT_CLIENT_SECRET=xxxx
REDDIT_USER_AGENT=xxxxx
```
N'hésitez pas à me contacter si vous rencontrez des difficultés pour la configuration du .env.

Vous devez également installer les dépendances avec la commande suivante :

```bash
pip install -r requirements.txt
```


---

## Fonctionnalités principales

1. **Extraction de corpus** :
   - Collecte des posts les plus populaires sur Reddit en fonction d'un sujet donné.
   - Importation des publications Arxiv basées sur des mots-clés spécifiques.

2. **Recherche textuelle** :
   - Recherche par mots-clés avec options de filtrage par auteur ou par année.

3. **Analyse textuelle** :
   - Calcul des statistiques comme les mots les plus fréquents et les concordances pour un mot-clé donné.

4. **Interface utilisateur interactive** :
   - Basée sur Jupyter Notebook avec widgets pour une exploration intuitive.

---

## Tests unitaires

Des tests unitaires sont fournis pour valider les principales classes et fonctions de l'application. Vous pouvez les exécuter avec la commande suivante :

```bash
python -m pytest Tests/searchengine_tests.py Tests/corpus_tests.py Tests/author_tests.py
```

Assurez-vous que toutes les dépendances nécessaires sont installées avant de lancer les tests.

---

## Utilisation

### Exploration des fonctions TDs

Toutes les fonctions implémentées au cours des TDs sont regroupées dans le fichier `main.py`. Vous pouvez exécuter ce fichier pour tester les différentes fonctionnalités comme la recherche, l'analyse textuelle, et la gestion des auteurs.

### Lancement de l'interface utilisateur

L'interface utilisateur est disponible dans le fichier `main.ipynb`. Cette interface permet de :
- Rechercher des documents par mots-clés.
- Appliquer des filtres par auteur ou par année.
- Visualiser les résultats dans un tableau.
---