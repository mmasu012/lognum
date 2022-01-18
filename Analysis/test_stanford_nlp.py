#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 20:53:38 2021

@author: masud
"""

import stanza
# stanza.download('en')

nlp = stanza.Pipeline(lang='en', processors='tokenize,ner,pos,mwt')
doc = nlp("India")
print(*[f'entity: {ent.text}\ttype: {ent.type}' for sent in doc.sentences \
                                                    for ent in sent.ents], sep='\n')


# nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos')
# doc = nlp("elite hacker 4")
# print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')



# nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment')
# doc = nlp('i love')
# for i, sentence in enumerate(doc.sentences):
#     print(i, sentence.sentiment)

# import pandas as pd

# df = pd.read_csv('re_chunkification_output.csv')
# nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment')

# data=[]
# sentiements=[]
# usernames=[]

# for i, row in df.iterrows():
    
#     doc = nlp(str(row['all_meaningful_chunks']).replace(',', '').title())
#     sentiment=doc.sentences[0].sentiment
#     username = row['username']
#     # print(username, sentiment)
    
#     data.append([username, sentiment])
    
#     if i%1000 == 0:
#         print(i)
    

    
# df_sentiment = pd.DataFrame(data, columns =['username', 'sentiment'])
# df_sentiment['sentiment'] = df_sentiment['sentiment'].map({
#     0:'negative', 1:'neutral', 2:'positive'})
# df_sentiment.to_csv('sentiments.csv')
#     username = row['username']
#     forum = row['forum_name']
    
#     # print(chunks)
    
#     for chunk in chunks:
#         if chunk in keywords:
#             # print(username, forum, chunk)
#             usernames.append(username)
#             iter+=1
#             if chunk not in hack_terms:
#                 hack_terms[chunk]=1
#             else:
#                 hack_terms[chunk]+=1
                
            
#             if forum not in forum_names:
#                 forum_names[forum]=1
#             else:
#                 forum_names[forum]+=1