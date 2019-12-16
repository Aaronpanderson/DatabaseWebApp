Hello and thanks for looking at this repository.

This repository has populate and create sql scripts for creating a large database
with multiple relations of > 10,000 entries in a postgreSQL databse.

There is also a python script that utilizes bottle and pyscopg2 to connect to the
postgreSQL server and create a simple web app to read and write some of the data.
The web app has the following functionality:
Searching players by name, age, and team with wildcard support
Inserting a new player into the database.
Updating or editing player information in the database.
Deleting players from the database.
Viewing all matches the player has played in and the results of those matches.
Adding new matches for players to play in.

All these are achieved through SQL statements while connected to the postgreSQL
database with pyscopg2. There is a also a base level of input sanitation to make
sure no malicious inserts come through.

The website is made in HTML using a bootstrap front-edn framework.

Thanks for reading!
