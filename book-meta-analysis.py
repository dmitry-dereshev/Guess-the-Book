# From Guess the Book project by Dmitry Dereshev. MIT Licence 2019.

# Basic text & visual analysis of the Gutenberg's catalogue: 
# authors, their years of birth/death, and book titles.


import pandas as p # all data is set into DataFrames
import matplotlib.pyplot as plt # for graphs
import numpy as np # recommended to import separately from matplotlib


#=========================================
# Removes all rows with empty cells from the set
data = p.read_csv("path/to/.csv/with/metadata/as/a/single/table")
all_rows = data.dropna() # removes all rows with empty cells
all_rows.to_csv("data/with/no/empty/cells/out")
#=========================================


#=========================================
# Load the cleaned-up dataset to check for anomalies in each column
data = p.read_csv("path/to/clean/.csv/with/metadata/as/a/single/table")
#=========================================


#=========================================
# Authors column analysis
author_analysis = data.groupby(['Author']).count() # summarizes count by author
print(author_analysis.sort_values(by=["Work_Title"], ascending=False)["Work_Title"]) # sorts authors by the number of works they produced
author_title_disribution = author_analysis.groupby(["Work_Title"]).count() #summarizes count by number of authors vs. nummber of titles
#=========================================


#=========================================
# Dates of birth column analysis
print(author_title_disribution["Birthdate"])

plt.plot(author_title_disribution["Birthdate"], 'o', label='Works Produced')
plt.xlabel('Number of Works')
plt.ylabel('Number of Authors')
plt.title("Number of Authors vs. Number of Works They Produced")
plt.show()

date_analysis = data['Birthdate']
n, bins, patches = plt.hist(date_analysis.sort_values(), bins=28, range=(-830, 1970))
plt.show()
print(n, bins)

# Allows for a numerical idea about who was born when.
date_analysis = p.concat([data['Birthdate'], data["Work_Title"]], axis=1)
plt.plot(date_analysis.groupby(["Birthdate"]).count(), 'o')
plt.show()
#=========================================


#=========================================
# Death dates analysis
date_analysis = data['Deathdate']

n, bins, patches = plt.hist(date_analysis.sort_values(), bins=100, range=(1500, 2000))
plt.show()
print(n, bins)

# Allows to have a numerical idea about who was died when.
date_analysis = p.concat([data['Deathdate'], data["Work_Title"]], axis=1)
plt.plot(date_analysis.groupby(["Deathdate"]).count(), 'o')
plt.show()
#=========================================


#=========================================
# Birth and death years together - lifespan analysis
unique_authors = data.drop_duplicates(subset="Author")
unique_authors["Lifespan"] = p.Series(unique_authors["Deathdate"] - unique_authors["Birthdate"])

#Setting up a lifespan of 100 years
liveable_authors = unique_authors.loc[(unique_authors["Lifespan"] > 0) & (unique_authors["Lifespan"]<100)]

# Plotting the lifespan on a histogram
plt.hist(liveable_authors["Lifespan"].sort_values(), bins=100)
plt.show()

young_authors = unique_authors.loc[(unique_authors["Lifespan"] > 0) & (unique_authors["Lifespan"]<19)]
print(young_authors[["Author", "Lifespan"]].sort_values(by="Lifespan").reset_index(drop=True))
#=========================================


#=========================================
# Checking the work titles column for anomalies

# Simple check for works that are named the same
work_titles = data["Work_Title"]
print(len(work_titles))
print(work_titles.head())
no_repeats = work_titles.drop_duplicates()
print(len(no_repeats))
print(no_repeats.head())

# A further check to see if the duplicate books are by the same author
work_titles_and_authors = data[["Author", "Work_Title"]]
repeats = work_titles_and_authors.groupby("Work_Title").count()
print(repeats.sort_values(by="Author", ascending=False))

# Check if an author has consistent birth/death dates across their works.
print(data[data["Author"] == "Shakespeare, William"].drop_duplicates(subset=["Birthdate", "Deathdate"]).count())