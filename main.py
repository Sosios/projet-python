import json
import html
import urllib.request
import urllib.parse
import xmltodict
import pandas as pd
import Document
import Author
import Corpus
import datetime

theme = "cinema"
docs = []
origines = []

# 1.1

url_hn = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
    {"query": theme, "tags": "story", "hitsPerPage": 50})
print(url_hn)

with urllib.request.urlopen(url_hn) as reponse:
    d_hn = json.load(reponse)

print(d_hn.keys())          
print(d_hn["nbHits"])        
hits = d_hn["hits"]
print(len(hits))             
print(hits[0].keys())        

id2doc = {}
id2aut = {}
i = 0

for hit in hits:
    
    texte = hit.get("story_text")
    if not texte:
        texte = hit.get("title", "")


    texte = html.unescape(texte).replace("<p>", " ").strip()
    docs.append(texte)
    origines.append("hackernews")
    dateStr = hit.get("created_at")
    dateTab = dateStr.split("-")
    date = datetime.datetime(int(dateTab[0]),int(dateTab[1]),int(dateTab[2].split("T")[0]))
    titre = hit.get("title")
    auteur = hit.get("author")
    url = hit.get("url")

    if auteur not in id2aut.keys():
        id2aut[auteur] = Author.Author(auteur)
    doc = Document.Document(titre,auteur,date,url,texte)
    id2doc[str(i)] = doc
    id2aut[auteur].add(doc)
    i += 1

print(id2doc["15"])
print(id2aut.keys())
print(id2aut["georgex7"])
id2aut["rcarmo"].present()


print("Documents Hacker News :", len(docs))

# 1.2
url_arxiv = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
    {"search_query": "all:" + theme, "start": 0, "max_results": 50})
print(url_arxiv)

with urllib.request.urlopen(url_arxiv) as reponse:
    d_arxiv = xmltodict.parse(reponse.read())

print(d_arxiv.keys())
print(d_arxiv["feed"].keys())    


entrees = d_arxiv["feed"].get("entry", [])
if isinstance(entrees, dict):
    entrees = [entrees]
print(len(entrees))
print(entrees[0].keys())         


for entree in entrees:
    texte = entree["summary"].replace("\n", " ").strip()
    docs.append(texte)
    dateStr = entree["published"]
    dateTab = dateStr.split("-")
    date = datetime.datetime(int(dateTab[0]),int(dateTab[1]),int(dateTab[2].split("T")[0]))
    titre = entree["title"]
    auteurs = entree["author"]
    if type(auteurs) is not list:
        auteurs = [auteurs]
    for auteur in auteurs:
        if auteur["name"] not in id2aut.keys():
            id2aut[auteur["name"]] = Author.Author(auteur["name"])
    url = entree["id"]
    doc = Document.Document(titre,auteurs[0]["name"],date,url,texte)
    id2doc[str(i)] = doc
    i += 1
    for auteur in auteurs:
        id2aut[auteur["name"]].add(doc)
    origines.append("arxiv")

print("Taille du corpus :", len(docs))

print(id2doc["15"])
print(id2aut.keys())
print(id2aut["georgex7"])
id2aut["rcarmo"].present()

# 2.1
df = pd.DataFrame({"id": range(len(docs)),
                   "texte": docs,
                   "origine": origines})
print(df.shape)
print(df.head())
print(df["origine"].value_counts())

# 2.2

df.to_csv("corpus.csv", sep="\t", index=False)

# 2.3
df = pd.read_csv("corpus.csv", sep="\t")
print(df.shape)


# 3.1
print("Nombre de documents :", len(df))

# 3.2
for texte in df["texte"]:
    mots = texte.split(" ")
    phrases = texte.split(".")
    print(len(mots), "mots,", len(phrases), "phrases")

# 3.3
print("Avant filtrage :", len(df))
df = df[df["texte"].str.len() >= 20]
print("Après filtrage :", len(df))

# 3.4
chaine = " ".join(df["texte"])
print(len(chaine))
print(chaine[:500])

#Implémentation de la classe corpus

id2aut["georgex7"].present()

corpus = Corpus.Corpus("Corpus cinéma", id2aut, id2doc)
corpus.sort_date(5)
corpus.sort_title(5)
print(corpus)
corpus.save("corpus.csv")
