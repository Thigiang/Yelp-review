# from yelp_eda import Text_plot
from yelp_eda import Text_preprocessing
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import pandas as pd 
from wordcloud import WordCloud
import nltk #The natural language toolkit
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.chunk import RegexpParser
from nltk.tree import tree

def import_csvdata(file_name, header_status):
    data=pd.read_csv(file_name, header=header_status)
    return data

path="/Users/gabati/Documents/GitHub/Yelp-review/yelproject/data/"
columns_name={0:"reviews",1:"rating"}
file_name="yelp_data.csv"
review_data=import_csvdata(file_name, None) #importing data
review_data=pd.DataFrame(review_data).rename(columns=columns_name) #rename columns for easy working
data=review_data.drop_duplicates(subset=["reviews"],keep='first') #remove duplicates


stop_words=set(stopwords.words('English'))
special_char=["'ve",".", ",", "...", "[", "]", "@", "_", "!", "#", "$", "%", "^", "&", "*", "(", ")", "<", ">", "?",  "{", "}", "~", ":"]
revert_words=["won't",'does','aren',"it's","don't",'isn','are',"aren't",'doesn','didn',"isn't",'ain',
"wasn't", 'hasn','won','mightn', "shouldn't",'mustn',"mustn't","haven't","weren't",
"didn't","doesn't",'couldn','weren', 'hadn',"hadn't",'not',"needn't","no",'shouldn',"wouldn't","very"]
for char in special_char:
    stop_words.add(char)
for word in revert_words:
    stop_words.remove(word)


review=Text_preprocessing(data["reviews"]).token_word()

"""
REMOVING STOP WORDS as they appear a lot in the wordcloud
"""
review=Text_preprocessing(data["reviews"]).remove_stop_words(stop_words)

print(review)
