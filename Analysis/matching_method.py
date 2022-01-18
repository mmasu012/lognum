#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 11:42:59 2021

@author: masud
"""

import pandas as pd
from fuzzywuzzy import fuzz
import statistics


def get_numerical_similarity(number_list_1, number_list_2):
    
    # print(number_list_1, number_list_2)
    match_count = len(list(set(number_list_1).intersection(set(number_list_2))))
    return ( 2 * match_count) / (len(number_list_1) + len(number_list_2))

def get_transformed_similarity(transformed_username_list, username):
    
    highest=0.0
    for transformed_username in transformed_username_list:
        temp = fuzz.ratio(transformed_username, username)
        if temp > highest:
            highest = temp
    # highest = process.extractOne(username,transformed_username_list)
    # print(username,transformed_username_list)
    # print(highest)
    
    return highest/100

def get_punctuation_chunks_similarity(str_list_1, str_list_2):
    
    score=0.0
    for str_1 in str_list_1:
        
        for str_2 in str_list_2:
            score += (fuzz.ratio(str_1, str_2) / 100)
            
    return score/(len(str_list_1)*len(str_list_2) + 1)


def get_meaningful_chunks_similarity(str_list_1, str_list_2):
    
    # scores = [[0]*len(str_list_1)]*len(str_list_2)
    score=0.0
    for str_1 in str_list_1:
        
        for str_2 in str_list_2:
            score += (fuzz.ratio(str_1, str_2) / 100)
            
    return score/(len(str_list_1)*len(str_list_2) + 1)

def get_transformed_meaningful_chunks_similarity(str_list_1, str_list_2):
    
    # scores = [[0]*len(str_list_1)]*len(str_list_2)
    highest=0.0
    for str_1 in str_list_1:
        
        for str_2 in str_list_2:
            temp = fuzz.ratio(str_1, str_2)
            if temp > highest:
                temp = highest
            
    return highest/100


def get_total_similarity_score(user1_seg_info, user2_seg_info) :
    
    # numerical similarity
    numerical_similarity=0.0
    
    
    number_list_1=user1_seg_info['numbers'].split(',') \
        if user1_seg_info['numbers'] != '' else []
    number_list_2=user2_seg_info['numbers'].split(',') \
        if user2_seg_info['numbers'] != '' else []
    
    if len(number_list_1) > 0 and len(number_list_2) > 0:
        numerical_similarity=get_numerical_similarity( \
                number_list_1, number_list_2)
    
    # print(numerical_similarity)
    
    # transformed username similarity
    transformed_similarity=0.0
    
    if user1_seg_info['is_transformed'] or user2_seg_info['is_transformed']:
        
        if user1_seg_info['is_transformed']:
            transformed_username_list = user1_seg_info['transformed_usernames'].strip(',')
            username = user2_seg_info['username'].lower()
            
            transformed_similarity+=get_transformed_similarity( \
                      transformed_username_list, username)
                
        if user2_seg_info['is_transformed']:
            transformed_username_list = user2_seg_info['transformed_usernames'].strip(',')
            username = user1_seg_info['username'].lower()
            
            transformed_similarity+=get_transformed_similarity( \
                      transformed_username_list, username)
        
        if user1_seg_info['is_transformed'] and user2_seg_info['is_transformed']:
            transformed_similarity/=2
        
    
    # print(transformed_similarity)
    
    # punctuation chunks similarity
    punctuation_chunks_similarity=0.0
    if user1_seg_info['has_punctuation'] or user2_seg_info['has_punctuation']:
            
        punctuation_chunks_similarity=get_punctuation_chunks_similarity( \
                      user1_seg_info['puncutuation_chunks'].strip(','), 
                      user2_seg_info['puncutuation_chunks'].strip(',')                                   
        )
    
    # print(punctuation_chunks_similarity)
    
    
    # meaningful chunks similarity
    meaningful_chunks_similarity=0.0
    meaningful_chunks_similarity=get_meaningful_chunks_similarity( \
                      user1_seg_info['meaningful_chunks'].strip(','),
                      user2_seg_info['meaningful_chunks'].strip(',')                                
    )
    
    # print(meaningful_chunks_similarity)
    
    # transformed meaningful chunks similarity
    transformed_meaningful_chunks_similarity = 0.0
    transformed_meaningful_chunks_similarity=get_transformed_meaningful_chunks_similarity( \
                      user1_seg_info['transformed_meaningful_chunks'].strip(','),
                      user2_seg_info['transformed_meaningful_chunks'].strip(',')                                
    )
    
    # print(transformed_meaningful_chunks_similarity)
    
    total_similarity_score = statistics.mean([ numerical_similarity, \
                               transformed_similarity,
                               punctuation_chunks_similarity,
                               meaningful_chunks_similarity,
                               transformed_meaningful_chunks_similarity ])
    
    return total_similarity_score

def is_candidate(str1, str2):
    
    
    if len(str1) == 0 or len(str2) == 0:
        return False
    
    found=0
    for char in str1:
        
        if char in str2:
            found+=1
    
    
    
    percentage=(found/len(str2))*100
    
    if percentage >= 50:
        return True


forums_usernames = pd.read_csv('re_chunkification_output.csv')
forums_usernames=forums_usernames.set_index('index')

forums_usernames['username']=forums_usernames['username'].astype(str)
forums_usernames['numbers']=forums_usernames['numbers'].astype(str)
forums_usernames['transformed_usernames']=forums_usernames['transformed_usernames'].astype(str)
forums_usernames['is_transformed']=forums_usernames['is_transformed'].astype(bool)
forums_usernames['puncutuation_chunks']=forums_usernames['puncutuation_chunks'].astype(str)
forums_usernames['has_punctuation']=forums_usernames['has_punctuation'].astype(bool)
forums_usernames['meaningful_chunks']=forums_usernames['meaningful_chunks'].astype(str)
forums_usernames['transformed_meaningful_chunks']=forums_usernames['transformed_meaningful_chunks'].astype(str)
forums_usernames['all_meaningful_chunks']=forums_usernames['all_meaningful_chunks'].astype(str)



forums_usernames['numbers'].fillna('', inplace=True)

print(forums_usernames.columns)
print(forums_usernames.head())

# print(forums_usernames.iloc[0]['username'])


total_count=forums_usernames.shape[0]
# # scores = [[0]*total_count]*total_count

candidate_mapping = [[True]*total_count]*total_count


matching=[]
forums_usernames = forums_usernames.to_dict(orient='records')
for i, rowi in enumerate(forums_usernames):
    
    print('current index', i)
    best_similarity_index = -1
    best_similarity_score = 0.0
    for j, rowj in enumerate(forums_usernames):
        
        # if not candidate_mapping[i][j] or i==j:
        #     continue
        
        # if is_candidate(rowi['username'], rowj['username']):
            
        total_similarity_score = get_total_similarity_score(rowi, rowj)
        # print(rowi['index'], rowj['index'])
        # scores[rowi['index']][rowj['index']]=total_similarity_score
        
        if total_similarity_score >= best_similarity_score:
            best_similarity_index=j
            best_similarity_score=total_similarity_score
        # else:
        #     candidate_mapping[i][j]=False
        #     candidate_mapping[j][i]=False
 
    if best_similarity_index != -1:
        username_1 = forums_usernames[i]['username']
        forum_1 = forums_usernames[i]['forum_name']
        
        username_2 = forums_usernames[best_similarity_index]['username']
        forum_2 = forums_usernames[best_similarity_index]['forum_name']
        
        # print(username_1, forum_1, username_2, forum_2, best_similarity_score)
        with open('ouput_test.csv', 'a') as ouput:
            ouput.write(username_1 + ',' + forum_1 + ',' + username_2 + ',' + \
                      forum_2+ ',' + str(best_similarity_score) + '\n')
        matching.append([username_1, forum_1, username_2, forum_2, best_similarity_score])
        

   

# matching=[]
# for i in range(0, len(scores)):
    
#     similarity_index = 0
#     similarity_score = 0.0
#     for j in range(0, len(scores)):
        
#         if i!=j and scores[i][j] > similarity_score:
#             similarity_index=j
#             similarity_score=scores[i][j]
            
#     username_1 = forums_usernames[forums_usernames['index']==i]['username'][0]
#     forum_1 = forums_usernames[forums_usernames['index']==i]['forum_name'][0]
    
#     username_2 = forums_usernames[forums_usernames['index']==j]['username'][0]
#     forum_2 = forums_usernames[forums_usernames['index']==j]['forum_name'][0]
    
#     matching.append([username_1, forum_1, username_2, forum_2, similarity_score])

df_output=pd.DataFrame(matching, columns=['username_1', 'forum_1', 'username_2', 'forum_2',
                                'similarity_score'])

df_output.to_csv('matching_found_test.csv')

        
            
            
                
    
    
    