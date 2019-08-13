# From Guess the Book project by Dmitry Dereshev. MIT Licence 2019.
# https://github.com/dmitry-dereshev/guess-the-book-public

# Basic text & visual analysis of the Gutenberg's catalogue: 
# authors, their years of birth/death, and lifespan.
# Works with a .csv table generated from 01_rdf_to_csv.py of this project.


import pandas as p # all data is set into DataFrames
import matplotlib.pyplot as plt # for graphs
import numpy as np # recommended to import separately from matplotlib
import datetime # helps with outrageous dates skeweing the graphics


def author_analysis(input_csv):
    # Authors column analysis
    data = p.read_csv(input_csv)
    #summarizes count by number of authors vs. nummber of titles
    author_title_disribution = data.groupby(['Author']).count()\
        .groupby(["Work_Title"]).count() 
    author_works = author_title_disribution['ID']
    author_works = p.DataFrame({'Number of Authors': author_works.values,\
         'Number of Works': author_works.index.values})
    print(author_works)
    print()


    # Plotting the above data
    plt.scatter(x=[author_works['Number of Works']],\
         y=[author_works['Number of Authors']])
    plt.xlabel('Number of Works')
    plt.ylabel('Number of Authors')
    plt.title("Number of Authors & Number of Works They Produced")
    plt.show()
    
def titles_analysis(input_csv):
    # Checking the work titles column for anomalies
    # Simple check for works that are named the same
    data = p.read_csv(input_csv)
    work_titles = data["Work_Title"]
    print('Total number of works:', len(work_titles))
    no_repeats = work_titles.drop_duplicates()
    print('Number of works with identical names:',\
        len(work_titles)-len(no_repeats))
    print('Duplicates by the same author:')
    # A further check to see if the duplicate books are by the same author
    work_titles_and_authors = data[["Author", "Work_Title"]]
    repeats = work_titles_and_authors.groupby("Work_Title").count()
    repeated_work_titles = repeats[repeats['Author']>1]
    duplicate_works = p.DataFrame({'Work Title': repeated_work_titles.index.values,\
         'Number of Works': repeated_work_titles.Author.values})
    print(duplicate_works)

def dates_analysis(input_csv):
    # Preliminary prep
    data = p.read_csv(input_csv)
    initial_data_length = max(len(data.Birthdate), len(data.Deathdate))
    data = data.dropna(subset=['Birthdate', 'Deathdate'])
    analysis_data_length = min(len(data.Birthdate), len(data.Deathdate))
    print('Dropped', initial_data_length-analysis_data_length,\
         'NaN items from the analysis\n')
    print("Statistical Description of Authors' Birthdates:")
    print(data.describe())

    # Plotting the results of the analysis
    date_analysis = data['Birthdate']
    plt.subplot(231)
    plt.hist(date_analysis.sort_values(), bins=100,\
         range=(min(data['Birthdate']), datetime.datetime.now().year))
    #plt.xlabel("Author's Year of Birth")
    plt.ylabel('Number of Authors')
    plt.title("Birth Years Overall")

    plt.subplot(232)
    plt.hist(date_analysis.sort_values(), bins=100,\
         range=(min(0, min(data['Birthdate'])), 1500))
    #plt.xlabel("Author's Year of Birth")
    #plt.ylabel('Number of Authors')
    plt.title("Birth Years Before 1500 CE")
    
    plt.subplot(233)
    plt.hist(date_analysis.sort_values(), bins=100, \
        range=(1500, datetime.datetime.now().year))
    #plt.xlabel("Author's Year of Birth")
    plt.ylabel('Number of Authors')
    plt.title("Birth Years After 1500 CE")
    

    date_analysis = data['Deathdate']
    plt.subplot(234)
    plt.hist(date_analysis.sort_values(), bins=100,\
         range=(min(data['Deathdate']), datetime.datetime.now().year))
    plt.xlabel("Author's Death Year")
    plt.ylabel('Number of Authors')
    plt.title("Death Years Overall")

    plt.subplot(235)
    plt.hist(date_analysis.sort_values(), bins=100,\
         range=(min(0, min(data['Deathdate'])), 1500))
    plt.xlabel("Author's Death Year")
    #plt.ylabel('Number of Authors')
    plt.title("Death Years Before 1500 CE")
    
    plt.subplot(236)
    plt.hist(date_analysis.sort_values(), bins=100, \
        range=(1500, datetime.datetime.now().year))
    plt.xlabel("Author's Death Year")
    plt.ylabel('Number of Authors')
    plt.title("Death Years After 1500 CE")
    plt.show()

def lifespan_analysis(input_csv):
    data = p.read_csv(input_csv)
    # Birth and death years together - lifespan analysis
    unique_authors = data.drop_duplicates(subset="Author")
    unique_authors["Lifespan"] = p.Series(unique_authors["Deathdate"]\
         - unique_authors["Birthdate"])

    #Setting up a lifespan of 120 years
    liveable_authors = unique_authors.loc[(unique_authors["Lifespan"] > 0)\
         & (unique_authors["Lifespan"]<121)]

    # Plotting the lifespan on a histogram
    plt.hist(liveable_authors["Lifespan"].sort_values(), bins=100)
    plt.show()

    young_authors = unique_authors.loc[(unique_authors["Lifespan"] > 0)\
         & (unique_authors["Lifespan"]<19)]
    print('Young Authors (0-18 years old):')
    print(young_authors[["Author", "Lifespan"]].sort_values(by="Lifespan")\
        .reset_index(drop=True))

# Path to the .csv file with metadata
input_csv = "path/to/.csv"

#author_analysis(input_csv)
#titles_analysis(input_csv)
#dates_analysis(input_csv)
#lifespan_analysis(input_csv)