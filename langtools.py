# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 14:31:56 2020

@author: Adam
"""
# Flash card system
import re
import csv
import random
import requests
from bs4 import BeautifulSoup


def flashcard():
    mode = input("Mode? Choose flashcard, verb: ")
    if re.search("f(lashcards)?", mode, re.IGNORECASE):
        dic = {} # Initialized empty dictionary to store English/foreign word pairings
        filename = input("filename: ")
        with open(filename, 'r', encoding = 'UTF-8') as csvfile:
            fsource = csv.reader(csvfile)
            atype = input("Answer in English? (y/n): ")
            if re.search("y(es)?", atype, re.IGNORECASE):
                for row in fsource:
                    dic[row[0]] = row[1:] # stores all English words as possible answers
            if re.search("n(o)?", atype, re.IGNORECASE):
                for row in fsource:
                    ind = random.randint(1,len(row)-1) # chooses random English translation
                    dic[row[ind]] = row[0]
        # Start asking questions
        rvec = list(range(len(dic)))
        random.shuffle(rvec) # randomizes order of indices
        print("type 'exit' to end this session")
        for i in range(len(dic)):
            ind = rvec[i] # randomized index
            k = list(dic.keys())
            v = list(dic.values())
            answer = input("Translate the following: " + k[ind] + "\n")
            if answer.lower() in v[ind]:
                print("CORRECT!")
            elif re.search("exit", answer, re.IGNORECASE):
                break
            else:
                print("WRONG! The correct answer is " + " or ".join(v[ind]))
                
    
'''
Choose Language

User inputs language which generates list of subjects, verbs, and tenses
'''
def choose_lang(langin, option, tense = None):
    # FRENCH
    if re.search("French", langin, re.IGNORECASE):
        
        if option == "qset":
            vbank = [
                "aimer",
                "penser",
                "jouer",
                "chanter",
                "choisir",
                "vendre",
                "venir",
                "vouloir",
                "savoir",
                "aller",
                "faire",
                "avoir",
                "être",
                "dire",
                "pouvoir",
                "prendre",
                "mettre",
                "appeler"]
            subjects = ["je/j'", "tu", "il/elle", "nous", "vous", "ils/elles"]
            tenses = ["présent", "imparfait", "subjonctif", "plus-que-parfait",
                      "futur simple", "conditionnel\nprésent", "futur antérieur"]
            URLstem = "https://www.wordreference.com/conj/FrVerbs.aspx?v="
            lang = "French"
            return (vbank, subjects, tenses, URLstem, lang)
        
        if option == "find":
            if tense in ["présent", "imparfait", "passé simple", "futur simple"]:
                category = "indicatif"
            elif tense in ["passé composé", "plus-que-parfait", "passé antérieur", "futur antérieur"]:
                category = "formes composées / compound tenses"
            elif tense in ["subjonctif", "subjonctif passé"]:
                category = "subjonctif"
            elif tense in ["conditionnel\nprésent", "conditionnel passé"]:
                category = "conditionnel"
            # Determines regex subject pattern based on subject input
            sdic = {
                "je/j'" : "je", 
                "tu" : "tu",
                "il/elle" : "il, elle, on", 
                "nous" : "nous", 
                "vous" : "vous", 
                "ils/elles": "ils, elles"
                }
            return (category, sdic)
        
        if option == "stop":
            stop_code = {
                "je/j'" : ["tu"],
                "tu" : ["il, elle, on"],
                "il/elle" : ["nous"],
                "nous" : ["vous"],
                "vous" : ["ils, elles"],
                "ils/elles" : ["imparfait", "passé simple", "futur simple",
                               "plus-que-parfait", "passé antérieur", "futur antérieur",
                               "passé"]
                }
            return stop_code
    
    # SPANISH
    if re.search("Spanish", langin, re.IGNORECASE):
        
        if option == "qset":
            vbank = [
                "comer"]
            subjects = ["yo", "tú", "él/ella/Ud.", "nosotros", "ellos/ellas/Uds."]
            tenses = ["presente"]
            URLstem = "https://www.wordreference.com/conj/EsVerbs.aspx?v="
            lang = "Spanish"
            return (vbank, subjects, tenses, URLstem, lang)

        if option == "find":
            if tense in ["presente", "imperfecto", "pretérito", "futuro", "condicional"]:
                category = "Indicativo"
            if tense in ["pretérito perfecto", "pluscuamperfecto", 
                         "futuro perfecto", "condicional perfecto"]:
                category = "Formas compuestas comunes"
            if tense in ["subjuntivo"]:
                category = "Subjuntivo"
            # Determines regex subject pattern based on subject input
            sdic = {
                "yo" : "yo", 
                "tú" : "tú",
                "él/ella/Ud." : "él, ella, Ud.", 
                "nosotros" : "nosotros", 
                "ellos/ellas/Uds.": "ellos, ellas, Uds."
                }
            return (category, sdic)    

        if option == "stop":
            stop_code = {
                "yo" : ["tú"],
                "tú" : ["él, ella, Ud."],
                "él/ella/Ud." : ["nosotros"],
                "nosotros" : ["vosotros"],
                "ellos/ellas/Uds." : ["vos"]
                }
            return stop_code


'''
Conjugate

Draws from list of subjects, verbs, and tenses at random to quiz user.
Asks 5 questions each time. 
'''
def conjugate():    
    langin = input("Choose Language: ")    
    vbank, subjects, tenses, URLstem, lang = choose_lang(langin, "qset")
    
    # Choosing subject,verb,tense combination
    cont = True
    i = 0
    while cont:
        r1 = random.randint(0,len(vbank)-1)
        r2 = random.randint(0,len(subjects)-1)
        r3 = random.randint(0,len(tenses)-1)
        print("Conjugate " + vbank[r1] + ", subject " + subjects[r2] + " in the " + 
                       tenses[r3] + " tense: ")
        
        # Collecting user answer
        answer = input(subjects[r2] + " ")
        URL =  URLstem + vbank[r1]
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find("table", id = "contenttable")
        table = table.find_all("div", class_ = "aa")
        
        # Calling findans function to get answer with extra text stuck on
        anstext = findans(lang, vbank[r1], table, subjects[r2], tenses[r3])
        # Checking user answer against parsed text
        checkans(lang, answer, anstext, subjects[r2])
        
        # Prompts for user to continue
        i += 1
        if (i % 5) == 0 and i != 0:
            again = input("Go again? (y/n): ")
            if again.lower() == "n":
                cont = False    

'''
Find Answer

Parses HTML text to locate correct answer.
'''
        
def findans(lang, verb, text, subject, tense):
    category, sdic = choose_lang(lang, "find", tense)
    
        # Iterate through html text into right table/tense
    for group in text:
        group = group.text # Converts html into string
        # If the tense category matches the group
        if re.search(re.escape(category), group, re.IGNORECASE):
            # Finds the indices for the tense
            tenseind = (re.search(tense, group)).span()
            anstext = group[tenseind[1]:] # remaining text after finding tense
            break
        
    # Handling special French case with a verb starting with a vowel or aux. verb
    if lang == "French":    
        if verb[0] in ["a", "e", "i", "o", "u"] or category == "formes composées / compound tenses":
            sdic["je/j'"] = "j'"
        elif category == "subjonctif" or category == "conditionnel":
            sdic["je/j'"] = "je/j'"
    # spattern is the pattern that will be used for regex
    spattern = sdic[subject] 
    # ansind is the location of the matched subject- what comes next is the answer
    ansind = (re.search(re.escape(spattern), anstext)).span()        
    return anstext[ansind[1]:]
        # Do a regex match with answer at beginning of remaining text from index
   
'''
Check Answer

Identifies correct answer from text and compares to user answer.
'''
def checkans(lang, answer, anstext, subject):
    stop_code = choose_lang(lang, "stop")
    stop_indices = stop_code[subject]
    # Handles special case with subjunctive verbs
    if lang == "French":
        stop_indices.append("que")
        stop_indices.append("qu'")
    # Goes through each possible element in stop indices to find where answer ends
    shortest = 500
    for stop in stop_indices:
       end_ex = re.search(re.escape(stop), anstext)
       if end_ex:
           end = (re.search(re.escape(stop), anstext)).span()
           # Ensures the shortest index for the answer
           if end[0] < shortest:
               shortest = end[0]
    # CORRECT ANSWER
    correct = anstext[0:shortest]
        
    if answer == correct:
        print("Correct!")
    else:
        print("Wrong! The correct answer is: " + correct)
        