# -*- coding: utf-8 -*-
import re
from wordsegment import load, segment
load()

def extract_numerics(username):
    
    # extract numbers/digits from the string
    nums_in_username=re.findall(r'[0-9]{1,}', username)
    print(nums_in_username)
    
    return nums_in_username

def discard_numerics_at_ends(username):
    
    # discard leading/trailing numerics
    username = re.sub(r'^[0-9]{1,}', '', username)
    username = re.sub(r'[0-9]{1,}$', '', username)
    
    return username

# Motivation
# Attempting to find the chunks provided by users
# Remove numbers from start-end
# if stopping chars find any in-between numbers, they are of valuable meanings  
def extract_chunks_based_on_stop_chars(username):
    
    username = discard_numerics_at_ends(username)
    
    # split based on stopping characters
    chunks_based_on_stopping_chars=re.split('(?=[A-Z]) | [_ -.@]', username)
    
    if username in chunks_based_on_stopping_chars:
        chunks_based_on_stopping_chars.remove(username)
    
    print('Chunks based on stopping chars', chunks_based_on_stopping_chars)
    
    return chunks_based_on_stopping_chars


# # Motivation
# # Attempting to find the chunks provided by users
# def extract_chunks_based_on_capital_letters(username):
    
#     username = discard_numerics_at_ends(username)
#     re.findall('[A-Z][a-z]*', username)

# def extract_meaningful_chunks(chunks):
    
#     # extract meaningful words
#     meaningful_chunks=[]
#     for chunk in chunks:
#         segment_list=segment(chunk)
#         for seg in segment_list:
#             # if seg in words.words():
#             meaningful_chunks.append(seg)
# #     print('Meaningful chunks', meaningful_chunks)
    
#     return meaningful_chunks

# transformer_map={
#     '0': ['o'],
#     '1': ['i', 'l', 't'],
#     '2': ['z'],
#     '3': ['e', 's'],
#     '4': ['a', 'r'],
#     '5': ['s'],
#     '@': ['a'],
#     '!': ['i'],
    
# }

# def transform(username):
    
#     transformed_usernames=[username]
#     for char, transformer_vals in transformer_map.items():
        
#         if char in username:
#             temp=[]
#             for val in transformer_vals:
                
#                 for username in transformed_usernames:
#                     temp.append( username.replace(char, val) )
#             transformed_usernames=temp
            
#     transformed_usernames = list(set(transformed_usernames))
# #     print('Transformed usernames', transformed_usernames)
    
#     chunks_based_on_stopping_chars=[]
#     meaningful_chunks=[]
#     for username in transformed_usernames:
#         chunks_based_on_stopping_chars = chunks_based_on_stopping_chars + extract_chunks_based_on_stop_chars(username)
#         meaningful_chunks = meaningful_chunks + extract_meaningful_chunks(chunks_based_on_stopping_chars)
    
#     chunks_based_on_stopping_chars = list(set(chunks_based_on_stopping_chars))
#     meaningful_chunks = list(set(meaningful_chunks))
    
# #     print('Chunks based on stopping chars', chunks_based_on_stopping_chars)
# #     print('Meaningful chunks', meaningful_chunks)    

#     return transformed_usernames, chunks_based_on_stopping_chars, meaningful_chunks

def chunkify(username):
    
    # make the usernames lowercased
    u_p = preprocess_username(username)
    
    # extract the numbers from the username
    nums_in_username = extract_numerics(u_p)
    
    # extract the chunks based on the stopping chars
    chunks_based_on_stopping_chars = extract_chunks_based_on_stop_chars(u_p)
    
    # extract the chunks based on the uppercase letter
    
    
    # meaningful_chunks = extract_meaningful_chunks(chunks_based_on_stopping_chars)
    
    # transformed_usernames, transformed_chunks_based_on_stopping_chars, \
    #         transformed_meaningful_chunks = transform(username_numerics_removed)
    
    
    
    # return [numbers_in_prefix_suffix, chunks_based_on_stopping_chars, transformed_chunks_based_on_stopping_chars, \
    #         meaningful_chunks, transformed_meaningful_chunks]
#     print('Numbers found', numbers_in_prefix_suffix)
#     print('Chunks found',  all_chunks)
#     print('Meaningful chunks found',  all_meaningful_chunks)


def check_direct_matching(u_1, u_2):
    
    # make the usernames lowercased
    u_1_p = preprocess_username(u_1)
    u_2_p = preprocess_username(u_2)
    
    return u_1_p == u_2_p


def preprocess_username(username):
    
    return str(username).lower().strip()

def find_matching_score(u_1, u_2):
    
    
    if check_direct_matching(u_1, u_2):
        return 1.0
    else:
        chunkify(u_1)
        chunkify(u_2)
        return 0.0





import pandas as pd

GOOGLE='google_plus'
FACEBOOK='facebook'
TWITTER='twitter'

def main():
    
    data = pd.read_csv('fb_links_twitter_usernames.csv')
    # print(data.columns)
    
    data = data[ [GOOGLE, FACEBOOK, TWITTER] ]
    # print(data.head())
    
    
    data_map = data.to_dict('records')
    for iteration, record in enumerate(data_map):
        
        # print( record[GOOGLE], record[FACEBOOK], record[TWITTER] )
        
        u_g = record[GOOGLE]
        u_f = record[FACEBOOK]
        u_t = record[TWITTER]
        
        # matching_score_GF = find_matching_score(u_g, u_f)
        # matching_score_GT = find_matching_score(u_g, u_t)
        matching_score_FT = find_matching_score(u_f, u_t)
        
        print(record[FACEBOOK], record[TWITTER], matching_score_FT)
        
        
        if (iteration == 2):
            break

def test():
    extract_numerics('45abc.34@def90')
    extract_chunks_based_on_stop_chars('45abc34def90')
    extract_chunks_based_on_stop_chars('45abc.34@def90')

# chunkify('45abc34def90')
# test()
main()

