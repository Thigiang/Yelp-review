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

class Text_plot():
    def __init__(self, data, text):
        self.__data=data
        self.__text=text
    def dist_bar(self,x, title, ylabel):
        fig= plt.figure
        ax=sns.countplot(x=x)
        plt.title(title)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.show()
    def wordcloud(self, title):
        WC=WordCloud(max_words=10000).generate(str(self.__text))
        fig=plt.figure
        plt.imshow(WC)
        plt.title(title)
        plt.axis('off')
        plt.show()
        
class Text_preprocessing():
    def __init__(self, data):
        self.__data=data
    def token_word(self):
        token_review=[word_tokenize(text) for text in self.__data]
        return token_review

    def chunking(self, chunk_rule):
        chunk_parser=RegexpParser(chunk_rule)
        all_chunks=[]
        pos_tags=[nltk.pos_tag(tokens) for tokens in self.token_word(self.__data)]
        for pos_tag in pos_tags:
            tree=chunk_parser.parse(pos_tag)
            chunks=[]
            for subtree in tree.subtrees():
                if subtree.label()=="Chunk":
                    chunk=' '.join([token for token, pos in subtree.leaves()])
                    chunks.append(chunk)
            all_chunks.append(chunks)
    def remove_stop_words(self, stop_words):        
        filter_token= []
        for rev in self.token_word():
            filter=[word for word in rev if word.lower() not in stop_words]
            filter_token.append(filter)
        return filter_token
    
    def lemmatize_word(self):
        lemmatizer=WordNetLemmatizer()
        filter_lemma=[]
        for rev in self.remove_stop_words(stop_words):
            filter=[lemmatizer.lemmatize(word) for word in rev]
            filter_lemma.append(filter)
        return filter_lemma


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


def subset_review(data, type, stop_words):
    numsub=len(np.unique(data["rating"]))
    for i in range(1,numsub+1):
        preprocessing=Text_preprocessing(data["reviews"][data['rating']==i])
        if type=="token":
            subreview=preprocessing.token_word()
        elif type=="remove":
            subreview=preprocessing.remove_stop_words(stop_words)
        Text_plot(data, subreview).wordcloud("WordCloud for reviews with rating {star} star".format(star=i))
        


"""
Plot the distribution of the original data for a better understand of the problem.
The figure distribution of the data shows that the dataset is unbalanced
5 star reviews takes up to 50% of the data. Small rating (negative rating) has very few observation.
i.e. there are <1000 review with 2 stars, about 1000 reviews with 1 star. The negative review is only 12% of the dataset
"""
Text_plot(data, data["reviews"]).dist_bar(x=data["rating"],title="Distribution of the data",ylabel="Number of review" )
"""
Create wordcloud for the original data to investigate the text
"""
review=Text_preprocessing(data["reviews"]).token_word()
Text_plot(data, review).wordcloud("WordCloud for all ratings")
subset_review(data,"token",stop_words)

"""
REMOVING STOP WORDS as they appear a lot in the wordcloud
"""
review=Text_preprocessing(data["reviews"]).remove_stop_words(stop_words)
Text_plot(data, review).wordcloud("WorldCloud for all ratings after removing stopwords")
subset_review(data,"remove",stop_words)

print(review)
