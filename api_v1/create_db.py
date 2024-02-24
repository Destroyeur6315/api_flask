import sqlite3

conn = sqlite3.connect('database.db')
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