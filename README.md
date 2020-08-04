# language-practice-tools
Python programs for studying and practicing natural languages

This purpose of this project is to design software that can provide additional support to people studying natural languages, creating additional e-learning functionality beyond the limits of software such as Duolingo. I am using this project as an opportunity to improve my Python skills and make studying languages easier.

What can the code in this repository do right now?
1. Flashcards- 75% complete
  The user can input a CSV file containing a list of vocabulary in the target language with the translations in the native language. The program mixes the words up, and quizzes    the user, printing the correct answer if s/he gets it wrong. 
  Opportunities for improvement- I'm thinking of implementing a web scraper that can pick vocabulary words off Duolingo. Also, the answer validation seems buggy, and I'm not sure if it has to do with the CSV file I've been using or if Python doesn't like the extended characters. 

2. Verb Conjugator- 100% complete for French, need to add Spanish/English.
  The user can define a list of verbs and tenses, and the program will randomly select a subject, verb, and tense, asking the user to conjugate. The answer validation process uses BeautifulSoup to scrape wordreference.com to find the right answer. The HTML is a little unfriendly, so I had to use (what feels like) a fairly inefficient process for answer checking.
  
I am looking for other opportunities to create additional features that would be useful for passionate natural language learners!
