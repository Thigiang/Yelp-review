#import data
import csv
import pandas as pd 
# path="/Users/gabati/Documents/GitHub/Yelp-review/yelproject/data/"
columns_name={0:"reviews",1:"rating"}
def import_csvdata(file_name, header_status):
    data=pd.read_csv(file_name, header=header_status)
    return data
file_name="yelp_data.csv"
data=import_csvdata(file_name, None)
data=pd.DataFrame(data).rename(columns=columns_name)
review=data["reviews"]
reviews=[[review[i]] for i in range(len(review))] #store review in a 2 D array

import nltk #The natural language toolkit
#nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


"""
Do chunking to group a certain group of words first
"""
from nltk.chunk import RegexpParser
from nltk.tree import tree

token_review=[word_tokenize(text[0]) for text in reviews]

pos_tags=[nltk.pos_tag(tokens) for tokens in token_review]
# print(pos_tags)

chunk_rule=r"""Chunk: {<JJ>* <NN.*>+}"""
chunk_parser=RegexpParser(chunk_rule)
all_chunks=[]
for pos_tag in pos_tags:
    tree=chunk_parser.parse(pos_tag)
    chunks=[]
    for subtree in tree.subtrees():
        if subtree.label()=="Chunk":
            chunk=' '.join([token for token, pos in subtree.leaves()])
            chunks.append(chunk)
    all_chunks.append(chunks)
print("token review: ", token_review[:10])
print("all chunks: ", all_chunks[:10])

# filter_token= []
# stop_words=set(stopwords.words('English'))
# special_char=[".", ",", "...", "[", "]", "@", "_", "!", "#", "$", "%", "^", "&", "*", "(", ")", "<", ">", "?",  "{", "}", "~", ":"]
# revert_words=["won't",'does','aren',"it's","don't",'isn','are',"aren't",'doesn','didn',"isn't",'ain',
# "wasn't", 'hasn','won','mightn', "shouldn't",'mustn',"mustn't","haven't","weren't",
# "didn't","doesn't",'couldn','weren', 'hadn',"hadn't",'not',"needn't","no",'shouldn',"wouldn't","very"]
# for char in special_char:
#     stop_words.add(char)
# for word in revert_words:
#     stop_words.remove(word)

# for rev in token_review:
#     filter=[word for word in rev if word.lower() not in stop_words]
#     filter_token.append(filter)

# lemmatizer=WordNetLemmatizer()
# filter_lemma=[]
# for rev in filter_token:
#     filter=[lemmatizer.lemmatize(word) for word in rev]
#     filter_lemma.append(filter)
# print(lemmatizer.lemmatize("dogs"))
# print("token: ", filter_token[299])
# print("lemma: ", filter_lemma[299])


