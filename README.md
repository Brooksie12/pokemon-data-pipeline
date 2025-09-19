Pokemon Data Pipeline: API -> CSV -> MySQL

Description:
My first data pipeline project is designed to explore collecting API data from the internet, clean the data selecting the information I specificially want and organise it into an appropriate data frame format and then exporting that format to a CSV file. Once I have the CSV file I can import the data into SQL to perform queries on the data. 

Background:
I chose to use Pokemon data for this project as this is a game series that I feel strong nostalgia for and there is easily accessible, abundant data on this to be collected. This is intended to be a fun but realistic project for working with real world data. I wanted to be able to select data primarily about the types of the pokemon and their stats so I can query the database around these values. Whenever I usually look up pokemon data I use a website called pokemon db which allows me to easily check the same stats that I am collecting for individual pokemon but it does not have any kind of comparison metric whereas my SQL table should be able to do things like compare the top 10 pokemon with the highest specific or total stats etc.

Features:
PokemonAPICollectAndCleaner:
-select a custom range of pokemon (based on national number/ID) to collect data for
-cleans the data selecting: national number (ID), name, height, weight, types (primary and secondary listed as type_1 and type_2), abilities, base stats (HP, ATK, DEF, SP_ATK, SP_DEF, Speed)
-exports the cleaned data to a CSV
-logs all info to a file pokemon.log

PokemonCSVIntoSQL
-loads CSV from a custom path 
-connects to a my SQL server 
-creates a database and table for the data to be entered into
-handles duplicates so they are not entered into the table
-logs all info into a file called pokemon_sql.log

Installation/Setup
-Clone the repository:
   ```bash
   git clone https://github.com/Brooksie12/pokemon-data-pipeline.git
   cd pokemon-data-pipeline
   ```

-set up a MYSQL local server to import the data into and create a user with permissions
-install dependencies (MySQL connector, pandas, requests): 
```bash
pip install -r requirements.txt
```
-Python version 3.10+

Usage
- run the API collector to fetch the data
    -input the ID of the pokemon at the start of the range you want to collect data for
    -input the ID of the pokemon at the end of the range you want to collect data for
    -input a file name for the CSV
    -program will save a CSV in the same folder as the file itself using your input name and with the data of the requested pokemon
Example: 
python PokemonAPICollectAndCleaner.py
# Example input:
# Start ID: 1
# End ID: 151
# CSV filename: kanto_pokemon.csv

-run the CSV to SQL file: 
    -input the name of the CSV file (if it is not saved in the same directory as the file then you have to specify the full path)
    -input the password to your local SQL server that you want the data to be stored in
    -File will input the CSV data into your local MySQL server, creating a database pokemon_db and inserting the data into a table pokemon
Example: 
python PokemonCSVIntoSQL.py
# Example input:
# CSV Filename: kanto_pokemon.csv
# MySQL password: MyPassword

Structure:
PokemonAPICollectAndCleaner.py   # Fetches Pokémon data from API and saves to CSV
PokemonCSVIntoSQL.py             # Loads CSV into MySQL
pokemon.log                      # Log file for API fetch
pokemon_sql.log                  # Log file for MySQL inserts
README.md                        # Documentation
requirements.txt                 # Python dependencies

Logging
- API data collection logs → `pokemon.log`
- MySQL data loading logs → `pokemon_sql.log`
Both include errors, warnings, and information messages.

References
PokeAPI: https://pokeapi.co
PokemonDB: https://pokemondb.net
Libraries: Pandas, MySQL Connector, Logging
