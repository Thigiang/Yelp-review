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

class Yelp_eda:
    def __init__(self,data):
        self.__data=data
    def plot_bar(self,x, title, ylabel):
        fig= plt.figure
        ax=sns.countplot(x=x)
        plt.title(title)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.show()
    def plot_wordcloud(self, title, reviews):
        WC=WordCloud(max_words=10000).generate(str(reviews))
        fig=plt.figure
        plt.imshow(WC)
        plt.title(title)
        plt.axis('off')
        plt.show()
    def plot_subwordcloud(self, sentence_type, stop_words):
        numsub=len(np.unique(self.__data["rating"]))
        for i in range(1,numsub+1):
            review=self.__data["reviews"][data['rating']==i]
            if sentence_type=="token":
                subreview=self.prepro_token(reviews=review)
            elif sentence_type=="remove":
                subreview=self.prepro_remove_stopwords(stop_words, reviews=review)
            self.plot_wordcloud("WordCloud for reviews with rating {star} star".format(star=i), subreview)

    def prepro_token(self, reviews):
        token_review=[word_tokenize(words) for words in reviews]
        return token_review

    def prepro_chunking(self, chunk_rule):
        chunk_parser=RegexpParser(chunk_rule)
        all_chunks=[]
        pos_tags=[nltk.pos_tag(tokens) for tokens in self.prepro_token(self.__data["reviews"])]
        for pos_tag in pos_tags:
            tree=chunk_parser.parse(pos_tag)
            chunks=[]
            for subtree in tree.subtrees():
                if subtree.label()=="Chunk":
                    chunk=' '.join([token for token, pos in subtree.leaves()])
                    chunks.append(chunk)
            all_chunks.append(chunks)
    def prepro_remove_stopwords(self, stop_words, reviews):       
        filter_token= []
        for rev in self.prepro_token(reviews):
            filter=[word for word in rev if word.lower() not in stop_words]
            filter_token.append(filter)
        return filter_token
    
    def prepro_lemmatize(self):
        lemmatizer=WordNetLemmatizer()
        filter_lemma=[]
        for rev in self.prepro_remove_stopwords(stop_words):
            filter=[lemmatizer.lemmatize(word) for word in rev]
            filter_lemma.append(filter)
        return filter_lemma

"""
Feature Extraction using BoW and TF-IDF
"""

class Yelp_featuresextr:
    def __init__(self, features):
        self.__features=features
    def BoW(self):
        BoW_vectorizer=CountVectorizer()
        BoW_features=BoW_vectorizer.fit_transform(self.__features)
        return BoW_features
    def Tfidf(self):
        tfidf_vectorizer=TfidfVectorizer()
        tfidf_features=tfidf_vectorizer.fit_transform(self.__features)
        return tfidf_features
    def combined(self):
        BoW_features=self.BoW()
        tfidf_features=self.Tfidf()
        combined_features=BoW_features.multiply(tfidf_features)
        return combined_features







