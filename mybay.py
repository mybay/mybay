# -*- coding: utf-8 -*-

import sys
import tempfile
import webbrowser
import os

import search
import generate_db
from utils import log, size
import settings


def generate_html_file(term, results):
    html = """
    <html>
        <head>
            <title>MyBay - Search results for "{0}"</title>
            <style>

            h1 {{
                font-family: Georgia, serif;
            }}

            table.table2{{
                font-family: Georgia, serif;
                font-size: 18px;
                font-style: normal;
                font-weight: normal;
                line-height: 1.2em;
                border-collapse:collapse;
                text-align:center;
                width: 100%;
            }}

            .table2 thead th, .table2 tfoot td{{
                padding:20px 10px 40px 10px;
                color:#fff;
                font-size: 26px;
                background-color:#222;
                font-weight:normal;
                border-right:1px dotted #666;
                border-top:3px solid #666;
                -moz-box-shadow:0px -1px 4px #000;
                -webkit-box-shadow:0px -1px 4px #000;
                box-shadow:0px -1px 4px #000;
                text-shadow:0px 0px 1px #fff;
                text-shadow:1px 1px 1px #000;
            }}

            .table2 tfoot th{{
                padding:10px;
                font-size:18px;
                text-transform:uppercase;
                color:#888;
            }}

            .table2 tfoot td{{
                font-size:36px;
                color:#EF870E;
                border-top:none;
                border-bottom:3px solid #666;
                -moz-box-shadow:0px 1px 4px #000;
                -webkit-box-shadow:0px 1px 4px #000;
                box-shadow:0px 1px 4px #000;
            }}

            .table2 thead th:empty{{
                background:transparent;
                -moz-box-shadow:none;
                -webkit-box-shadow:none;
                box-shadow:none;
            }}

            .table2 thead :nth-last-child(1){{
                border-right:none;
            }}

            .table2 thead :first-child,
            .table2 tbody :nth-last-child(1){{
                border:none;
            }}

            .table2 tbody th{{
                text-align:left;
                padding:10px;
                color:#333;
                text-shadow:1px 1px 1px #ccc;
                background-color:#f9f9f9;
            }}

            .table2 tbody td{{
                padding:10px;
                background-color:#f0f0f0;
                border-right:1px dotted #999;
                text-shadow:-1px 1px 1px #fff;
                color:#333;
            }}

            </style>
        </head>

        <body>
            <h1>MyBay - Search results for "{0}"</h1>
            <table class="table2">
                <tr>
                    <th>Name</th>
                    <th>Size</th>
                    <th>SE</th>
                    <th>LE</th>
                </tr>
    """.format(term)

    for result in results:
        html += """
            <tr>
                <td>
                    <a href="magnet:?xt=urn:btih:{1}">
                        {0}
                    </a>
                </td>
                <td>{2}</td>
                <td>{3}</td>
                <td>{4}</td>
            </tr>
        """.format(result[0], result[1], size(result[2]), str(result[4]), str(result[5]))
    html += """
            </table>
        </body>
    </html>
    """

    # Create temp HTML file
    f = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    f.write(html)
    name = f.name
    f.close()

    return name


def run(terms):
    # Check if the magnet link database exists
    if not os.path.exists(settings.DATABASE_FILE_NAME):
        log('No database found. To generate a new database, use the "generate" parameter')
        exit()

    # Search!
    results = search.search(terms)

    # Create an HTML file and open it in the default browser
    name = generate_html_file(' '.join(terms), results)
    webbrowser.open('file://' + name)


if not len(sys.argv) > 1:
    print 'Invalid input.'
    exit()

if sys.argv[1] == 'generate':
    if os.path.exists(settings.DATABASE_FILE_NAME):
        log('A database already exists. Removing...')
        os.remove(settings.DATABASE_FILE_NAME)
        log('Done')

    log('Generating a new database...')

    if len(sys.argv) == 3:
        generate_db.run(sys.argv[2])
    else:
        generate_db.run()

elif sys.argv[1] == 'search':
    if len(sys.argv) == 2:
        print 'Missing search terms. Add at least one word after the search parameter.'
        exit()

    run(sys.argv[2:])

else:
    print 'Invalid input.'
    exit()
