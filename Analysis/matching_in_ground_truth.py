#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 13:35:05 2022

@author: masud
"""
import pandas as pd

fb_twitter_data = pd.read_csv('data/fb_links_twitter_usernames.csv')

print(fb_twitter_data.columns)

fb_twitter_data = fb_twitter_data[ ['facebook', 'twitter'] ]

print(fb_twitter_data.head())

map_data = fb_twitter_data.to_dict(orient='records')

for data in map_data:
    
    
    print(data['facebook'], data['twitter'])
    break