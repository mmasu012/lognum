#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 16:21:16 2021

@author: masud
"""
# https://blog.ouseful.info/2017/09/04/simple-text-analysis-using-python-identifying-named-entities-tagging-fuzzy-string-matching-and-topic-modelling/
# https://pypi.org/project/geotext/
# ((?![0-9]).)[4]{2,}$
# 54+105+89+48+28+40+52+73+54+96
# 36+45+43+37+16+20+24+80+64+42
import pandas as pd
from geotext import GeoText

df = pd.read_csv('re_chunkification_social_output.csv')

# print(df['numbers'].describe())
# print(df['numbers'].value_counts().idxmax())
# print(df['numbers'].count())

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


# # ################### Malware Terms
# keywords=['Adware',
#           'DDoS','Exploit','Hack','Monitoring', 'Malware', 'botnet',
#           'Ransom','RemoteAccess', 'Ransomware', 'Spam', 'Spoof',
#           'Spammer','Spoofer','Trojan', 'sniffer', 'backdoor',
#           'Spyware', 'Rootkit', 'Keylogger', 'Hacker', 'attack',
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
#                 hack_terms[chunk]=1
#             else:
#                 hack_terms[chunk]+=1

# print(iter)
# print(hack_terms.items())

# # does numerics mean valid year
# def valid_year(year):
#   if year and year.isdigit():
#     year = int(year)
#     if year >=1900 and year <=2021:
#       return True
#     else:
#         return False
    
# iter=0
# for i, row in df.iterrows():
    
#     chunks = str(row['numbers']).split(',')
#     username = row['username']
#     # print(chunks)
    
#     for chunk in chunks:
        
#         if valid_year(chunk):
#             iter+=1
#             print(username, chunk)
            
# print(iter)

# # Valid english meaningful word
# import enchant
# d = enchant.Dict("en_US")

# iter=0
# for i, row in df.iterrows():
    
#     chunks = str(row['all_meaningful_chunks']).split(',')
#     username = row['username']
#     # print(chunks)
  
#     for chunk in chunks:
        
#         if len(chunk) >= 4 and d.check(chunk):
            
            
#             iter+=1
            
#             print(username, chunk)
#             break

# print(iter)

# # username length
# df['length'] = df['username'].str.len()
# print(df[['username', 'length']])
# print(df['length'].describe())
# hist = df['length'].hist(bins=36)
# hist.set_xlabel("length of login name(cybersecurity forums)")
# hist.set_ylabel("frequency")
# print(df[df['length'] == 36]['username'])

# # segmentation length
# df['segments_count'] = df.apply(lambda x: len(str(x['meaningful_chunks']).split(',')), axis=1)
# print(df[['username', 'segments_count']])
# print(df['segments_count'].describe())
# hist = df['segments_count'].hist(bins=13)
# hist.set_xlabel("count of segments(cybersecurity forums)")
# hist.set_ylabel("frequency")

# # how many slangification
print(df[df['is_transformed'] == True].shape[0])
import enchant
d = enchant.Dict("en_US")

iter=0
for i, row in df.iterrows():
    
    if row['is_transformed']:
        chunks = str(row['meaningful_chunks']).split(',')
        transformed_chunks = str(row['transformed_meaningful_chunks']).split(',')
        username = row['username']
        # print(chunks)
      
        for transformed_chunk in transformed_chunks:
            
            if d.check(transformed_chunk) and transformed_chunk not in chunks:
            
                iter+=1
                
                # print(username, chunks, transformed_chunks)
                break

print(iter)


# print(str(df['meaningful_chunks']).split(','))
# print(df[df['segments_count'] == 50]['username'])

# colnames=['index', 'username']

# df_cc = pd.read_csv('data/cc_usernames.csv', names=colnames, header=None)
# unique_cc=df_cc['username'].unique()
# print(len(unique_cc))

# df_oc = pd.read_csv('data/offensive_community_usernames.csv', names=colnames, header=None)
# unique_oc=df_oc['username'].unique()
# print(len(list(set( list(unique_cc) + list(unique_oc) ) )))


############## Numeric Use







        