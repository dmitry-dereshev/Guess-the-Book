# Part of Guess the Book project by Dmitry Dereshev. MIT Licence 2019.
# https://github.com/dmitry-dereshev/guess-the-book-public

# Scales the dataset from 4_merge.py, and splits it into training sets based 
# on the number of books per author. Fills in empty values with 0s, and removes
# entries with empty frequency rows.

import pandas as pd
from sklearn import preprocessing

def split_that_data(data_in, data_out, books_per_author):
    # Drop empty rows, fill the rest with 0s, drop 'various' author.
    data = pd.read_csv(data_in, index_col="ID")
    data = data.dropna(subset=data.iloc[:, 4:].columns.values, how='all')
    data = data[data.Author != 'Various']
    data = data.fillna(value=0)
    
    # Scale the data, bring it back into a dataframe
    training_data = data.iloc[:, 4:]
    min_max_scaler = preprocessing.MinMaxScaler()
    training_data_scaled = min_max_scaler.fit_transform(training_data)
    back_to_dataframe = pd.DataFrame(data=training_data_scaled,\
         index=training_data.index, columns=training_data.columns)
    back_to_dataframe = data.iloc[:, :4].join(back_to_dataframe)
    
    # Generate datasets with the required number of books per author.
    count_books_per_author = back_to_dataframe.groupby(['Author']).count()
    count_books_per_author = count_books_per_author.Birthdate
    
    for i in books_per_author:
        chosen_authors = count_books_per_author >= i
        chosen_authors = chosen_authors[chosen_authors == True]
        needed_authors = back_to_dataframe[back_to_dataframe['Author'].isin(chosen_authors.index)]
        
        limit_to_i_books_per_author = needed_authors.groupby(['Author']).head(i)
        file_name = data_out+'/'+str(i)+' books per author.csv'

        limit_to_i_books_per_author.to_csv(file_name, index='ID')



# Where the table from 04_merge.py is
path_to_data = 'path/to/.csv'
# Folder where you want the resulting scaled sets to drop
output_path = 'folder/to/store/scaled/table'
# A list of number of books per author to split dataset into
book_per_author = [26, 52, 78, 104]
split_that_data(path_to_data, output_path, book_per_author)
