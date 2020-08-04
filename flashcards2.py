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


def main():
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
    
    # Verb conjugation mode
    if re.search("v(erb)?", mode, re.IGNORECASE):
        # To-do: implement BeautifulSoup web scrape for verbs
        lang = input("Choose Language: ")
        if re.search("French", lang, re.IGNORECASE):
            fbank = [
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
                "appeler"
                ]
            subjects = ["je/j'", "tu", "il/elle", "nous", "vous", "ils/elles"]
            tenses = ["présent", "imparfait", "subjonctif", "plus-que-parfait",
                      "futur simple", "conditionnel présent", "futur antérieur"]
            cont = True
            i = 0
            while cont:
                r1 = random.randint(0,len(fbank)-1)
                r2 = random.randint(0,5)
                r3 = random.randint(0,len(tenses)-1)
                print("Conjugate " + fbank[r1] + ", subject " + subjects[r2] + " in the " + 
                               tenses[r3] + " tense: ")
                answer = input(subjects[r2] + " ")
                URL = "https://www.wordreference.com/conj/FrVerbs.aspx?v=" + fbank[r1]
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, 'html.parser')
                table = soup.find("table", id = "contenttable")
                table = table.find_all("div", class_ = "aa")
                # Calling findans function to get answer with extra text stuck on
                correct = findans("French", fbank[1], table, subjects[r2], tenses[r3])
                # Needs to look for answer at the very beginning of the text
                if re.search(("^" + re.escape(answer)), correct):
                    print("Correct!")
                # If our answer is not correct
                else:
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
                    stop_indices = stop_code[subjects[r2]]
                    stop_indices.append("que")
                    stop_indices.append("qu'")
                    # Goes through each possible element in stop indices
                    shortest = 500
                    for stop in stop_indices:
                       end_ex = re.search(re.escape(stop), correct)
                       if end_ex:
                           end = (re.search(re.escape(stop), correct)).span()
                           # Ensures we'll get the shortest index for the answer
                           if end[0] < shortest:
                               shortest = end[0]
                    # Printing out correct answer
                    correct = correct[0:shortest]
                    print("Wrong! The correct answer is: " + correct)
                i += 1
                if (i % 5) == 0 and i != 0:
                    again = input("Go again? (y/n): ")
                    if again.lower() == "n":
                        cont = False    

# Find the correct answer by parsing through HTML text        
def findans(language, verb, text, subject, tense):
    if language == "French":
        if tense in ["présent", "imparfait", "passé simple", "futur simple"]:
            category = "indicatif"
        elif tense in ["passé composé", "plus-que-parfait", "passé antérieur", "futur antérieur"]:
            category = "formes composées / compound tenses"
        elif tense in ["subjonctif", "subjonctif passé"]:
            category = "subjonctif"
        elif tense in ["conditionnel présent", "conditionnel passé"]:
            category = "conditionnel"
        # Iterate through html text into right table/tense
        for group in text:
            group = group.text # Converts html into string
            # If the tense category matches the group
            if re.search(re.escape(category), group, re.IGNORECASE):
                # Finds the indices for the tense
                tenseind = (re.search(tense, group)).span()
                anstext = group[tenseind[1]:] # remaining text after finding tense
                break
        # Determines regex subject pattern based on subject input
        sdic = {
            "je/j'" : "je", 
            "tu" : "tu",
            "il/elle" : "il, elle, on", 
            "nous" : "nous", 
            "vous" : "vous", 
            "ils/elles": "ils, elles"
            }
        if verb[0] in ["a", "e", "i", "o", "u"]:
            sdic["je/j"] = "j'"
        # spattern is the pattern that will be used for regex
        spattern = sdic[subject] 
        # ansind is the location of the matched subject- what comes next is the answer
        ansind = (re.search(re.escape(spattern), anstext)).span()        
        return anstext[ansind[1]:]
            # Do a regex match with answer at beginning of remaining text from index
main()    
