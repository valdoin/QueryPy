import praw
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
user_agent = os.getenv('REDDIT_USER_AGENT') 
  
# Chargement des données reddit

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

subr = reddit.subreddit('Coronavirus')

docs=[]

for post in subr.hot(limit=100):
    texte = post.selftext # contenu textuel d'un post
    if not texte:  # si vide, on peut utiliser le titre comme alternative
        texte = post.title
    texte = texte.replace("\n", " ")
    docs.append(texte)

print(docs)