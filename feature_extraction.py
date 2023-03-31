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
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


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



        


"""
Plot the distribution of the original data for a better understand of the problem.
The figure distribution of the data shows that the dataset is unbalanced
5 star reviews takes up to 50% of the data. Small rating (negative rating) has very few observation.
i.e. there are <1000 review with 2 stars, about 1000 reviews with 1 star. The negative review is only 12% of the dataset
"""

Yelp_eda(data).plot_bar(x=data["rating"],title="Distribution of the data",ylabel="Number of review" )
"""
Create wordcloud for the original data to investigate the text
"""
orig_reviews=Yelp_eda(data).prepro_token(data["reviews"])
Yelp_eda(data).plot_wordcloud("WordCloud for all ratings", orig_reviews)
Yelp_eda(data).plot_subwordcloud("token",stop_words)

# """
# REMOVING STOP WORDS as they appear a lot in the wordcloud
# """
removed_reviews=Yelp_eda(data).prepro_remove_stopwords(stop_words, data["reviews"])
Yelp_eda(data).plot_wordcloud("WorldCloud for all ratings after removing stopwords", removed_reviews)
Yelp_eda(data).plot_subwordcloud("remove",stop_words)


# review_sentences=[]
# for rev in removed_reviews:
#     text=""
#     for word in rev:
#         text+= (" "+word)
#     review_sentences.append(text)
# data["cleaned_review"]=pd.DataFrame(review_sentences)
