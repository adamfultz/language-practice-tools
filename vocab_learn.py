# -*- coding: utf-8 -*-
"""
Flashcard/Vocab Reinforcement Tools- take 2
Created on Sat Sep 26 22:39:50 2020

@author: Adam
"""
import re
import csv
import random
import requests
import sys

from bs4 import BeautifulSoup
import nltk

'''
Vocab Test

User inputs the name of a csv file containing a list of French words and
evaluates user by checking for correct answer words in page text 
'''
def vocab_test(filename):
    vocab_list = []
    with open(filename, 'r', encoding = 'UTF-8') as csvfile:
        file = csv.reader(csvfile)
        for row in file:
            vocab_list.append(row)    
    # scramble so that the word order is different every time
    random.shuffle(vocab_list)
    #saving words guessed incorrectly
    missed = set()
    print("type 'exit' to stop program")    
    # looping through vocab and pulling up wordreference page using BS
    for word in vocab_list:
        word = word[0]
        url = "https://www.wordreference.com/fren/" + word.replace(" ", "%20")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
############### Option 1: NLTK/tokenize approach #################
        text = soup.get_text()
        tokens = nltk.word_tokenize(text)
        text = [word.lower() for word in tokens]
        search_text = text[text.index("principales"):]
        user = input("Define " + word + " : ")
        # Exit clause for easier testing
        if user == "exit":
            print("Missed words: (question word, user guess) ")
            for pair in missed:
                print(pair)
            sys.exit("user initiated program exit.")
        
        check = True
        for user_word in nltk.word_tokenize(user):
            if user_word not in search_text:
                check = False        
        if check == False:
            print("Wrong! Try again.")
            missed.add((word, user))
        else:
            print("Correct!")
            
    print("Missed words: (question word, user guess) ")
    for pair in missed:
        print(pair)       
            
vocab_test("vocab_test2.csv")