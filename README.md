# Project Guess the Book Scripts
Scripts from Guess the Book project - training an AI to guess author names based on symbol frequency of their works.

The scripts work based on Project Gutenberg's library of public domain works. You can download the metadata about the books here: http://www.gutenberg.org/wiki/Gutenberg:Offline_Catalogs
And the instructions about how to get the actual books here: http://www.gutenberg.org/wiki/Gutenberg:Mirroring_How-To (mirroring the site) and here: http://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages (downloading a specific subset of books).

Included scripts:
- rdf-to-csv.py: takes a path where .rdf/xml files are stored, extracts author names, years of birth & death, and titles of their works, puts them into a Pandas dataframe, and saves them as a .csv file in the location of your choice.

What you'll need:

- rdflib: https://github.com/RDFLib/rdflib
- pandas: http://pandas.pydata.org

-- WARNING: this script is not optimised. It may take a while to process the workload depending on the number of .rdf/xml files, and the capabilities of your machine. However, it does the job eventually, if you leave it to it.
