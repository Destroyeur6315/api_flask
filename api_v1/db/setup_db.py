import sqlite3
import csv

name_db = "database.db"

# Function which create 2 tables : item and file
def create_table(name_db):
    conn = sqlite3.connect(name_db)
    print("Connected to databse Successfully")

    conn.execute('CREATE TABLE item( \
                        id INT PRIMARY KEY, \
                        reference varchar(255) NOT NULL, \
                        item_code varchar(255) NOT NULL, \
                        item_name varchar(255))')

    conn.execute('CREATE TABLE file( \
                        id INT PRIMARY KEY, \
                        num_file varchar(255) NOT NULL, \
                        date date, \
                        id_item INT REFERENCES article)')

    print("Create Table file and item with success")

    conn.close()

# Function which insert data from .csv
def insert_data(name_bd):
    conn = sqlite3.connect(name_bd)
    cur = conn.cursor()

    ## ITEM
    with open('data/data_item.csv') as f:
        reader = csv.reader(f, delimiter=";")
        data = list(reader)

    if data:
        data.pop(0)

    for row in data:
        cur.execute("INSERT INTO item \
                    (id, reference, item_code, item_name) VALUES (?, ?, ?, ?)", row)

    print("Insert data to item Successfully")

    ## FILE
    with open('data/data_file.csv') as f:
        reader = csv.reader(f, delimiter=";")
        data = list(reader)

    if data:
        data.pop(0)

    i = 1
    for row in data:
        cur.execute("INSERT INTO file \
                    (id, num_file, date, id_item) VALUES (?, ?, ?, ?)", (i, row[0], row[1], row[2]))
        i += 1

    print("Insert data to file Successfully")

    conn.commit()
    conn.close()

create_table(name_db)
insert_data(name_db)