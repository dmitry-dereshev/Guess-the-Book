#Part of Guess the Book project by Dmitry Dereshev. MIT Licence 2019.
# https://github.com/dmitry-dereshev/guess-the-book-public

#The script takes in a top-level folder with .txt files, and transforms
#them into a Pandas DataFrame of symbol frequencies. The DataFrame is
#then saves as a .csv.

import pandas as pd
import os


def frequentize(path_to_txt, path_for_csv):
    # Creates a list of all paths to .txt files
    txt_files = [os.path.join(root, name)
                for root, dirs, files in os.walk(path_to_txt) 
                for name in files]

    temp_store = [] #stores .txt frequency dictionaries
    len_data = len(txt_files)
    counter = 0

    for paths in txt_files:
        counter += 1
        alist = [line.rstrip() for line in open(paths, errors='ignore')]
        stringify = ''.join(alist)
        res = {}
        res["ID"] = os.path.basename(paths)
        # using dict.get() to get count of each element in string  
        for keys in stringify: 
            res[keys] = res.get(keys, 0) + 1
        temp_store.append(res)
        print("processing %s of %s through temp_store" % (counter, len_data))

    print("assembling temp_res into a dataframe...")
    # Turns a list of dictioanries into a Pandas DataFrame.
    symbols_assemble = pd.DataFrame(temp_store)
    id_column = symbols_assemble["ID"]
    symbols_assemble.drop(labels=['ID'], axis=1,inplace = True)
    symbols_assemble.insert(0, 'ID', id_column)

    print("saving everything into a csv...")
    symbols_assemble.to_csv(path_for_csv)



# Top-level folder with .txt files
# The script checks for all subfolders as well.
path_to_txt = 'top/folder/with/.txt/files' 
path_for_csv = 'where/you/want/the/resulting/table.csv'
frequentize(path_to_txt, path_for_csv)