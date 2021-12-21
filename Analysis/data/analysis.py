#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 19:38:26 2021

@author: masud
"""

# https://realpython.com/pandas-groupby/

import pandas as pd
import os

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
         
         forum_name=filename.replace('_usernames.csv', '')
         
         if forum_name in forums and filename.endswith('.csv'):
             
             df=pd.read_csv(filename, names=colnames, header=None)
             print(filename, df.shape)
             df['forum_name']=forum_name
             df_arr.append(df[['username', 'forum_name']])
    
    forums_usernames=pd.concat(df_arr, ignore_index=True)
    forums_usernames['forum_name'].replace(forums,forums_shorts,inplace=True)
    print(forums_usernames.shape)
    

    boolean_series = forums_usernames.forum_name.isin(forums_shorts[:-2])
    forums_usernames_except_stackexchange = forums_usernames[boolean_series]
    print(forums_usernames_except_stackexchange.shape)
    
    return forums_usernames, forums_usernames_except_stackexchange

def dump_exact_matching (data, out_filename):
    exact_matchings={
        'username':[], 'forums':[], 'count':[],
    }
    for _, g in data.groupby(['username']):
        if len(g) >= 3:
            matched_forum_list=list(g['forum_name'])
            exact_matchings['username'].append(g['username'].iloc[0])
            exact_matchings['forums'].append(matched_forum_list)
            exact_matchings['count'].append(len(matched_forum_list))
            # print(g['username'].iloc[0], matched_forum_list, len(matched_forum_list))
        
    for _, g in data.groupby(['username']):
        if len(g) == 2:
            matched_forum_list=list(g['forum_name'])
            exact_matchings['username'].append(g['username'].iloc[0])
            exact_matchings['forums'].append(matched_forum_list)
            exact_matchings['count'].append(len(matched_forum_list))
            # print(g['username'].iloc[0], matched_forum_list, len(matched_forum_list))
    
    df=pd.DataFrame(data=exact_matchings)
    df.to_csv(out_filename)

if __name__ == "__main__":
    
    forums_usernames, forums_usernames_except_stackexchange = read_usernames()
    dump_exact_matching(forums_usernames, 'exact_match_all.csv')
    dump_exact_matching(forums_usernames_except_stackexchange, 'exact_match_except_ss.csv')        
    
    # print(forums_usernames.shape)
    
    for forum in forums_shorts:
        # print(forum, forums_usernames[forums_usernames['forum_name'] == forum].shape)
        df=forums_usernames[forums_usernames['forum_name'] == forum]
        
        # df['username_length']=df['username'].str.len()
        df['username']=df['username'].astype(str)
        df['username_length']=df['username'].apply(lambda x: len(x))
        # print(df.head())
        print(forum,df['username_length'].mean())
    

# """
#     for _, g in forums_usernames_except_stackexchange.groupby(['username']):
#         if len(g) > 1:
#             matched_forum_list=list(g['forum_name'])
#             print(g['username'].iloc[0], matched_forum_list, len(matched_forum_list))"""
        