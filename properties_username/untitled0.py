#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 10:56:43 2022

@author: masud
"""

import re
import os
from wordsegment import load, segment
load()

import wordsegment as ws
import enchant
english_dict = enchant.Dict("en_US")


import nltk
# nltk.download('wordnet')

from nltk.corpus import wordnet

from nltk.corpus import sentiwordnet as swn
# nltk.download('sentiwordnet')

from suffix_trees import STree
import jaro

def extract_numerics(username):
    
    # extract numbers/digits from the string
    nums_in_username=re.findall(r'[0-9]{2,}', username)
    # print(nums_in_username)
    
    return nums_in_username

def discard_numerics(username, choice=None):
    
    if choice == 'all':
        username = re.sub(r'[0-9]{1,}', '', username)
    else:
        # discard leading/trailing numerics
        username = re.sub(r'^[0-9]{1,}', '', username)
        username = re.sub(r'[0-9]{1,}$', '', username)
    
    return username


# Motivation
# Attempting to find the chunks provided by users
# Remove numbers from start-end
# if stopping chars find any in-between numbers, they are of valuable meanings  
def extract_chunks_based_on_stop_chars(username):
    
    username = discard_numerics(username)
    
    # split based on stopping characters
    chunks_based_on_stopping_chars=re.split('[_ -.@]', username)
    
    if username in chunks_based_on_stopping_chars:
        chunks_based_on_stopping_chars.remove(username)
    while '' in chunks_based_on_stopping_chars:
        chunks_based_on_stopping_chars.remove('')
    
    # print('Chunks based on stopping chars', chunks_based_on_stopping_chars)
    
    return chunks_based_on_stopping_chars


# Motivation
# Attempting to find the chunks provided by users
def extract_chunks_based_on_capital_letters(username):
    
    username = discard_numerics(username)
    chunks_based_on_capital_chars = re.findall('[A-Z][^A-Z]*', username)
    
    if username in chunks_based_on_capital_chars:
        chunks_based_on_capital_chars.remove(username)
    
    chunks_based_on_capital_chars = list(map(lambda u : u.lower(), 
                                         chunks_based_on_capital_chars))
    
    # print('Chunks based on capital chars', chunks_based_on_capital_chars)
    
    return chunks_based_on_capital_chars


def cal_sentiment_score(synset_name):
    
    swn_synset = swn.senti_synset(synset_name)
    pos_score = swn_synset.pos_score()
    neg_score = swn_synset.neg_score()
    sentiment_score = pos_score - neg_score
    
    # print(synset_name, pos_score, neg_score)
    
    return sentiment_score


def extract_meaningful_chunks(username):
    
    # extract meaningful words
    username = discard_numerics(username, 'all')
    chunks_based_on_word_segmentation = segment(username)
    # print(chunks_based_on_word_segmentation)
    
    meaningful_chunks = []
    sentiment_score = 0
    for chunk in chunks_based_on_word_segmentation:
        
        if len(chunk) > 1:
            
            # check in two dataset
            if english_dict.check(chunk):
                meaningful_chunks.append(chunk)
        
            synsets = wordnet.synsets(chunk)
            if synsets:
                synset = synsets[0]
                meaningful_chunks.append(chunk)
                sentiment_score += cal_sentiment_score(synset.name())
                # print(chunk, synset.lexname(), sentiment_score)
            
    meaningful_chunks = set(meaningful_chunks)
    # print('Meaningful chunks', list(meaningful_chunks))
    
    meaningless_chunks = \
        set(chunks_based_on_word_segmentation) - set(meaningful_chunks)
        
    # print('Meaningless chunks', list(meaningless_chunks))
    
    return list(meaningful_chunks), list(meaningless_chunks), sentiment_score


slangification_map={
    '0': ['o'],
    '1': ['i', 'l', 't'],
    '2': ['z'],
    '3': ['e', 's'],
    '4': ['a', 'r'],
    '5': ['s'],
    '@': ['a'],
    '!': ['i'],
    # '2k9'
}


def slangify(username):
    
    slang_chars=re.findall(r'[0123445@!]{1,1}', username)
    # print(slang_chars)
    
    
    if len(slang_chars) > 0:
        
        transformed_usernames=[username]
        for char in slang_chars:
            
            replace_vals = slangification_map[char]
            temp = []
            
            for r_v in replace_vals:
                
                for t_u in transformed_usernames:
                    temp.append( t_u.replace(char, r_v) )
            
            transformed_usernames = temp
        
        
        transformed_usernames = list(set(transformed_usernames))
        # print('Transformation is finished', transformed_usernames)
        
        return transformed_usernames
    
    else:
        return []
        


def chunkify(username):
    
    chunkification_out = {}
    chunkification_out['username'] = username
    # print()
    # print()
    # print("Starting Chunkification for ", username)
    
    # make the usernames lowercased
    u_p = preprocess_username(username)
    chunkification_out['u_p'] = u_p
    
    # extract the numbers from the username
    nums_in_username = extract_numerics(u_p)
    chunkification_out['nums_in_username'] = nums_in_username
    
    # extract the chunks based on the stopping chars
    chunks_based_on_stopping_chars = extract_chunks_based_on_stop_chars(u_p)
    chunkification_out['chunks_based_on_stopping_chars'] = \
        chunks_based_on_stopping_chars
    
    # extract the chunks based on the uppercase letter
    chunks_based_on_capital_letters = \
        extract_chunks_based_on_capital_letters(str(username).strip())
    chunkification_out['chunks_based_on_capital_letters'] = \
        chunks_based_on_capital_letters
    
    # extract the chunks based on the word segmentation of username
    meaningful_chunks_ori, meaningless_chunks_ori, sentiment_score_ori = \
        extract_meaningful_chunks(username)
    chunkification_out['meaningful_chunks_ori'] = meaningful_chunks_ori
    chunkification_out['meaningless_chunks_ori'] = meaningless_chunks_ori
    chunkification_out['sentiment_score_ori'] = sentiment_score_ori
    
    
    # slangify the username
    slangified_usernames = slangify(username)
    chunkification_out['slangified_usernames'] = slangified_usernames
    
    return chunkification_out



def check_direct_matching(u_1, u_2):
    
    # make the usernames lowercased
    u_1_p = preprocess_username(u_1)
    u_2_p = preprocess_username(u_2)
    
    return u_1_p == u_2_p


def preprocess_username(username):
    
    return str(username).lower().strip()



import pandas as pd

def show_stats(filename):
    
    if filename != 'fb_links_twitter':
        forum_name = filename
        print(forum_name)
        data = pd.read_csv('data/' + forum_name +'_usernames.csv', 
                           names=['index', 'name'], index_col=0)
        
        size_before_dropping_na = data.shape[0]
        data.dropna(inplace = True)
        size_after_dropping_na = data.shape[0]
        # print("removing ", str(size_before_dropping_na - size_after_dropping_na))
        print('total user count', data.shape[0])
    else:
        forum_name = filename
        print(forum_name)
        data = pd.read_csv('data/' + forum_name +'_usernames.csv', 
                           index_col=0)
        data = data[['google_plus']]
        data.rename(columns={'google_plus': 'name'}, inplace=True)
        # print(data.columns)
        size_before_dropping_na = data.shape[0]
        data.dropna(inplace = True)
        size_after_dropping_na = data.shape[0]
        # print("removing ", str(size_before_dropping_na - size_after_dropping_na))
        print('total user count', data.shape[0])
    
    data['username_length'] = 0
    data_map = data.to_dict('records')
    
    # # with open('chunks.csv', 'w') as fp:
    
    for iteration, record in enumerate(data_map):
        
        record['username_length'] = len(record['name'])
        
        
    #     u_g = record[GOOGLE]
    #     u_f = record[FACEBOOK]
    #     u_t = record[TWITTER]
        
    #     if '.' in u_f or '@' in u_f or '_' in u_f:
    #         # print(u_f, u_t)
            
    #         find_matching_score(u_f, u_t)
    #     elif '.' in u_t or '@' in u_t or '_' in u_t:
    #         # print(u_f, u_t)
            
    #         find_matching_score(u_f, u_t)
            
        # if (iteration == 10):
        # #         print("count", iteration)
        #         break
    
    updated_data = pd.DataFrame(data_map)
    # print(updated_data.head())
    
    
    print('Mean', updated_data['username_length'].mean())
    print('25th percentile', updated_data['username_length'].quantile(0.25))
    print('50th percentile', updated_data['username_length'].quantile(0.50))
    print('75th percentile', updated_data['username_length'].quantile(0.75))
    print('90th percentile', updated_data['username_length'].quantile(0.90))
    print('95th percentile', updated_data['username_length'].quantile(0.95))
    print('Min', updated_data['username_length'].min())
    print('Max', updated_data['username_length'].max())
    print('standard deviation', updated_data['username_length'].std())
    
    print(updated_data.iloc[updated_data['username_length'].idxmax()]['name'])
    print(updated_data.iloc[updated_data['username_length'].idxmin()]['name'])
    # updated_data.hist(column=['username_length'])
    print()
    

def main():
    
    
    forum_list = [
        'ethical_hacker',
        'hack_forums',
        'hack_this_site',
        'mpgh',
        'offensive_community',
        'security_stack_exchange',
        # 'fb_links_twitter',
        
    ]
    
    # char_set = set()
    # for i in range(0, 26):
    #     char_set.add(chr(ord('A') + i))
    #     char_set.add(chr(ord('a') + i))
    
    # for i in range(0, 10):
    #     char_set.add(chr(ord('0') + i))
    
    # print(char_set)
    
    for forum in forum_list:
        
        show_stats(forum)
    
    
    

from os.path import exists
if exists('chunks.csv'):
    os.remove("chunks.csv")
    
main()








