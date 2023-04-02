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
from yelp_eda import Yelp_eda, Yelp_featuresextr
from yelp_classifiers import Yelp_classification
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
def import_csvdata(file_name, header_status):
    data=pd.read_csv(file_name, header=header_status)
    return data
path="/Users/gabati/Documents/GitHub/Yelp-review/yelproject/data/"
columns_name={0:"reviews",1:"rating"}
file_name=["yelp_traindata.csv", "Yelp_testdata.csv"]
for i in range(2):
    if file_name[i]=="yelp_traindata.csv":
        review_data=import_csvdata(file_name[i], None) #importing data
    else:
        test_data=import_csvdata(file_name[i], None)
review_data=pd.DataFrame(review_data).rename(columns=columns_name) #rename columns for easy working
test_data=pd.DataFrame(test_data).rename(columns=columns_name)
data=review_data.drop_duplicates(subset=["reviews"],keep='first', ignore_index=True) #remove duplicates
data_tst=test_data.drop_duplicates(subset=["reviews"],keep='first', ignore_index=True)

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
VISULIZATION
Plot the distribution of the original data for a better understand of the problem.
The figure distribution of the data shows that the dataset is unbalanced
5 star reviews takes up to 50% of the data. Small rating (negative rating) has very few observation.
i.e. there are <1000 review with 2 stars, about 1000 reviews with 1 star. The negative review is only 12% of the dataset
"""

# Yelp_eda(data).plot_bar(x=data["rating"],title="Distribution of the data",ylabel="Number of review" )
# """
# Create wordcloud for the original data to investigate the text
# """
# orig_reviews=Yelp_eda(data).prepro_token(data["reviews"])
# Yelp_eda(data).plot_wordcloud("WordCloud for all ratings", orig_reviews)
# Yelp_eda(data).plot_subwordcloud("token",stop_words)

# # """
# # REMOVING STOP WORDS as they appear a lot in the wordcloud
# # """
removed_reviews=Yelp_eda(data).prepro_remove_stopwords(stop_words, data.reviews)
removed_reviews_tst=Yelp_eda(data_tst).prepro_remove_stopwords(stop_words,data_tst.reviews)
# Yelp_eda(data).plot_wordcloud("WorldCloud for all ratings after removing stopwords", removed_reviews)
# Yelp_eda(data).plot_subwordcloud("remove",stop_words)

"""
FEATURE EXTRACTION
"""
def make_sentence(data):
    review_sentences=[]
    for rev in data:
        text=""
        for word in rev:
            text+= (" "+word)
        review_sentences.append(text)
    return review_sentences

data["cleaned_review"]=pd.DataFrame(make_sentence(removed_reviews))
data_tst["cleaned_review"]=pd.DataFrame(make_sentence(removed_reviews_tst))
Xtr=data.cleaned_review
ytr=data.rating
Xtst=data_tst.cleaned_review
ytst=data_tst.rating

"""
Start classify the data. Keep the data as its original with 5 ratings.
"""
feature_type=["BoW", "Tfidf","Combined"]
results={}
for ft in feature_type:
    pred, accuracy_rate, F1_score=Yelp_classification(Xtr, ytr, Xtst, ytst).NB(ft, alp=0.01)
    results[ft]=[pred, accuracy_rate, F1_score]

# xtick=[i for i in range(1,6)]
# confu_matrix=metrics.confusion_matrix(ytst, results["BoW"][0])
# sns.heatmap(confu_matrix, annot=True, xticklabels=xtick, yticklabels=xtick)
# plt.xlabel("Predicted label")
# plt.ylabel("True label")
# plt.show()

wrong_pred=data_tst[["reviews","rating"]][ytst!=results["BoW"][0]]
wrong_pred["predicted rating"]=results["BoW"][0][ytst!=results["BoW"][0]]
wrong_pred.sort_values("rating", inplace=True)
wrong_pred_one=wrong_pred[wrong_pred.rating==1].sort_values("predicted rating")
review_one=wrong_pred_one["reviews"][wrong_pred_one["predicted rating"]==5]
reviews_one=[[i] for i in review_one]
print(reviews_one)


