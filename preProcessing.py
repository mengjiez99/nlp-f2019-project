#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 11:22:40 2019

@author: xinning.w
"""
import pandas as pd
import numpy as np

import loader
import base


# =============================================================================
# Process Text Data
# =============================================================================
def htmlTagRemover(df):
    df['Abstract'] = df['Abstract'].apply(lambda x: base.htmlTagRemover(x))
    
    return df

def characterRemover(df):
    df['Abstract'] = df['Abstract'].apply(lambda x: base.characterRemover(x))
    
    return df

def tokenizer(df):
    df['Tokens'] = df['Abstract'].apply(lambda x: base.tokenizer(x))
    
    return df

def stemAndLemma(df):
    df['Tokens'] = df['Tokens'].apply(lambda x: base.tokensStemAndLemma(x))
    
    return df

def stopwordsRemover(df):
    df['Tokens'] = df['Tokens'].apply(lambda x: base.stopwordsRemover(x))
    
    return df

def extractVocab(df):
    vocab = [word for ab in df.Tokens for word in ab]
    vocab = list(set(vocab))
    
    return vocab

def extractDosuments(df):
    documents = [base.unTokenize(tokens) for tokens in df['Tokens']]
    
    return documents

def extractVectorMatrix(df):
    vocab = extractVocab(df)
    vectorizer = loader.loadVectorizer(vocab)
    matrix = vectorizer.fit_transform(extractDosuments(df)).todense()
    vectors = pd.DataFrame(matrix)
    vectors.columns = vocab
    df.reset_index(inplace=True)
    df.drop('index', axis=1, inplace=True)
    vectors.reset_index(inplace=True)
    vectors.drop('index', axis=1, inplace=True)
    df = pd.concat([df, vectors], axis=1)
    
    return df

# =============================================================================
# Process Non-Text Data
# =============================================================================
def nonPredictiveFeatureRemover(df):
    # Here I'm aggresively deleting features for the purpose of dimention reduction
    # Might consider adding some of the features back if they are predictive
    non_predictive_features = ['AwardNumber', 'Title', 'Program(s)', 'LastAmendmentDate',
                               'PrincipalInvestigator', 'Organization', 'ProgramManager',
                               'Co-PIName(s)', 'PIEmailAddress', 'OrganizationStreet',
                               'OrganizationCity', 'OrganizationState', 'OrganizationZip',
                               'OrganizationPhone', 'NSFDirectorate', 'ProgramElementCode(s)',
                               'ProgramReferenceCode(s)', 'ARRAAmount', 'Abstract', 'Tokens']
    df.drop(non_predictive_features, axis=1, inplace=True)
    
    return df

def processDateFeatures(df):
    df['StartDate'] = pd.to_datetime(df['StartDate'])
    df['EndDate'] = pd.to_datetime(df['EndDate'])
    df['YearStart'] = df['StartDate'].dt.year
    df['DaysElapsed'] = (df.EndDate - df.StartDate)/np.timedelta64(1, 'D')
    df.drop(['StartDate', 'EndDate'], axis=1, inplace=True)
    
    return df

def processCategoricalFeatures(df):
    categorical_features = ['NSFOrganization', 'State', 'AwardInstrument']
    for cat in categorical_features:
        df_ohe = pd.get_dummies(df[cat], drop_first=True)
        df = pd.concat([df, df_ohe], axis=1)
    df.drop(categorical_features, axis=1, inplace=True)
    
    return df
    
    

