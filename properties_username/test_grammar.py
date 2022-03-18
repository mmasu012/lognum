#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:52:40 2022

@author: masud
"""

from parsimonious.grammar import Grammar

grammar = Grammar(
"""
        hacking_name  = number text number
        text       = ~"[A-Z]*"i
        number = ~"\d+"i
""")


name_list = ["012masud92", "masud012"]
for username in name_list:
    
    print()
    print(username)
    try:
        
        print (grammar.parse(username))
        print('Geeky behavior')
    except Exception as e:
        print('Usual naming behavior')


# r"\b(?=\w)" + re.escape(TEXTO) + r"\b(?!\w)"