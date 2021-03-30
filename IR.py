#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from collections import OrderedDict


# In[7]:


# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')


# In[12]:


def read_file(filename):
    with open(filename, 'r', encoding ="ascii", errors ="surrogateescape") as f:
        stuff = f.read()
        return stuff
  
def preprocessing(final_string):
    # Tokenize.
    only_words = word_tokenize(final_string)
  
    # Lemmatization
    wordnet_lemmatizer = WordNetLemmatizer()
    afterLemitKeywords=[w for w in only_words if w in wordnet_lemmatizer.lemmatize(w)]

    # List of English stop words 
    english_stop_words=set(stopwords.words("english"))
    # Removal of stop words from the text
    token_list=[w for w in afterLemitKeywords if not w in english_stop_words]
    return token_list
  


# In[16]:


def get_pos_indexes():
    # In this example, we create the positional index for only 1 folder.
    folder_names = ["Assignment"]

    # Initialize the file no.
    fileno = 0

    # Initialize the dictionary.
    pos_index = {}

    # Initialize the file mapping (fileno -> file name).
    file_map = {}


    for folder_name in folder_names:

        # Open files.
        file_names = sorted(os.listdir(folder_name))

        # For every file.
        for file_name in file_names:
            
            if file_name.startswith("Doc"):

                # Read file contents.
                stuff = read_file(folder_name + "/" + file_name)

                final_token_list = preprocessing(stuff)

                # open output file for writing
                with open(folder_name + "/" + "preprocessed_"+file_name, "w") as filehandle:
                    if not os.path.exists(filehandle.name):
                        json.dump(final_token_list, filehandle)

                # For position and term in the tokens.
                for pos, term in enumerate(final_token_list):

                            # If term already exists in the positional index dictionary.
                            if term in pos_index:

                                # Increment total freq by 1.
                                pos_index[term][0] = pos_index[term][0] + 1

                                # Check if the term has existed in that DocID before.
                                if fileno in pos_index[term][1]:
                                    pos_index[term][1][fileno].append(pos)

                                else:
                                    pos_index[term][1][fileno] = [pos]

                            # If term does not exist in the positional index dictionary 
                            # (first encounter).
                            else:

                                # Initialize the list.
                                pos_index[term] = []
                                pos_index[term].append(1)
                                pos_index[term].append({})      
                                # Add doc ID to postings list.
                                pos_index[term][1][fileno] = [pos]

                with open(folder_name + "/" + "inverted_index_"+file_name, "w") as file:
                    if not os.path.exists(file.name):
                        file.write(json.dumps(pos_index))
        #         print(pos_index)
                # Map the file no. to the file name.
                file_map[fileno] = folder_name + "/" + file_name

                fileno += 1
            
    return pos_index

def get_query_result(query):
    
    try: 
        pos_index = get_pos_indexes()

        # Remove all stopwords and words which is not in dictionary
        preprocessed_query = preprocessing(query)

        preprocessed_query = {word for word in preprocessed_query
                                if word in pos_index.keys()}
        # creating an empty dictionary consisting of as many items as the number of words preprocessed
        words_dict = OrderedDict((i, {}) for i in preprocessed_query)

        # assigning the filenumber and positions to the values of words_dict for each word
        for word in words_dict.keys():
            if word in words_dict.keys():

                files_li = []
                pos_li = []
                temp_index = pos_index[word]
                files_pos = temp_index[1]
                print(files_pos)
                for fileno, positions in files_pos.items():
                     words_dict[word] = files_pos


        # store each word file number in a set to find the intersection(boolean "and") between the all the words
        li_s = []
        for i, key in enumerate(words_dict.keys()):
            li_s.append(set(words_dict[key].keys()))

        intersect_result = li_s[0].intersection(*li_s)

        if len(intersect_result) > 0:
            print("Total match(es) found: ", len(intersect_result))
            for i, doc in enumerate(intersect_result):
                print("Matching document-{}: {}".format(i+1, "Assignment" + "/" + "inverted_index_"+ str(doc)))
                for key in words_dict.keys():
                    print("{} positions are: {}".format(key, words_dict[key][doc]))
        else:
            print("No match found!")
    except Exception as e:
        print("Exception occured! : ", str(e))


# In[17]:


query = input("Enter the search query you would like to retrieve information for: ")
if len(query)>0:
    get_query_result(query)
else: 
    print("Please enter a valid query!")


# In[125]:





# In[ ]:




