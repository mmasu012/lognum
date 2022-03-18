#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:57:46 2022

@author: masud
"""

import pandas as pd
import os
from os.path import exists
import re

def get_digit_vector(data_map, forum_name):
    
    
    list_number_behavior = []
    for iteration, record in enumerate(data_map):
        
        # print(record['name'])
        username = '12a300b410c520d13'
        if len(re.findall('\d+', username)) > 0:
            
            start=re.findall('^\d+', username)
            if len(start) > 0:
                len_start = len(start[0])
            else:
                len_start = 0
            
            end=re.findall('\d+$', username)
            if len(end) > 0:
                len_end = len(end[0])
            else:
                len_end = 0
            
            username = re.sub(r'^[0-9]{1,}', '', username)
            username = re.sub(r'[0-9]{1,}$', '', username)
                
            between_list = re.findall('\d+', username)
            len_between = len(between_list)
            
            print(len_start, len_end, len_between)
            list_number_behavior.append([len_start, len_end, len_between])
        
        
    total_count=len(data_map)
    print(total_count)
    has_digit = len(list_number_behavior)
    
    start_count = 0
    end_count = 0
    between_count = 0
    only_start = 0
    only_end = 0
    only_between  = 0
    
    for record in list_number_behavior:
        
        if record[0] != 0:
             start_count += 1
        
        if record[1] != 0:
            end_count += 1
        
        if record[2] != 0:
            between_count += 1
        
        
    
        
        
        

def show_stats(filename):
    
    
        forum_name = filename
        
        data = pd.read_csv('processed/' + forum_name +'_usernames.csv')
    
        # data['username_length'] = 0
        
        data_map = data.to_dict('records')
        print(forum_name)
        print('total user count', data.shape[0])
    
        get_digit_vector(data_map, forum_name)
    

def main():
    
    
    forum_list = [
        
        'ethical_hacker',
        # 'hack_this_site',
        # 'mpgh',
        # 'security_stack_exchange',
        # 'garage4hackers',
        # 'wilderssecurity',
        # 'offensive_community',
        # 'hack_forums',
        # 'raidforums',
        # 'google_plus',
        # 'facebook',
        # 'twitter',         
    ]

        
    for forum in forum_list:
        
        show_stats(forum)

    
# main()

# start=re.findall('^\d+','ab')[0]
# print(start)

# end=re.findall('\d+$','12a3b2')[0]
# print(end)

# between=re.findall('([^\d]+\d+[^\d])','a3b4c5d')
# print(between)

# print(re.findall('^\d+','ab'))

# username = re.sub(r'^[0-9]{1,}', '', '12a300b410c520d13')
# username = re.sub(r'[0-9]{1,}$', '', username)

print(re.findall('\d+', '12ma1sud12'))
print(re.findall('\d+', '12ma1sud123'))
print(re.findall('\d+', '1ma1sud2'))



