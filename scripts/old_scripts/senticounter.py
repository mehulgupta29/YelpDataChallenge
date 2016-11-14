"""
Reads a list of reviews and decide if each review is positive or negative,
based on the occurences of positive and negative words.
"""

import sys

#function that loads a lexicon of positive words to a set and returns the set
def loadLexicon(fname):
	newLex=set()
	lex_conn=open(fname)
	#add every word in the file to the set
	for line in lex_conn:
		newLex.add(line.strip())# remember to strip to remove the lin-change character
	lex_conn.close()

	return newLex

#function that reads in a file with reviews and decides if each review is positive or negative
#The function returns a list of the input reviews and a list of the respective decisions
def run(path):

	pfreq={}

	#load the positive and negative lexicons
	posLex=loadLexicon('positive-words.txt')
	negLex=loadLexicon('negative-words.txt')

	fin=open(path)
	for line in fin: # for every line in the file (1 review per line)
		line=line.lower().strip()   
		words=line.split(' ') # slit on the space to get list of words
		myPos=set()#unique pos words for this review
		for word in words: #for every word in the review
			if word in posLex: # if the word is in the positive lexicon
				myPos.add(word)
		
		#update the global counts of the pos and neg words of this review	
		for word in myPos:
			pfreq[word]=pfreq.get(word,0)+1

	fin.close()
	return pfreq