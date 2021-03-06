# -*- coding: utf-8 -*-
"""EmailFiltering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_1RZT5bxgLDiZfQshcR0PmkTzzzHg0NP
"""

import nltk
nltk.download('wordnet')
nltk.download('punkt')
import re
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import string
import matplotlib.pyplot as plt
from gensim.parsing.preprocessing import strip_non_alphanum, strip_multiple_whitespaces, preprocess_string,split_alphanum, strip_numeric, strip_short

"""Input dataset from Google Drive"""

dataset = pd.read_csv('dataset_2.csv',encoding='latin-1', usecols =['type','email'])

print(dataset.head())

print(dataset.shape)

print(dataset.info())

#check for duplicates and removing them
dataset.drop_duplicates(inplace = True)

#Show the new shape (number of rows & colums)
print(dataset.shape)

"""Therefore, there are approximately 400 duplicate samples

In 'type' column, set 'spam' to 1, 'ham' to 0
"""

dataset.loc[dataset['type'] == 'spam', 'type'] = 1  
dataset.loc[dataset['type'] == 'ham', 'type'] = 0

print(dataset.head())

"""data preprocessing """

def raw_text_preprocessing(Message):
    Message = strip_non_alphanum(Message).strip()  # remove non alphanum and blank space
    Message = Message.lower()  # set lowercase
    Message = split_alphanum(Message)  
    Message = strip_short(Message, minsize=2)  
    Message = strip_numeric(Message)  # remove number
    Message = word_tokenize(Message) # tokenize
    return Message

dataset['email'] = dataset['email'].apply(str).apply(raw_text_preprocessing)

print(dataset.head())

"""lemmatization"""

wnl = nltk.WordNetLemmatizer()
dataset['email']= [[wnl.lemmatize(word) for word in s]
              for s in dataset['email']]

print(dataset['email'].head())

"""vectorize and apply stop words"""

cv = CountVectorizer(stop_words='english')
X = cv.fit_transform(dataset['email'].astype('str'))

y = dataset['type'].values.astype('int')

"""split dataset"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size =0.25, random_state =0)

"""Training with MultinomialNB"""

model_1 = MultinomialNB()
model_1.fit(X_train, y_train)

"""Training with GaussianNB()"""

model_2 = GaussianNB()
model_2.fit(X_train.toarray(), y_train)

"""Training with BernoulliNB"""

model_3 = BernoulliNB()
model_3.fit(X_train.toarray(), y_train)

y_predict1 = model_1.predict(X_test)
y_predict2 = model_2.predict(X_test.toarray())
y_predict3 = model_3.predict(X_test.toarray())

print('y_test: ' ,y_test)

print('MultinomialNB y_predict: ' ,y_predict1)
print('GaussianNB y_predict: ' ,y_predict2)
print('BernoulliNB y_predict: ' ,y_predict3)

#Evaluation
print('Evaluation')

accuracy1 = accuracy_score(y_test, y_predict1)
accuracy2 = accuracy_score(y_test, y_predict2)
accuracy3 = accuracy_score(y_test, y_predict3)
print('MultinomialNB accuracy: ', accuracy1)
print('GaussianNB accuracy: ', accuracy2)
print('BernoulliNB accuracy: ', accuracy3)

precision1 = precision_score(y_test, y_predict1, pos_label=0)
precision2 = precision_score(y_test, y_predict2, pos_label=0)
precision3 = precision_score(y_test, y_predict3, pos_label=0)
print('MultinomialNB precision: ', precision1)
print('GaussianNB precision: ', precision2)
print('BernoulliNB precision: ', precision3)

recall1 = recall_score(y_test, y_predict1, pos_label=0)
recall2 = recall_score(y_test, y_predict2, pos_label=0)
recall3 = recall_score(y_test, y_predict3, pos_label=0)
print('MultinomialNB recall: ', recall1)
print('GaussianNB recall: ', recall2)
print('BernoulliNB recall: ', recall3)

f1_1 = f1_score(y_test, y_predict1, pos_label=0)
f1_2 = f1_score(y_test, y_predict2, pos_label=0)
f1_3 = f1_score(y_test, y_predict3, pos_label=0)
print('MultinomialNB f1 score: ', f1_1)
print('GaussianNB f1 score: ', f1_2)
print('BernoulliNB f1 score: ',f1_3)

matrix1 = confusion_matrix(y_test, y_predict1)
matrix2 = confusion_matrix(y_test, y_predict2)
matrix3 = confusion_matrix(y_test, y_predict3)

print('MultinomialNB:')
print(matrix1)
print('GaussianNB:')
print(matrix2)
print('BernoulliNB:')
print(matrix3)