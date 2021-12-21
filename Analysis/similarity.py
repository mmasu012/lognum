#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 02:49:27 2021

@author: masud
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

def get_recommendations(title, cosine_sim, indices,df):
    # Get the index of the movie that matches the title
    idx = indices[title]
    # Get the pairwsie similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores for 10 most similar movies
    sim_scores = sim_scores[1:2]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    return df['username'].iloc[movie_indices[0]]

if __name__ == "__main__":
    
    df = pd.read_csv('chunks.csv').dropna()
    # print(df.columns)
    # print(df.head())
    usernames=df['username'].unique()
    print(len(usernames))
    
    indices = pd.Series(df.index, index=df['username'])
    
    segments = df['merge']
    
    tfidf = TfidfVectorizer()
    
    # Construct the TF-IDF matrix
    tfidf_matrix = tfidf.fit_transform(segments)
    
    # Generate the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    # Generate recommendations
    usernames=df['username'].unique()
    # print(len(usernames))
    for username in usernames:
        print(username, get_recommendations(username, cosine_sim, indices,df))
