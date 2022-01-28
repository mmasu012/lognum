# -*- coding: utf-8 -*-
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



def chunkify(username):
    
    chunkification_out = {}
    chunkification_out['username'] = username
    # print()
    # print()
    # print("Starting Chunkification for ", username)
    
    # make the usernames lowercased
    u_p = preprocess_username(username)
    chunkification_out['u_p'] = u_p
    
    
    # extract the chunks based on the stopping chars
    chunks_based_on_stopping_chars = extract_chunks_based_on_stop_chars(u_p)
    chunkification_out['chunks_based_on_stopping_chars'] = \
        chunks_based_on_stopping_chars
    
    return chunkification_out
    


def check_direct_matching(u_1, u_2):
    
    # make the usernames lowercased
    u_1_p = preprocess_username(u_1)
    u_2_p = preprocess_username(u_2)
    
    return u_1_p == u_2_p


def preprocess_username(username):
    
    return str(username).lower().strip()


def get_stop_char_score(l1, l2, u_1, u_2):
    
    l1.sort()
    l2.sort()
    
    len_l1 = len(l1)
    len_l2 = len(l2)
    if len_l1 > 0 and len_l2 > 0:
    
        l1, l2 = (l1,l2) if len_l1 > len_l2 else (l2,l1)
        
        s2 = ""
        for c2 in l2:
            s2 += c2
    
    else:
        l1, s2 = (l1,u_2) if len_l1 > 0 else (l2,u_1)
    
    match = 0
    temp = []
    for c1 in l1:
        
        if c1 in s2:
            s2 = s2.replace(c1, '')
            match += 1
        else:
            temp.append(c1)
    
    if len(l1) == match or len(s2) == 0:
        return 1
    else:
        
        if match >= 1:
            
            l1 = temp
            temp_s = s2
            match = 0
            # characterwise
            # print(l1, s2[-1])
            for c1 in l1:
                
                if c1[0] == temp_s[0] or c1[0] == temp_s[-1]:
                    temp_s=temp_s.replace(c1[0], '')
                    match += 1
            if len(l1) == match or len(temp_s) == 0:
                return 1
        
    
    return 0
    
    

    
def find_matching_score(u_1, u_2, write=True):
    
    
    if check_direct_matching(u_1, u_2):
        return 1.0
    else:
        chunkification_out_u_1 = chunkify(u_1)
        chunkification_out_u_2 = chunkify(u_2)
        # print(u_1, u_2, 
        #       chunkification_out_u_1['chunks_based_on_stopping_chars'],
        #       chunkification_out_u_2['chunks_based_on_stopping_chars'])
        
        lower_u_1 = u_1.lower()
        lower_u_2 = u_2.lower()
        c1 = chunkification_out_u_1['chunks_based_on_stopping_chars']
        c2 = chunkification_out_u_2['chunks_based_on_stopping_chars']
        
        if len(c1) > 0 or len(c2) > 0:
            score = get_stop_char_score(c1, c2, lower_u_1, lower_u_2)
            if (not write):
                print(score)
            if score == 1 and write:
                with open('security_chunks.csv', 'a') as fp:                                
                    fp.write(u_1 + ',' + '-'.join(c1) + ',' + \
                                 u_2 + ',' + '-'.join(c2) + ',' + str(score) + '\n')






import pandas as pd

forums=[
            'hack_this_site_usernames',
            'ethical_hacker',
            'wilderssecurity',
            'offensive_community',
            'mpgh',
            'security_stack_exchange',
            'unix_stackexchange',    
]


def main():
    
    forum_1 = pd.read_csv("../Analysis/data/offensive_community_usernames.csv", names=['index', 'name'], index_col = 'index')
    forum_1 = forum_1[['name']]
    
    f1_names = forum_1.to_dict('records')
    
    
    forum_2 = pd.read_csv("../Analysis/data/wilderssecurity_usernames.csv", names=['index', 'name'], index_col = 'index')
    forum_2 = forum_1[['name']]
    
    f2_names = forum_2.to_dict('records')
    
    for iteration_1, record_1 in enumerate(f1_names):
        
        u_1 = str(record_1['name'])
        found = False
        
        for stop_char in ['_', '.', '@']:
            if stop_char in u_1:
                found = True
                break
        if found:
            for iteration_2, record_2 in enumerate(f2_names):
                u_2 = str(record_2['name'])
                found = False
                for stop_char in ['_', '.', '@']:
                    if stop_char in u_2:
                        found = True
                        break
                if found:
                    # print(u_1, u_2)
                    # break
                    find_matching_score(u_1, u_2)
        
    
    # data = data[ [GOOGLE, FACEBOOK, TWITTER] ]
    # # print(data.head())
    
    
    
    # data_map = data.to_dict('records')
    
    # # with open('chunks.csv', 'w') as fp:
        
    # for iteration, record in enumerate(data_map):
        
    #     # print( record[GOOGLE], record[FACEBOOK], record[TWITTER] )
        
    #     u_g = record[GOOGLE]
    #     u_f = record[FACEBOOK]
    #     u_t = record[TWITTER]
        
    #     for stop_char in ['_ -.@']:
    #         if stop_char in u_f:
    #         # print(u_f, u_t)
            
    #             find_matching_score(u_f, u_t)
            
    #     # matching_score_GF = find_matching_score(u_g, u_f)
    #     # matching_score_GT = find_matching_score(u_g, u_t)
    #     # matching_score_FT = str(find_matching_score(u_f, u_t))
        
    #     # # print(record[FACEBOOK], record[TWITTER], matching_score_FT)
    #     # fp.write(\
    #     #     record[FACEBOOK] + ',' + record[TWITTER] + ',' + matching_score_FT + '\n')
        
    #     # if (iteration != 0 and iteration % 100 == 0):
    #     if (iteration == 1000):
    #         print("count", iteration)
    #         break

    
# chunkify('45abc34def90')
# test()
from os.path import exists
if exists('security_chunks.csv'):
    os.remove("security_chunks.csv")
main()
# find_matching_score('hall-marcy','MarcyDH', False)
 

# print (syn1.wup_similarity(syn2))





