# Part of Guess the Book project by Dmitry Dereshev. MIT Licence 2019.
# https://github.com/dmitry-dereshev/guess-the-book-public

# Takes in the datasets from 06_mic_trees_feature_selection.py, runs them
# through 4 AIs (neural nets, trees, SVMs, Gaussian Bayes), exports accuracy
# base on 10-fold cross-validation, prints the results, and exports them to a
# .csv file.

from sklearn.model_selection import train_test_split, cross_val_score,\
     cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix,\
     accuracy_score

from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn import svm
from sklearn.naive_bayes import GaussianNB

import pandas as pd
import os

def neural_net_test(X, y):
    print("Training the neural network...")
    # train the neural network
    number_of_authors = y.nunique()
    mlp = MLPClassifier(hidden_layer_sizes=(len(X.columns),\
        int((abs(len(X.columns)-number_of_authors)/2)),\
            number_of_authors), max_iter=1000000)
    

    prediction = cross_val_predict(mlp, X, y, cv=10, n_jobs=-1, verbose=1)
    scores = accuracy_score(y, prediction)
    return scores

def trees_test(X, y):
    # I Am The Lorax I Speak For The Trees
    print("Training the trees...")
    clf = tree.DecisionTreeClassifier(random_state=7275)

    prediction = cross_val_predict(clf, X, y, cv=10, n_jobs=-1, verbose=1)
    scores = accuracy_score(y, prediction)
    return(scores)

def svm_test(X, y):
    # Support Vector Machines (SVMs)
    print("Training the SVMs...")
    clf = svm.SVC(C=50,gamma='scale')

    prediction = cross_val_predict(clf, X, y, cv=10, n_jobs=-1, verbose=1)
    scores = accuracy_score(y, prediction)
    return scores

def gaussian_bayes_test(X, y):
    gnb = GaussianNB()

    prediction = cross_val_predict(gnb, X, y, cv=10, n_jobs=-1, verbose=1)
    scores = accuracy_score(y, prediction)
    return scores




def AI_tests(data_in, data_out):
    print("Importing data...")
    data = [os.path.join(root, name)
            for root, dirs, files in os.walk(data_in) 
            for name in files]
    neural_net_data = {}
    trees_data = {}
    svm_data = {}
    gaussian_bayes_data = {}
    
    for dataset in data:
        the_set = pd.read_csv(dataset, index_col='ID')
        the_dataset_name = os.path.basename(dataset)
        print("Splitting the data into question and answer sets...")
        X = the_set.iloc[:, 1:] # symbol frequencies
        y = the_set.iloc[:, 0] # authors
        neural_net_data[the_dataset_name] = neural_net_test(X, y)
        trees_data[the_dataset_name] = trees_test(X, y)
        svm_data[the_dataset_name] = svm_test(X, y)
        gaussian_bayes_data[the_dataset_name] = gaussian_bayes_test(X, y)
    report = pd.DataFrame([neural_net_data, trees_data, svm_data, gaussian_bayes_data])
    report = report.T
    report.set_axis(labels=['Neural Nets', 'Trees', 'SVM', 'Gaussian Bayes'],\
         axis='columns', inplace=True)
    print(report)
    report.to_csv(data_out)
    


# The script scans for all subfolders as well.
path_to_folder_with_datasets = 'D:/Downloads/2019 Software Code/2019 Python Code/Guess the Book Project/guess-the-book-data-software/.01 Data/Testing data/selected features'

# A concise report on the relative performance of each algorithm & dataset goes here.
where_results_go = 'D:/Downloads/2019 Software Code/2019 Python Code/Guess the Book Project/guess-the-book-data-software/.01 Data/Testing data/test_results.csv'

AI_tests(path_to_folder_with_datasets, where_results_go)