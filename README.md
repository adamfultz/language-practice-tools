# language-practice-tools
Python programs for studying and practicing natural languages

This purpose of this project is to design software that can provide additional support to people studying natural languages, creating additional e-learning functionality beyond the limits of software such as Duolingo. I am using this project as an opportunity to improve my Python skills and make studying languages easier.

What can the code in this repository do right now?
1. Verb Conjugator- 100% complete for French and Spanish. English coming. 
The user can define a list of verbs and tenses, and the program will randomly select a subject, verb, and tense, asking the user to conjugate. The answer validation process uses BeautifulSoup to scrape wordreference.com to find the right answer.
  
2. Vocabulary Reinforcement
The user inputs a csv file containing a list of French vocabulary words and is prompted to give their English definitions. The answers are checked against text from the corresponding page on wordreference.com.
  
I am looking for other opportunities to create additional features that would be useful for passionate natural language learners!

# Edit 2 Sept. 2020
Spanish conjugation functionality added, bugs relating to answer checking/handling vowel exceptions in French fixed. 

# Edit 29 Sept. 2020
Fixed a couple of bugs in the conjugation function, and added a new file (vocab_learn.py) containing a vocabularly reinforcement tool. I wanted to move away from the inflexibility of keeping both the questions and answers, so I made a first pass at implementing answer checking using BeautifulSoup to parse wordreference.com (again). It's not a foolproof method because the text from wordreference is tokenized and user answer is compared against each of the tokens, meaning that you could answer something completely wrong, but if the words were in the html, you would be marked correct. 
