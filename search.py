# -*- coding: utf-8 -*-

import sqlite3
import settings


# A search result
class Result(object):
    def __init__(self, name, magnet, size, se, le):
        # Result info
        self.name = name
        self.magnet = magnet
        self.size = size
        self.se = se
        self.le = le


def search(search_terms):
    global filtered_terms
    global result_list

    result_list = []

    # Remove all terms with two or less characters, and lowercase everything
    filtered_terms = [t.lower() for t in search_terms if len(t) > 2]

    print 'Performing search (it can take a while)...'

    if not len(filtered_terms):
        return []

    conn = sqlite3.connect(settings.DATABASE_FILE_NAME)
    cursor = conn.cursor()

    sql = '''
        SELECT m.name, m.magnet, m.size, c.name, m.seeders, m.leechers
        FROM magnet m, category c
        WHERE m.category_id = c.id
    '''

    for term in filtered_terms:
        sql += ''' AND m.name LIKE '%{0}%' '''.format(term)

    sql += ''' ORDER BY seeders DESC '''

    cursor.execute(sql)

    return cursor.fetchall()
