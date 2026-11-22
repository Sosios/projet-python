class Document:
    def __init__(self,titre,auteur,date,url,texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
    def __str__(self):
        return self.titre

class HackerNewsDocument(Document):
    def __init__(self,titre,auteur,date,url,texte,ncom,points):
        super().__init__(titre=titre,auteur=auteur,date=date,url=url,texte=texte)
        self.ncom = ncom
        self.points = points
    def get_ncom(self):
        return self.ncom
    def get_points(self):
            return self.points

class ArxivDocument(Document):
    def __init__(self,titre,auteur,date,url,texte,comments,category):
        super().__init__(titre=titre,auteur=auteur,date=date,url=url,texte=texte)
        self.comments = comments
        self.category = category
    def get_comments(self):
        return self.comments
    def get_points(self):
            return self.category

