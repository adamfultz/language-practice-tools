# -*- coding: utf-8 -*-
"""

Created on Fri Oct 23 15:42:43 2020

@author: Adam
"""
import sys
import random
import pandas as pd
import nltk
from nltk.corpus import wordnet

'''
exam- prompts user to translate vocab word/phrase and checks against
answers listed in row as well as synonyms on wordnet
'''
def exam(prompt, pos, row):
    user = input(f'Traduisez {prompt} ({pos}) en anglais: ')
    tset1 = nltk.word_tokenize(row['English1'])
    if type(row['English2']) == str:
        tset2 = nltk.word_tokenize(row['English2'])
    else:
        tset2 = []
    # Building the set of words to consider
    tset = [word for word in (tset2+tset1) if word.isalpha()]
    remove = ['to', 'and', 'the', 'it', 'of', 'from', 'in']
    tset = [word for word in tset if word not in remove]
    allowed = []
    for word in tset:
        syns = wordnet.synsets(word)
        synlist = [syns[n].lemmas()[0].name() for n in range(len(syns))]
        allowed += (synlist)
        allowed.append(word)
    # Tokenizing and processing user answer
    wset = nltk.word_tokenize(user)
    wset = [word for word in wset if word.isalpha()]
    for word in [w for w in wset if w not in remove]:
        if word in allowed:
            print('Correct!')
            return True
        elif type(row['English2']) != str:
            ans1 = row['English1']
            print(f'Wrong! The correct answer is {ans1}')
            return False
        elif type(row['English2']) == str:
            ans1 = row['English1']
            ans2 = row['English2']
            print(f'Wrong! The correct answers are: {ans1} and {ans2}')
            return False


filename = 'oct2020_vocab.csv'
df = pd.read_csv(filename)

# random order of rows that will be used to move through vocab DataFrame
seq = list(range(df.shape[0]))
random.shuffle(seq)

# counter for number of questions
i = 0
# tracks where in seq we are, determining which word will be asked
n = 0
repeat = []
learned = []
while True:
    # logic for choosing ind based on repeating missed words
    choice = random.choices(['new', 'repeat'], weights = [70, 30])
    if choice == ['new'] or (not repeat):
        ind = seq[n]
        n += 1
    elif choice == ['repeat']:
        ind = random.choice(repeat)
    
    row = df.iloc[ind]
    prompt = row['French']
    pos = row['POS']
    
    ex = exam(prompt, pos, row)
    # tracks if missed words are answered correctly later
    if ex and ind in repeat:
        learned.append(ind)
        # if word answered correctly five times, won't repeat it again
        if learned.count(ind) == 5:
            repeat.remove(ind)
    # adds question to queue for re-asking missed words later
    elif not ex:
        repeat.append(ind)
    # repeats previous question until you get it right
    while not ex:
        ex = exam(prompt, pos, row)
        
    # Prompts for user to continue after 5 questions
    i += 1
    if (i % 5) == 0 and i != 0:
        again = input("Go again? (y/n): ")
        if again.lower() == "n":
            sys.exit()
                              