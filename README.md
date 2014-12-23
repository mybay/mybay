MyBay!
====

MyBay is a cross-platform local Pirate Bay "website".

It uses the recent [OpenBay Database Dump](http://openbay.isohunt.to/), generating a local SQLite database and allowing someone to search millions of magnet links using the command line.

How to Use
====

1. Make sure you have Python 2.7.* installed. You can download it [here](https://www.python.org/downloads/) (if you are on a Mac or Linux it
   should already be available)

2. Download the project [here](https://github.com/mybay/mybay/archive/master.zip)

3. Unzip somewhere

5. Download Pirate Bay's database dump (provided by OpenBay). 
   - Magnet link here (paste it on your torrent app):<br>
     magnet:?xt=urn:btih:B3BCB8BD8B20DEC7A30FD9EC43CE7AFAAF631E06
   - Torrent file link [here](http://openbay.isohunt.to/files/openbay-db-dump.torrent)

6. Copy the gz file to the same folder where you unzipped MyBay.

7. Run "python mybay.py generate" to generate the magnet link database (you only need to do this once)

8. Run "python mybay.py search yify planet apes" (or whatever you want)

9. Enjoy

