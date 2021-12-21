#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 08:08:10 2021

@author: masud
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 07:15:10 2021

@author: masud
"""

import nltk
nltk.download('words')

from nltk.corpus import words
import os

from os import listdir
from os.path import isfile, join
import pandas as pd
import re
from wordsegment import load, segment
load()


forums=[
            'fb_links_twitter',
]
forums_shorts=[
            'fb',
]

def read_usernames ():
    

    path='data'
    df_arr=[]
    for file in os.listdir(path):
         filename = os.fsdecode(file)
         forum_name=filename.replace('_usernames.csv', '')
         if forum_name in forums:
             df=pd.read_csv(join(path, filename))
             print(filename, df.shape)
             print(df.columns)
             df['forum_name']=forum_name
             df=df.rename(columns={'facebook': 'username'})
             df_arr.append(df[['username', 'forum_name']])
    
    forums_usernames=pd.concat(df_arr, ignore_index=True)
    forums_usernames['forum_name'].replace(forums,forums_shorts,inplace=True)
    print(forums_usernames.shape) 
#     boolean_series = forums_usernames.forum_name.isin(forums_shorts[:-2])
#     forums_usernames_except_stackexchange = forums_usernames[boolean_series]
#     print(forums_usernames_except_stackexchange.shape)
    
    return forums_usernames


def extract_numerics(username):
    
    # extract numbers/digits in leading/trailing position of the string
    numbers_in_prefix=re.findall(r'^[0-9]{1,}', username)
    username = re.sub(r'^[0-9]{2,}', '', username)
        
    numbers_in_suffix=re.findall(r'[0-9]{1,}$', username)
    username = re.sub(r'[0-9]{2,}$', '', username)
    
    numbers_in_middle=re.findall(r'[0-9]{2,}', username)
    
    all_numbers=numbers_in_prefix+numbers_in_suffix+numbers_in_middle
    all_numbers=list(set(all_numbers))
    all_numbers.sort()
    
    # print(username, all_numbers)
    
    return all_numbers, username



def extract_chunks_based_on_stop_chars(username):
    
    has_punctuation = False
    
    # split based on stopping characters
    chunks_based_on_stopping_chars=re.split('[_ -.]', username)
#     print('Chunks based on stopping chars', chunks_based_on_stopping_chars)
    
    if len(chunks_based_on_stopping_chars) > 1:
        has_punctuation = True
    
    chunks_based_on_stopping_chars.sort()
    
    return chunks_based_on_stopping_chars, has_punctuation


def extract_meaningful_chunks(chunks):
    
    # extract meaningful words
    meaningful_chunks=[]
    for chunk in chunks:
        segment_list=segment(chunk)
        for seg in segment_list:
            # if seg in words.words():
            meaningful_chunks.append(seg)
#     print('Meaningful chunks', meaningful_chunks)
    
    meaningful_chunks.sort()
    
    return meaningful_chunks


transformer_map={
    '0': ['o'],
    '1': ['i', 'l', 't'],
    '2': ['z'],
    '3': ['e', 's'],
    '4': ['a', 'r'],
    '5': ['s'],
    '@': ['a'],
    '!': ['i'],
    
}

def transform(username):
    
    transformed_usernames=[username]
    is_transformed= False
    for char, transformer_vals in transformer_map.items():
        
        if char in username:
            is_transformed = True
            temp=[]
            for val in transformer_vals:
                
                for username in transformed_usernames:
                    temp.append( username.replace(char, val) )
            transformed_usernames=temp
            
    transformed_usernames = list(set(transformed_usernames))
#     print('Transformed usernames', transformed_usernames)
    
    chunks_based_on_stopping_chars=[]
    meaningful_chunks=[]
    for username in transformed_usernames:
        extracted, _ = extract_chunks_based_on_stop_chars(username)
        chunks_based_on_stopping_chars = chunks_based_on_stopping_chars + \
            extracted
        meaningful_chunks = meaningful_chunks + extract_meaningful_chunks(extracted)
    
    chunks_based_on_stopping_chars = list(set(chunks_based_on_stopping_chars))
    meaningful_chunks = list(set(meaningful_chunks))
    
#     print('Chunks based on stopping chars', chunks_based_on_stopping_chars)
#     print('Meaningful chunks', meaningful_chunks)    

    transformed_usernames.sort()
    chunks_based_on_stopping_chars.sort()
    meaningful_chunks.sort()
    
    return transformed_usernames, chunks_based_on_stopping_chars, \
                meaningful_chunks, is_transformed
                


def chunkify(username):
    
    username_lower=username.lower()
    
    all_numbers, username_numerics_removed = extract_numerics(username_lower)
    
    chunks_based_on_stopping_chars, has_punctuation = \
        extract_chunks_based_on_stop_chars(username_numerics_removed)
        
    meaningful_chunks = extract_meaningful_chunks(
                            chunks_based_on_stopping_chars)
    
    transformed_usernames, transformed_chunks_based_on_stopping_chars, \
            transformed_meaningful_chunks, is_transformed = transform(username_numerics_removed)
    
        
    return [all_numbers, transformed_usernames, is_transformed, \
            chunks_based_on_stopping_chars, has_punctuation, \
                meaningful_chunks, transformed_meaningful_chunks]
#     print('Numbers found', numbers_in_prefix_suffix)
#     print('Chunks found',  all_chunks)
#     print('Meaningful chunks found',  all_meaningful_chunks)




forums_usernames = read_usernames()

forums_usernames['numbers']=''

forums_usernames['transformed_usernames']=''
forums_usernames['is_transformed']=''
forums_usernames['puncutuation_chunks']=''
forums_usernames['has_punctuation']=''
forums_usernames['meaningful_chunks']=''
forums_usernames['transformed_meaningful_chunks']=''

forums_usernames['all_meaningful_chunks']=''


for i, row in forums_usernames.iterrows():
    
    chunkify_output = chunkify(str(row['username']).strip())
    
    all_numbers = chunkify_output[0]
    transformed_usernames = chunkify_output[1]
    is_transformed = chunkify_output[2]
    chunks_based_on_stopping_chars = chunkify_output[3]
    has_punctuation = chunkify_output[4]
    meaningful_chunks = chunkify_output[5]
    transformed_meaningful_chunks = chunkify_output[6]
    
    all_meaningful_chunks = list(set(meaningful_chunks+ \
                                     transformed_meaningful_chunks))
    
    
    row['numbers']=','.join(all_numbers)

    row['transformed_usernames']=','.join(transformed_usernames)
    row['is_transformed']=is_transformed
    row['puncutuation_chunks']=','.join(chunks_based_on_stopping_chars)
    row['has_punctuation']=has_punctuation
    row['meaningful_chunks']=','.join(meaningful_chunks)
    row['transformed_meaningful_chunks']=','.join(transformed_meaningful_chunks)
    row['all_meaningful_chunks']=','.join(all_meaningful_chunks)
    
    
    print(i)

forums_usernames.to_csv('re_chunkification_social_output.csv')
    
    