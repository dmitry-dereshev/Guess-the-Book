# Project Guess the Book Scripts
Scripts from Guess the Book project - training an AI to guess author names based on symbol frequency of their works.

The scripts work based on Project Gutenberg's library of public domain works. You can download the metadata about the books here: http://www.gutenberg.org/wiki/Gutenberg:Offline_Catalogs
And the instructions about how to get the actual books here: http://www.gutenberg.org/wiki/Gutenberg:Mirroring_How-To (mirroring the site) and here: http://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages (downloading a specific subset of books).

Included scripts:

01_rdf_to_csv.py: 
Takes a path where .rdf/xml files are stored, extracts author names, years of birth & death, and titles of their works, puts them into a Pandas dataframe, and saves them as a .csv file in the location of your choice.

02_book-metadata_analysis:
Takes in the .csv generated by 01_rdf_to_csv.py, and runs basic analysis on author names and numbers, their birth/death years, and lifespan (+ some sanity checking).

03_frequentize.py:
Takes a path where .txt files are stored, returns a .csv with symbol frequency table, one row per .txt file.

04_merge.py:
Merges the data from 01_rdf_to_csv.py and 03_frequentize.py into a single table, cleans empty entries.
