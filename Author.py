class Author:
    def __init__(self,name):
        self.name = name
        self.ndoc = 0
        self.production = {}
    def add(self,doc):
        self.production[str(self.ndoc)] = doc
        self.ndoc += 1
    def __str__(self):
        return self.name
    def present(self):
        print("Nom de l'auteur : "+str(self.name))
        print("Nombre de documents produits : "+str(self.ndoc))
        if self.ndoc > 0:
            total = 0
            for doc in self.production.values():
                total += len(doc.texte)
            average = total / self.ndoc
        print("Longueur moyenne : "+str(average))