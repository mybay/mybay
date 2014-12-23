# -*- coding: utf-8 -*-

import sqlite3
import os
import sys
import csv
import urllib
import gzip

from utils import log
import settings


def extract_csv_file():
    log('Extracting CSV file...')

    if not os.path.exists(settings.GZIP_FILE_NAME):
        log(settings.GZIP_FILE_NAME + ' was not found. You must download and copy this file to the current directory')
        exit()

    with gzip.open(settings.GZIP_FILE_NAME, 'rb') as in_f, open(settings.BROKEN_CSV_FILE_NAME, 'wb') as out_f:
        out_f.write(in_f.read())

    log('Done')


def fix_csv_file():
    log('Fixing CSV file...')

    # Remove null characters
    with open(settings.BROKEN_CSV_FILE_NAME, 'rb') as fi:
        data = fi.read()

    with open(settings.FIXED_CSV_FILE_NAME, 'wb') as fo:
        fo.write(data.replace('\x00', ''))

    log('Done')


def insert_line(cursor, line):
    # Add category (if it was not alerady added)
    category_name = buffer(line[4])

    sql = cursor.execute('''SELECT id FROM category WHERE name=?''', (
        category_name,
    ))

    if not cursor.fetchone():
        # Wasn't found. Insert
        sql = u"INSERT OR REPLACE INTO category (name) VALUES (?)"

        cursor.execute(sql, (
            category_name,
        ))

    # Add magnet

    # Unquote HTML ena escape SQL quotes
    name = urllib.unquote(line[0]).replace("'", "''")

    sql = u'''INSERT INTO magnet
              (name,magnet,size,category_id,seeders,leechers)
              VALUES (?,?,?,(SELECT id FROM category WHERE name=?),?,?)'''

    cursor.execute(sql, (
        buffer(name),     # name
        buffer(line[2]),  # magnet
        int(line[1]),     # size
        category_name,    # category
        int(line[5]),     # seeders
        int(line[6]),     # leechers
    ))


def create_and_populate_database():
    log('Creating database...')

    conn = sqlite3.connect(settings.DATABASE_FILE_NAME)
    cursor = conn.cursor()

    # Create magnets table
    cursor.execute('''CREATE TABLE magnet (
        id integer primary key,
        name text collate nocase,
        magnet text,
        size integer,
        category_id integer,
        seeders integer,
        leechers integer
    )''')

    # Create categories table
    cursor.execute('''CREATE TABLE category (
        id integer primary key,
        name text
    )''')

    log('Done')

    log('Populating database (this may take 5 to 10 minutes)...')

    with open(settings.FIXED_CSV_FILE_NAME, 'rb') as csv_file:
        lines = csv.reader(csv_file, delimiter='|', quotechar='"')

        for line in lines:
            insert_line(cursor, line)

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

    log('Done')


def delete_temp_files():
    log('Deleting temporary files...')

    os.remove(settings.BROKEN_CSV_FILE_NAME)
    os.remove(settings.FIXED_CSV_FILE_NAME)

    log('Done')


def run(custom_gzip_file_name=None):
    if custom_gzip_file_name:
        settings.GZIP_FILE_NAME = custom_gzip_file_name

    extract_csv_file()
    fix_csv_file()
    create_and_populate_database()
    delete_temp_files()
    log('MyBay is ready! You can delete %s if you want' % settings.GZIP_FILE_NAME)
