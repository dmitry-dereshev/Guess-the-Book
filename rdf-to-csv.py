# From Guess the Book project by Dmitry Dereshev. MIT Licence 2019.

# Point this script at the top folder containing .rdf/xml files (metadata) from Project Gutenberg,
# and it will recursively compile a list of paths for each .rdf/xml file,
# then proceed to extract author names, their years of birth and death, and their book titles.

# WARNING: this script is unoptimised, so it may be slow, but it does the job eventually.


import rdflib # to decypher .rdf format into plain text triplets
import os # to build a file list to process by rdflib.
import pandas # to save the resulting table as a .csv for analysis


#=======================
# Lists all file paths in a given directory
path = 'path/to/top/folder/with/.rdf/xml' # point at the top folder with .rdf files
rdffiles = [os.path.join(root, name)
             for root, dirs, files in os.walk(path) # checks for all subfolders as well.
             for name in files]
#=======================


#=======================
# Initializes the dataframe where all extracted metadata will be stored.
book_data = pandas.DataFrame(index = range(len(rdffiles)), columns=["Author", "Birthdate", "Deathdate", "Work_Title"])
counter = -1 # keeps track of cycles, so that data appends to the dataframe correctly, even if some items are missing


for path in rdffiles:
    counter +=1
    library_graph=rdflib.Graph() # initializes the graph. Also, empties the graph in each cycle
    library_graph.parse(path, format='application/rdf+xml') # adds an .rdf file from the path to the graph g
                            # mime type 'application/rdf+xml' is the correct one for the rdfs from Project Gutenberg
    for s,p,o in library_graph: # runs through every triple within an .rdf file, looks for author, dates of birth and death, and the title of the work
        if "pgterms/name" in p:
            book_data.loc[counter].Author = (str(o)) # appends author name if it's there, if not - leaves an empty cell
        elif "birthdate" in p:
            book_data.loc[counter].Birthdate = (str(o)) # appends birth date if it's there, if not - leaves an empty cell
        elif "deathdate" in p:
            book_data.loc[counter].Deathdate = (str(o)) # appends death date if it's there, if not - leaves an empty cell
        elif "terms/title" in p:
            book_data.loc[counter].Work_Title = (str(o)) # appends title of the work if it's there, if not - leaves an empty cell
#=======================

print(book_data.head()) # a test to see that the data has been processed correctly.
book_data.to_csv('path/to/save/the/.csv/file', index=False) # save the .csv to work on it later.
