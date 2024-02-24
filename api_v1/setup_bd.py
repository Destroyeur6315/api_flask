import sqlite3
import csv

name_db = "database.db"

def create_table(name_db):
    conn = sqlite3.connect(name_db)
    print("Connected to databse Successfully")

    conn.execute('CREATE TABLE article( \
                        id_article INT PRIMARY KEY, \
                        reference varchar(255) NOT NULL, \
                        code_article varchar(255) NOT NULL, \
                        article_nom varchar(255))')

    conn.execute('CREATE TABLE dossier( \
                        id_dossier INT PRIMARY KEY, \
                        num_dossier varchar(255) NOT NULL, \
                        date date, \
                        id_article INT REFERENCES article)')

    print("Create Table Dossier and Article with success")

    conn.close()

def insert_data(name_bd):
    conn = sqlite3.connect(name_bd)
    cur = conn.cursor()

    ## ARTICLE
    with open('./data/data_article.csv') as f:
        reader = csv.reader(f, delimiter=";")
        data = list(reader)

    if data:
        data.pop(0)

    for row in data:
        cur.execute("INSERT INTO article \
                    (id_article, reference, code_article, article_nom) VALUES (?, ?, ?, ?)", row)

    print("Insert data to Article Successfully")

    ## DOSSIER
    with open('./data/data_dossier.csv') as f:
        reader = csv.reader(f, delimiter=";")
        data = list(reader)

    if data:
        data.pop(0)

    i = 1
    for row in data:
        cur.execute("INSERT INTO dossier \
                    (id_dossier, num_dossier, date, id_article) VALUES (?, ?, ?, ?)", (i, row[0], row[1], row[2]))
        i += 1

    print("Insert data to dossier Successfully")

    conn.commit()
    conn.close()

create_table(name_db)
insert_data(name_db)