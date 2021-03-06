MyBay!
====

MyBay is a cross-platform local Pirate Bay "website".

It uses the recent [OpenBay Database Dump](http://openbay.isohunt.to/), generating a local SQLite database and allowing someone to search millions of magnet links using the command line.

How to Use
====

1. Make sure you have Python 2.7.* installed. You can download it [here](https://www.python.org/downloads/) (if you are on a Mac or Linux it
   should already be available). On Windows, you may have to add the Python directory to the PATH environment variable;

2. Download the project [here](https://github.com/mybay/mybay/archive/master.zip);

3. Unzip somewhere;

5. Download Pirate Bay's database dump (provided by OpenBay):
   - Magnet link here (paste it on your torrent app):<br>
     magnet:?xt=urn:btih:B3BCB8BD8B20DEC7A30FD9EC43CE7AFAAF631E06
   - Torrent file link [here](http://openbay.isohunt.to/files/openbay-db-dump.torrent)

6. Copy the torrents_mini.csv.gz file to the same folder where you unzipped MyBay;

7. Open you Terminal, cmd, etc, and cd to the directory where you unzipped MyBay;

8. Run "python mybay.py generate" to generate the magnet link database (it will take 5 to 10 minutes, but you only need to do it once);

9. Run "python mybay.py search yify planet apes" (or whatever you want);

10. Enjoy.

TODO
====

- Category filtering
- Create console-only mode (separate console and browser view)