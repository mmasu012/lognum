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

def get_numeric_score(nums1, nums2):
    
    if len(nums1) == 0 or len(nums2) == 0:
        return -1
    
    nums1 = set(nums1)
    nums2 = set(nums2)
    
    common = list(nums1.intersection(nums2))
    if len(common) > 0:
        return 1
    else:
        return 0


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
    
    

def get_capital_char_score(l1, l2):
    
    if len(l1) == 0 or len(l2) == 0:
        return 0
    
    score = 0
    for val1 in l1:
        
        for val2 in l2:
            
            score += jaro.jaro_winkler_metric(val1, val2)
            
    return round((score+.1)/(len(l1)*len(l2)), 2)


def get_meaningful_chunk_score(l1, l2):
    
    if len(l1) == 0 or len(l2) == 0:
        return 0
    
    score = 0
    for val1 in l1:
        for val2 in l2:
            
            if val1 == val2:
            
                score += 1
            
    return round((score+.1)/(len(l1)*len(l2)), 2)


def get_meaningless_chunk_score(l1, l2):
    
    if len(l1) == 0 or len(l2) == 0:
        return 0
    
    score = 0
    for val1 in l1:
        for val2 in l2:
            
            if val1 == val2:
            
                score += jaro.jaro_winkler_metric(val1, val2)
            
    return round((score+.1)/(len(l1)*len(l2)), 2)


def get_slangification_score(l1, u):
    
    if len(l1) == 0:
        return 0
    
    for val1 in l1:
        
        if val1 == u:
            return 1
        
    return 0


def get_sentiment_score(val1, val2):
    
    if val1 == 0 and val2 ==0:
        return -1
    
    if val1 > 0 and val2 > 0:
        return 1
    
    if val1 < 0 and val2 < 0:
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
            if write:
                with open('chunks.csv', 'a') as fp:                                
                    fp.write(u_1 + ',' + '-'.join(c1) + ',' + \
                                 u_2 + ',' + '-'.join(c2) + ',' + str(score) + '\n')
 
        
        # numeric_score = \
        #     get_numeric_score(chunkification_out_u_1['nums_in_username'],
        #                   chunkification_out_u_2['nums_in_username'])
        # # print(numeric_score)
        
        # stop_char_score = \
        #     get_stop_char_score(\
        #             chunkification_out_u_1['chunks_based_on_stopping_chars'],
        #             chunkification_out_u_2['chunks_based_on_stopping_chars'])
        
        # # print(stop_char_score)
        
        # capital_char_score = \
        #     get_capital_char_score(\
        #             chunkification_out_u_1['chunks_based_on_capital_letters'],
        #             chunkification_out_u_2['chunks_based_on_capital_letters'])
        
        # # print(capital_char_score)
        
        # meaningful_chunk_score = \
        #     get_meaningful_chunk_score(\
        #             chunkification_out_u_1['meaningful_chunks_ori'],
        #             chunkification_out_u_2['meaningful_chunks_ori'])
                
        # # print(meaningful_chunk_score)
        
        # meaningless_chunk_score = \
        #     get_meaningless_chunk_score(\
        #             chunkification_out_u_1['meaningless_chunks_ori'],
        #             chunkification_out_u_2['meaningless_chunks_ori'])
                
        # # print(meaningless_chunk_score)
        
        # slangification_score = \
        #     get_slangification_score(\
        #             chunkification_out_u_1['slangified_usernames'],
        #             chunkification_out_u_2['username'])
                
        # # print(slangification_score)
        
        # sentiment_score = \
        #     get_sentiment_score(\
        #             chunkification_out_u_1['sentiment_score_ori'],
        #             chunkification_out_u_2['sentiment_score_ori'])
        
        # # print(sentiment_score)
        
        # # chunkification_out['sentiment_score_ori'] = sentiment_score_ori
        # scores = []
        # string_score = [stop_char_score, capital_char_score, 
        #                   meaningful_chunk_score, meaningless_chunk_score,
        #                   slangification_score]
        # scores.append(max(string_score))
        
        
        # if numeric_score != -1:
        #     scores.append(numeric_score)
         
        # if sentiment_score != -1:
        #     scores.append(sentiment_score)
            
        # final_score = round(sum(scores) / len(scores), 2)
        
        # return final_score





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
    
    # with open('chunks.csv', 'w') as fp:
        
    for iteration, record in enumerate(data_map):
        
        # print( record[GOOGLE], record[FACEBOOK], record[TWITTER] )
        
        u_g = record[GOOGLE]
        u_f = record[FACEBOOK]
        u_t = record[TWITTER]
        
        if '.' in u_f:
            # print(u_f, u_t)
            
            find_matching_score(u_f, u_t)
            
        # matching_score_GF = find_matching_score(u_g, u_f)
        # matching_score_GT = find_matching_score(u_g, u_t)
        # matching_score_FT = str(find_matching_score(u_f, u_t))
        
        # # print(record[FACEBOOK], record[TWITTER], matching_score_FT)
        # fp.write(\
        #     record[FACEBOOK] + ',' + record[TWITTER] + ',' + matching_score_FT + '\n')
        
        # if (iteration != 0 and iteration % 100 == 0):
        if (iteration == 1000):
            print("count", iteration)
            break

def test():
    
    # extract_numerics('45Abc.34@def90')
    
    # extract_chunks_based_on_stop_chars('45Abc34def90')
    # extract_chunks_based_on_stop_chars('45abc.34@dEf90')
    
    # extract_chunks_based_on_capital_letters('45abc.34@dEf90')
    # extract_chunks_based_on_capital_letters('RichBohn')

    # extract_meaningful_chunks('dhakaprckfloweradicateindiabangladeshteacherhonestbadgoodhappyfightlovetrojanspywaremalwareddos')
    # slangify('h@ck3rsc0r3')
    # extract_meaningful_chunks('abcd12wer')
    # extract_meaningful_chunks('devil')
    # extract_meaningful_chunks('satan')
    # print(is_abbrev("rmasuds", "masudkarim"))
    # find_matching_score('abc45def89', 'def44')
    find_matching_score('aBc45.def89', 'dEf.l')
    
# chunkify('45abc34def90')
# test()
from os.path import exists
if exists('chunks.csv'):
    os.remove("chunks.csv")
main()
# find_matching_score('hall-marcy','MarcyDH', False)

# l1 = [1,2]
# l2 = [1,2,3]
# len_l1 = len(l1)
# len_l2 = len(l2)
# if len_l1 > 0 and len_l2 > 0:
    
#     l1, l2 = (l1,l2) if len_l1 > len_l2 else (l2,l1)
# print(l1,l2)



# print(jaro.jaro_winkler_metric(u'SHACKLEFORD', u'SHACKELFORD'))
# a = ["williamjuniorsmith", "juniorwilliams"]
# st = STree.STree(a)
# print(st.lcs()) # "abc"
  
# def is_abbrev(abbrev, text):
#     pattern = ".*".join(abbrev.lower())
#     print(pattern)
#     return re.match("^" + pattern, text.lower()) is not None

# import re    
# def is_abbrevs(abbrev, text):
#     pattern = "(|.*\s)".join(abbrev.lower())
#     return re.match("^" + pattern, text.lower()) is not None

# print(is_abbrevs( "juniorwilliams", "williamjuniorsmith"))

 
# syn1 = wordnet.synsets('devil')[0]
# syn2 = wordnet.synsets('bad')[0]
 

# print (syn1.wup_similarity(syn2))





