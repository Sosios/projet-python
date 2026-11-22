import pandas as pd
import Document
import Author
class Corpus:
    def __init__(self,nom,authors,id2doc):
        self.name = nom
        self.authors = authors
        self.id2doc = id2doc
        self.ndoc = len(id2doc)
        self.naut = len(authors)
    def sort_date(self, n):
        tri = sorted(self.id2doc.items(), key=lambda item: item[1].date)
        for id, doc in tri[:n]:
            print(id, " : ", doc, ", ", doc.date)

    def sort_title(self, n):    
        tri = sorted(self.id2doc.items(), key=lambda item: item[1].titre.lower())
        for id, doc in tri[:n]:
            print(id, " : ", doc, ", ", doc.date)
    def __repr__(self):
        return f"Corpus '{self.name}' : {self.ndoc} documents, {self.naut} auteurs"
    def save(self,chemin):
        df = pd.DataFrame({"id": list(self.id2doc.keys()),
                   "titre": [d.titre for d in self.id2doc.values()],
                   "auteur": [d.auteur for d in self.id2doc.values()],
                   "date": [d.date for d in self.id2doc.values()],
                   "url": [d.url for d in self.id2doc.values()],
                   "texte": [d.texte for d in self.id2doc.values()]})
        df.to_csv(chemin, sep="\t", index=False)
    def load(self,chemin):
        df = pd.read_csv(chemin, sep="\t")
        id2doc = {}
        id2aut = {}
        i = 0
        for _,ligne in df.iterrows():
            titre = ligne["titre"]
            auteur = ligne["auteur"]
            date = ligne["date"]
            url = ligne["url"]
            texte = ligne["texte"]

            if auteur not in self.id2aut.keys():
                self.id2aut[auteur] = Author.Author(auteur)
            doc = Document.Document(titre,auteur,date,url,texte)
            self.id2doc[str(i)] = doc
            self.id2aut[auteur].add(doc)
            i += 1

