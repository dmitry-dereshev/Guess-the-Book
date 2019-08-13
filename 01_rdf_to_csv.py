# From Guess the Book project by Dmitry Dereshev. MIT Licence 2019.
# https://github.com/dmitry-dereshev/guess-the-book-public

# Takes in a bunch of .rdf files from a given folder, extracts info from them, 
# puts that info into a Pandas DataFrame, then stores it as a csv.
#
# INPUT:
#   input_path: the top folder where .rdf/xml files are 
#               (script check for sufolders automatically).
#   
#   output_path: where you want the finished .csv file to land.
#   
#   verbose: an optional parameter which prints out the steps of the process.
#            useful for large batches of files. To turn off, set it to 0.
#
# This script may be slow for large collections, but does the job eventually.


import rdflib # to decypher .rdf format into plain text triplets
import os # to build a file list to process by rdflib.
import pandas # to save the resulting table as a .csv for analysis


def rdf_to_csv(input_path, output_path, verbose=1):
    # Lists all file paths in a given directory, checks for subfolders as well.
    if verbose==1:
        print("Parsing the paths of .rdf/xml through os.path...")
    rdffiles = [os.path.join(root, name)
        for root, dirs, files in os.walk(input_path)
        for name in files]

    # Initializes the dataframe where all extracted metadata will be stored.
    if verbose==1:
        print("Initializing the DataFrame...")
    book_data = pandas.DataFrame(index = range(len(rdffiles)),\
        columns=["ID",\
            "Author",\
            "Birthdate",\
            "Deathdate",\
            "Work_Title"])
    rdf_len = len(rdffiles)-1
    # keeps track of IDs & cycles, so that the
    # data appends to the dataframe correctly, even if some values are missing.
    counter = -1 

    for path in rdffiles:
        counter +=1
        if verbose==1:
            print("adding rdf %s of %s" % (counter, rdf_len))
        # Initializes the graph. Also, empties the graph in each cycle
        library_graph=rdflib.Graph() 
        library_graph.parse(path, format='application/rdf+xml')
        book_data.loc[counter].ID = os.path.basename(path)
        # Runs through every triplet within an .rdf file, looks for author, 
        # dates of birth and death, and the title of the work
        for s,p,o in library_graph:
            # appends author name if it's there, if not - leaves an empty cell.
            if "pgterms/name" in p:
                book_data.loc[counter].Author = (str(o)) 
            # appends birth date if it's there, if not - leaves an empty cell.
            elif "birthdate" in p:
                book_data.loc[counter].Birthdate = (str(o)) 
            # appends death date if it's there, if not - leaves an empty cell.
            elif "deathdate" in p:
                book_data.loc[counter].Deathdate = (str(o))
            # appends book title if it's there, if not - leaves an empty cell.
            elif "terms/title" in p:
                book_data.loc[counter].Work_Title = (str(o))
    
    # Showers the header of the dataset to check for correct data extraction.
    if verbose==1:
        print("Top 5 entries in the dataset:")
        print(book_data.head())
    # Saves the .csv with the extracted data.
    book_data.to_csv(output_path, index=False)



# Point at the top folder with .rdf files
input_path = 'path/to/top/folder/with/.rdf/files'

# Point at where you want the extracted data to be saved
output_path = 'path/to/output/file.csv'

#rdf_to_csv(input_path, output_path)
