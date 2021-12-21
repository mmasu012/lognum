#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 22:41:06 2021

@author: masud
"""
# https://jeremykun.com/2012/01/15/word-segmentation/
# https://goodboychan.github.io/python/datacamp/natural_language_processing/2020/07/17/04-TF-IDF-and-similarity-scores.html

import pandas as pd
import os
import re
import time
from wordsegment import load, segment
load()

slang_map={
    '0': ['o'],
    '1': ['i', 'l', 't'],
    '2': ['z'],
    '3': ['e', 's'],
    '4': ['a', 'r'],
    '5': ['s'],
}

forums=[
            'hack_this_site',
            'ethical_hacker',
            'wilderssecurity',
            'offensive_community',
            'mpgh',
            'security_stack_exchange',
            'unix_stackexchange',    
]

forums_shorts=[
            'htt',
            'eh',
            'ws',
            'oc',
            'mpgh',
            'ss',
            'us',    
]

def read_usernames ():
    currdir=os.getcwd()
    # print(currdir)
    
    df_arr=[]
    colnames=['index', 'username']
    for file in os.listdir(currdir):
         filename = os.fsdecode(file)
         
         if filename.endswith('.csv'):
             df=pd.read_csv(filename, names=colnames, header=None)
             # print(filename, df.shape)
             df['forum_name']=filename.replace('_usernames.csv', '')
             df_arr.append(df[['username', 'forum_name']])
    
    forums_usernames=pd.concat(df_arr, ignore_index=True)
    forums_usernames['forum_name'].replace(forums,forums_shorts,inplace=True)
    print(forums_usernames.shape) 
    boolean_series = forums_usernames.forum_name.isin(forums_shorts[:-2])
    forums_usernames_except_stackexchange = forums_usernames[boolean_series]
    print(forums_usernames_except_stackexchange.shape)
    
    return forums_usernames, forums_usernames_except_stackexchange

def slangify(username):
    
    if len(username) == 1:
        return []
    
    trailing_digits=re.findall(r'[0-9]+$',username)
    leading_digits=re.findall(r'^[0-9]+',username)
    
    if len(trailing_digits) > 0:
        if len(trailing_digits[0]) > 1:
            username=username[:-len(trailing_digits[0])]
    
    if len(leading_digits) > 0:
        if len(leading_digits[0]) > 1:
            username=username.replace(leading_digits[0], '', 1)
    
    slangified_names=[username]
    for char in username:
    
        if char in slang_map:
            lst=[]
            replacements=slang_map[char]
            for replacement in replacements:
                    
                for item in slangified_names:
                    lst.append(item.replace(char, replacement))
            
            slangified_names=lst
    
    if username in slangified_names:
        slangified_names.remove(username)
    chunklist=[]
    for name in slangified_names:
        chunklist=chunklist+[name]+segment(name)
    
    return chunklist
            

def chunkify(username):
    
    chunk_group=[]
    merge_group=""
    
    # using tool
    # print(type(username))
    chunklist_1=segment(username.lower())
    # chunk_group=chunk_group+list(set(chunklist_1))
    chunk_group.append(','.join(list(set(chunklist_1))))
    
    
    # using separator
    chunklist_2=re.split('[_ -.@]', username.lower())
    chunk_group.append(','.join(list(set(chunklist_2))))
    # chunk_group=chunk_group+list(set(chunklist_2))
    
    # removeing digits
    trailing_digits=re.findall(r'[0-9]+$',username.lower())
    leading_digits=re.findall(r'^[0-9]+',username.lower())
    # print(leading_digits, trailing_digits)
    
    digits_removed=username
    chunklist_3=[]
    if len(leading_digits) > 0:
        digits_removed=username.replace(leading_digits[0], '', 1)
        chunklist_3.append(leading_digits[0])
        
    if len(trailing_digits) > 0:
        digits_removed=digits_removed[:-len(trailing_digits[0])]
        chunklist_3.append(trailing_digits[0])
        
    # print(digits_removed)
    
    if username != digits_removed:
        chunklist_3=chunklist_3+segment(digits_removed.lower())
        # print(chunklist_3)
    chunk_group.append(','.join(list(set(chunklist_3))))
    # chunk_group=chunk_group+list(set(chunklist_3))
    
    # reversing
    reversed_username = digits_removed[::-1].lower()
    chunklist_4=[reversed_username]
    # chunklist_4=segment(reversed_username.lower())
    chunk_group.append(','.join(list(set(chunklist_4))))
    # chunk_group=chunk_group+list(set(chunklist_4))
    
    # slangify
    chunklist_5=slangify(username.lower())
    chunk_group.append(','.join(list(set(chunklist_5))))
    # chunk_group=chunk_group+list(set(chunklist_5))
    
    merge_group=merge_group+','.join(chunk_group)
    merge_group=merge_group.split(',')
    merge_group=' '.join(list(set(merge_group))).strip()
    chunk_group.append(merge_group)
    # print(merge_group)
    
    # print(chunk_group)
    return chunk_group
    # chunklist_2=re.split('; |, |\*|\n',username)
    
    

if __name__ == "__main__":
    
    forums_usernames, forums_usernames_except_stackexchange = read_usernames()
    # print(forums_usernames.columns)
    unique_names=list(forums_usernames['username'].unique())
    # print(len(unique_names))
    
    chunkification_map={}
    
    for username in  unique_names:
        # print(username)
        username=str(username).strip()
        segments=chunkify(username)
        # print(username, segments)
        
        
        chunkification_map[username]=segments
        
        # time.sleep(.25)
    
    df = pd.DataFrame.from_dict(chunkification_map, orient = 'index',
                                columns=['word_segment', 
                                         'punctuation_segment','numeric_segment',
                                         'reverse', 'slangify',
                                         'merge'])
    
    df.to_csv('chunks.csv')
    
    
    