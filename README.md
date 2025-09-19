Pokemon Data Collector and Cleaner plus MySQL Data Loader

Description:
My first data pipeline project is designed to explore collecting API data from the internet, clean the data selecting the information I specificially want and organise it into an appropriate data frame format and then exporting that format to a CSV file. Once I have the CSV file I can import the data into SQL to perform queries on the data. 

I chose to use Pokemon data for this project as this is a game series that I feel strong nostalgia for and there is easily accessible, abundant data on this to be collected. I wanted to be able to select data primarily about the types of the pokemon and their stats so I can query the database around these values. Whenever I usually look up pokemon data I use a website called pokemon db which allows me to easily check the same stats that I am collecting for individual pokemon but it does not have any kind of comparison metric whereas my SQL table should be able to do things like compare the top 10 pokemon with the highest specific or total stats etc.

Features:
PokemonAPICollectAndCleaner:
-ability to select a custom range of pokemon (based on national number/ID) to collect data for
-cleans the data selecting: national number (ID), name, height, weight, types (primary and secondary listed as type_1 and type_2), abilities, base stats (HP, ATK, DEF, SP_ATK, SP_DEF, Speed)

Installation/Setup

Usage

Structure

Logging

References

