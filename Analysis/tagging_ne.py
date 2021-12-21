#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 16:21:16 2021

@author: masud
"""
# https://blog.ouseful.info/2017/09/04/simple-text-analysis-using-python-identifying-named-entities-tagging-fuzzy-string-matching-and-topic-modelling/
# https://pypi.org/project/geotext/

import pandas as pd
from geotext import GeoText

df = pd.read_csv('chunkification_output_2.csv')

# # print(df.head())

##################### Countries
# iter=0
# countries={}
# for i, row in df.iterrows():
    
#     chunks = row['all_meaningful_chunks']
#     username = row['username']
#     forum = row['forum_name']
    
#     # print(chunks)
    
#     places = GeoText(str(chunks).title()).countries
#     # print(len(places))
#     if len(places) > 0:
#         print(username, forum, places)
        
#         iter+=1
#         if places[0] not in countries:
#             countries[places[0]]=1
#         else:
#             countries[places[0]]+=1
        
# print(iter)
# print(countries.items())
# print(len(countries))


#################### Malware Terms
# keywords=['Adware',
#           'DDoS','Exploit','Hack','Monitoring', 'Malware', 'botnet',
#           'Ransom','RemoteAccess', 'Ransomware', 'Spam', 'Spoof',
#           'Spammer','Spoofer','Trojan', 'sniffer', 'backdoor',
#           'Spyware', 'Rootkit', 'Keylogger', 'Hacker', 'rat', 'attack',
#           'TrojanSpy','Virus','Worm', 'hacking',
#           'spoofing', 'sniffing', 'spamming']

# for iter, keyword in enumerate(keywords):
    
#     keywords[iter]=keywords[iter].lower()

# iter=0
# hack_terms={}
# for i, row in df.iterrows():
    
#     chunks = str(row['all_meaningful_chunks']).split(',')
#     username = row['username']
#     forum = row['forum_name']
    
#     # print(chunks)
    
#     for chunk in chunks:
#         if chunk in keywords:
#             print(username, forum, chunk)
#             iter+=1
#             if chunk not in hack_terms:
#                 hack_terms[chunk]=0
#             else:
#                 hack_terms[chunk]+=1

# print(iter)
# print(hack_terms.items())

# colnames=['index', 'username']

# df_cc = pd.read_csv('data/cc_usernames.csv', names=colnames, header=None)
# unique_cc=df_cc['username'].unique()
# print(len(unique_cc))

# df_oc = pd.read_csv('data/offensive_community_usernames.csv', names=colnames, header=None)
# unique_oc=df_oc['username'].unique()
# print(len(list(set( list(unique_cc) + list(unique_oc) ) )))


############## Numeric Use







        