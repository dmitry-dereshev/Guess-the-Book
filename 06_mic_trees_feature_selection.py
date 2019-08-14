# Part of Guess the Book project by Dmitry Dereshev. MIT Licence 2019.
# https://github.com/dmitry-dereshev/guess-the-book-public

# Takes in the split sets from 05_scaling_splitting_sets.py, identifies top
# features based on mutual info classifier and classification trees, and saves
# the new datasets with those features.

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import ExtraTreesClassifier


def mic_feature_selection(data_in, data_out):
    # Creates a list of all paths to .csv files
    csv_files = [os.path.join(root, name)
                for root, dirs, files in os.walk(data_in) 
                for name in files]
    
    
    # Goes through every .csv identified in csv_files and creates a relevant
    # dataset.
    counter = 0
    for csv_file in csv_files:
        counter += 1
    
        data = pd.read_csv(csv_file, index_col="ID")
        data = data.fillna(0)

        # Calculates the number of features, given the number of books per 
        # author in the dataset
        count_books_per_author = data.groupby(['Author']).count()
        count_books_per_author = count_books_per_author.Birthdate
        num_of_features = int(count_books_per_author.iloc[0]/5)

        x = data.iloc[:, 4:] # letter frequencies
        y = data.iloc[:, 0] # authors

        #Mutual Info Classifier
        print('Selecting features for dataset #', counter, 'of', len(csv_files))
        x_new = mutual_info_classif(x, y)
        select_columns = pd.DataFrame(data={'Column_Names': x.columns.values,\
             'MIC': x_new})
        needed_columns = select_columns.sort_values(by='MIC', ascending=False)
        needed_features = needed_columns.head(num_of_features)
        needed_features = needed_features.Column_Names.apply(str).tolist()
        data = data.loc[:, needed_features]
        data.insert(loc=0, column='Author', value=y)

        path_out = data_out+'/'+'mic '+str(num_of_features)+' features.csv'
        data.to_csv(path_out, index='ID')

        



def trees_feature_selection(data_in, data_out):
    # Creates a list of all paths to .csv files
    csv_files = [os.path.join(root, name)
                for root, dirs, files in os.walk(data_in) 
                for name in files]
    
    # Goes through every .csv identified in csv_files and creates a relevant
    # dataset.
    counter = 0
    for csv_file in csv_files:
        counter += 1
    
        data = pd.read_csv(csv_file, index_col="ID")
        data = data.fillna(0)

        # Calculates the number of features, given the number of books per 
        # author in the dataset
        count_books_per_author = data.groupby(['Author']).count()

        count_books_per_author = count_books_per_author.Birthdate
        num_of_features = int(count_books_per_author.iloc[0]/5)

        x = data.iloc[:, 4:] # letter frequencies
        y = data.iloc[:, 0] # authors
        # Build a forest and compute the feature importances
        print('Selecting features for dataset #', counter, 'of', len(csv_files))
        forest = ExtraTreesClassifier(n_estimators=250, max_features="sqrt",
                                    random_state=0)

        forest.fit(x, y)
        importances = forest.feature_importances_
        select_columns = pd.DataFrame(data={'Column_Names': x.columns.values,\
             'Trees': importances})
        needed_columns = select_columns.sort_values(by='Trees', ascending=False)
        needed_features = needed_columns.head(num_of_features)
        needed_features = needed_features.Column_Names.apply(str).tolist()
        data = data.loc[:, needed_features]
        data.insert(loc=0, column='Author', value=y)

        path_out = data_out+'/'+'trees '+str(num_of_features)+' features.csv'
        data.to_csv(path_out, index='ID')





# Path to folder with .csv files from 05_scaling_splitting_sets
path_to_csv = "D:/Downloads/2019 Software Code/2019 Python Code/Guess the Book Project/guess-the-book-data-software/.01 Data/Data Prep & Cleaning/scaled tests"
# Path to where the resulting sets should land
path_to_output ="D:/Downloads/2019 Software Code/2019 Python Code/Guess the Book Project/guess-the-book-data-software/.01 Data/Data Prep & Cleaning/scaled tests/selected features"

#mic_feature_selection(path_to_csv, path_to_output)
trees_feature_selection(path_to_csv, path_to_output)