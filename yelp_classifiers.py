import seaborn as sns
import pandas as pd
import string
import matplotlib.pyplot as plt
from yelp_eda import Yelp_featuresextr
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn import metrics
class Yelp_classification:
    def __init__(self, Xtr, ytr, Xtst, ytst):
        self.__Xtr, self.__Xtst=Xtr, Xtst
        self.__ytr, self.__ytst=ytr, ytst
    def NB(self, feat_type, alp):
        if feat_type=="Tfidf":
            Xtrn, Xtest=Yelp_featuresextr(self.__Xtr, self.__Xtst).Tfidf()
        elif feat_type=="BoW":
            Xtrn, Xtest=Yelp_featuresextr(self.__Xtr, self.__Xtst).BoW()
        else:
            Xtrn, Xtest=Yelp_featuresextr(self.__Xtr, self.__Xtst).combined()
        clf=MultinomialNB(alpha=alp).fit(Xtrn, self.__ytr)
        pred=clf.predict(Xtest)
        accuracy=metrics.accuracy_score(pred, self.__ytst)
        F1_score=metrics.f1_score(self.__ytst, pred, average='macro')
        return pred, accuracy, F1_score
