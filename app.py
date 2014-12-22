#!/usr/bin/python

import sys
import tempfile
import webbrowser
import os
import sys
from threading import Thread

from Tkinter import Tk, Frame, Entry, Label, Button, TOP, BOTTOM, DISABLED, ACTIVE
import tkMessageBox

import filesize
from search import Search

DATABASE_FILE_NAME = 'torrents_mini.csv'

if len(sys.argv) > 1:
    DATABASE_FILE_NAME = sys.argv[1]

# Check if the magnet database exists
if not os.path.exists(DATABASE_FILE_NAME):
    print 'ERROR: Database file "' + DATABASE_FILE_NAME + '" not found.'
    exit()


class SearchThread(Thread):
    def __init__(self, app, term):
        Thread.__init__(self)
        # The App instance
        self.app = app

        # The search term
        self.term = term

    def run(self):
        search = Search(DATABASE_FILE_NAME)

        # Search!
        result_list = search.search(self.term)

        # Create an HTML file and open it in the default browser
        name = self.generate_html_file(result_list)
        webbrowser.open('file://' + name)

        # Re-enable the search button
        self.app.button.config(text='Search', state=ACTIVE)

    def generate_html_file(self, result_list):
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
                <h1>Search results for "{0}"</h1>
                <table class="table2">
                    <tr>
                        <th>Name</th>
                        <th>Size</th>
                        <th>SE</th>
                        <th>LE</th>
                    </tr>
        """.format(self.term)

        for result in result_list:
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
            """.format(result.name, result.magnet, filesize.size(result.size), str(result.se), str(result.le))

        html += """
                </table>
            </body>
        </html>
        """

        # &tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.istole.it%3A6969&tr=udp%3A%2F%2Ftracker.ccc.de%3A80

        # Create temp HTML file
        f = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        f.write(html)
        name = f.name
        f.close()

        return name


class App:
    def __init__(self, parent):
        # Create frame, buttons, etc
        self.f = Frame(parent)
        self.f.pack(padx=15, pady=15)

        self.search_label = Label(self.f, text="Enter the search terms below:")
        self.search_label.pack(side=TOP, padx=10, pady=10)

        self.entry = Entry(self.f)
        self.entry.pack(side=TOP, padx=10, pady=12)
        self.entry.bind("<Key>", self.key)
        self.entry.focus_set()

        self.exit = Button(self.f, text="Exit", command=self.f.quit)
        self.exit.pack(side=BOTTOM, padx=10, pady=10)

        self.button = Button(self.f, text="Search", command=self.search)
        self.button.pack(side=BOTTOM, padx=10, pady=10)

    def key(self, event):
        # If ENTER was pressed, search
        if event.char == '\r':
            self.search()

    def search(self):
        # If there's something to search, search!
        if self.entry.get() != '':
            self.button.config(text='Searching (it can take a while)...', state=DISABLED)

            th = SearchThread(self, self.entry.get())
            th.start()
        else:
            tkMessageBox.showinfo('Hey', 'You should type something in the search. That\'s the point, really...')


root = Tk()
root.title('MyBay')
app = App(root)

# If on Mac OS, bring the window to top
if sys.platform == 'darwin':
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

root.mainloop()
