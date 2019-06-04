import csv
import pandas as pd
from .models import Book, Cluster
path='/Users/emsud/Documents/Linkable/datafile/'


def createtable():
    with open(path+"data.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p=Book(title=row['Title'],node=row['Node'],sellnum=row['Sellnum'],autor=row['Autor'],discription=row['Description'],location=row['Location'], imagesource=row['ImageUrl'])
            p.save()


def createtable2():
    data = pd.read_csv(path + "c.csv", header=None, encoding='CP949')

    for i in range(len(data)):
        id1 = []
        for j in range(len(data[i]) - 1):
            if data[i][j + 1] == "0":
                break
            id1.append(int(data[i][j + 1]))
        p = Cluster(category=data[i][0], cluster=id1)
        p.save()