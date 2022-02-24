import sqlite3

from collections import defaultdict


def creaTable(path: str, fonction: str):

    def Date_rendez_vous():
        txt = '''CREATE TABLE Date_rendez_vous (NAME TEXT PRIMARY KEY, DATE TEXT, TEMPS TEXT, CLIENT TEXT, ADRESSE TEXT)'''
        return txt

    def Clients():
        text = '''CREATE TABLE Clients (name PRIMARY KEY, adresse TEXT)'''
        return text

    listTache = []
    listTable = []

    if fonction == 'All':
        listTache.append(Date_rendez_vous())
        listTache.append(Clients())
    elif fonction == 'Date_rendez_vous':
        listTache.append(Date_rendez_vous())
    elif fonction == 'Clients':
        listTache.append(Clients())

    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        for item in listTache:
            cursor.execute(item)
        txt = "SELECT name FROM sqlite_master WHERE type='table';"
        cursor.execute(txt)
        rows = cursor.fetchall()
        for row in rows:
            listTable.append(row[0])
    cursor.close()

    return listTable


def readTable(path: str, listTable: list):

    data = defaultdict(lambda: defaultdict(lambda: None))
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        for table in listTable:

            txt = 'PRAGMA table_info(' + table + ')'
            cursor.execute(txt)
            rows = cursor.fetchall()

            primary = '0'
            for row in rows:
                if row[5] == 1:
                    primary = row[1]
                    break

            txt = 'Select * from ' + table
            try:
                cursor.execute(txt)
            except sqlite3.OperationalError:
                creaTable(path=path, fonction=table)
                cursor.execute(txt)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]

            if len(rows) == 0:
                dictio = dict.fromkeys(columns, 'None')
                key = dictio[primary]
                data[table] = {key: dictio}
            else:
                for row in rows:
                    dictio = dict(zip(columns, row))
                    key = dictio[primary]

                    data[table][key] = dictio
            print('Table ' + table + ' lu')
    cursor.close()

    return data


def insertTable(path: str, table: str, value: dict):

    insert = ['?'] * len(value)
    insert = ', '.join(insert)

    listValue = list(value.values())

    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()

        txt = 'INSERT INTO ' + table + ' VALUES (' + insert + ')'
        try:
            cursor.execute(txt, listValue)
            make = True
        except sqlite3.IntegrityError:
            print('Erreur duplication de clef primaire dans la table : ' + table)
            make = False
    cursor.close()

    data = readTable(path=path, listTable=[table])

    return data, make


def deleteTable(path: str, table: str, primaryKey: str):

    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        txt = 'PRAGMA table_info(' + table + ')'
        cursor.execute(txt)
        rows = cursor.fetchall()

        primary = None
        for row in rows:
            if row[5] == 1:
                primary = row[1]
                break

        txt = 'DELETE FROM ' + table + ' WHERE ' + primary + ' = "' + primaryKey + '"'
        cursor.execute(txt)
    cursor.close()

    data = readTable(path=path, listTable=[table])

    return data, True
