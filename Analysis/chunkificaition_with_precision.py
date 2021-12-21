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
            'hack_this_site',
            'ethical_hacker',
            'wilderssecurity',
            # 'offensive_community',
            'mpgh',
            'security_stack_exchange',
            'unix_stackexchange',
            'cc',
]
forums_shorts=[
            'htt',
            'eh',
            'ws',
            # 'oc',
            'mpgh',
            'ss',
            'us',
            'oc_2',
]

def read_usernames ():
    

    path='data'
    df_arr=[]
    colnames=['index', 'username']
    for file in os.listdir(path):
         filename = os.fsdecode(file)
         forum_name=filename.replace('_usernames.csv', '')
         if forum_name in forums:
             df=pd.read_csv(join(path, filename), names=colnames, header=None)
             print(filename, df.shape)
             df['forum_name']=forum_name
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
    numbers_in_prefix=re.findall(r'^[0-9]{2,}', username)
    username = re.sub(r'^[0-9]{2,}', '', username)
        
    numbers_in_suffix=re.findall(r'[0-9]{2,}$', username)
    username = re.sub(r'[0-9]{2,}$', '', username)
    
    numbers_in_prefix_suffix=numbers_in_prefix+numbers_in_suffix
#     print('Numbers found', numbers_in_prefix_suffix)
    
    return numbers_in_prefix_suffix, username

def extract_chunks_based_on_stop_chars(username):
    
    # split based on stopping characters
    chunks_based_on_stopping_chars=re.split('[_ -.]', username)
#     print('Chunks based on stopping chars', chunks_based_on_stopping_chars)
    
    return chunks_based_on_stopping_chars

def extract_meaningful_chunks(chunks):
    
    # extract meaningful words
    meaningful_chunks=[]
    for chunk in chunks:
        segment_list=segment(chunk)
        for seg in segment_list:
            # if seg in words.words():
            meaningful_chunks.append(seg)
#     print('Meaningful chunks', meaningful_chunks)
    
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
    for char, transformer_vals in transformer_map.items():
        
        if char in username:
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
        chunks_based_on_stopping_chars = chunks_based_on_stopping_chars + extract_chunks_based_on_stop_chars(username)
        meaningful_chunks = meaningful_chunks + extract_meaningful_chunks(chunks_based_on_stopping_chars)
    
    chunks_based_on_stopping_chars = list(set(chunks_based_on_stopping_chars))
    meaningful_chunks = list(set(meaningful_chunks))
    
#     print('Chunks based on stopping chars', chunks_based_on_stopping_chars)
#     print('Meaningful chunks', meaningful_chunks)    

    return transformed_usernames, chunks_based_on_stopping_chars, meaningful_chunks

def chunkify(username):
    username_lower=username.lower()
    
    numbers_in_prefix_suffix, username_numerics_removed = extract_numerics(username_lower)
    chunks_based_on_stopping_chars = extract_chunks_based_on_stop_chars(username_numerics_removed)
    meaningful_chunks = extract_meaningful_chunks(chunks_based_on_stopping_chars)
    
    transformed_usernames, transformed_chunks_based_on_stopping_chars, \
            transformed_meaningful_chunks = transform(username_numerics_removed)
    
    
    
    return [numbers_in_prefix_suffix, chunks_based_on_stopping_chars, transformed_chunks_based_on_stopping_chars, \
            meaningful_chunks, transformed_meaningful_chunks]
#     print('Numbers found', numbers_in_prefix_suffix)
#     print('Chunks found',  all_chunks)
#     print('Meaningful chunks found',  all_meaningful_chunks)




forums_usernames = read_usernames()

forums_usernames['numbers']=''
forums_usernames['all_chunks']=''
forums_usernames['all_meaningful_chunks']=''

forums_usernames['chunks']=''
forums_usernames['transformed_chunks']=''
forums_usernames['meaningful_chunks']=''
forums_usernames['transformed_meaningful_chunks']=''


for i, row in forums_usernames.iterrows():
    
    chunkify_output = chunkify(str(row['username']).strip())
    
    numbers_in_prefix_suffix = chunkify_output[0]
    chunks_based_on_stopping_chars = chunkify_output[1]
    transformed_chunks_based_on_stopping_chars = chunkify_output[2]
    meaningful_chunks = chunkify_output[3]
    transformed_meaningful_chunks = chunkify_output[4]
    
    all_chunks = list(set(chunks_based_on_stopping_chars+transformed_chunks_based_on_stopping_chars))
    all_meaningful_chunks = list(set(meaningful_chunks+transformed_meaningful_chunks))
    
    row['numbers']=','.join(numbers_in_prefix_suffix)
    row['all_chunks']=','.join(all_chunks)
    row['all_meaningful_chunks']=','.join(all_meaningful_chunks)

    row['chunks']=','.join(chunks_based_on_stopping_chars)
    row['transformed_chunks']=','.join(transformed_chunks_based_on_stopping_chars)
    row['meaningful_chunks']=','.join(meaningful_chunks)
    row['transformed_meaningful_chunks']=','.join(transformed_meaningful_chunks)
    
    print(i)

forums_usernames.to_csv('chunkification_output_3.csv')
    
    