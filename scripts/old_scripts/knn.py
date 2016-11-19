import os
import sys
from operator import itemgetter
import nltk

#read the reviews and their polarities from a given file
def loadData(fname):
        reviews=[]
        labels=[]
        f=open(fname)
        for line in f:
                review,rating=line.strip().split('\t')
                reviews.append(review.lower())
                labels.append(int(rating))
        f.close()
        return reviews,labels

#function to load lexicons
def loadLexicon(fname):
        newLex=set()
        lex_conn=open(fname)
        #add every word in the file to the set
        for line in lex_conn:
                newLex.add(line.strip())# remember to strip to remove the lin-change character
        lex_conn.close()
        return newLex

def getCoordinate(review):
        xcord=0
        ycord=0
        review_class=0
        words=review.lower().strip().split(' ')
        for word in words:
                if word in posLex:
                        ycord+=1
                elif word in negLex:
                        xcord+=1
        if ycord > xcord:
                review_class=1
        return (xcord, ycord, review_class)

def calculateDistance(p1, p2):
        x2=p2[0]
        x1=p1[0]
        y2=p2[1]
        y1=p1[1]
        return (((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1))) ** 0.5

def getNeighbourDistance(test_coordinate, train_coordinates):
        result={}
        for train_cord in train_coordinates:
                #print(test_coordinate, train_cord)
                distance=calculateDistance(test_coordinate, train_cord)
                result[train_cord]=distance
        return result

def findNeighbours(neighbourDict, k):
        freq=neighbourDict
        sortedByValue=sorted(freq.items(),key=itemgetter(1))
        return sortedByValue[:k]

def voteLabels(topKNeighbours):
        vote={}
        for kn in topKNeighbours:
                #print(kn[0][2])
                rev_class = kn[0][2]
                vote[rev_class]=vote.get(rev_class, 0)+1
        #print(vote)
        sorting=sorted(vote.items(), key=itemgetter(1), reverse=True)
        return sorting[:1]

def getAccuracy(testList, predictions):
        correct = 0
        for x in range(len(testList)):
                if testList[x] is predictions[x]:
                        correct += 1
        return (correct/float(len(testList))) * 100.0

#load data
rev_train,labels_train=loadData('reviews_train.txt')
rev_test,labels_test=loadData('reviews_test.txt')

rev_test2,labels_test2=loadData('test.txt')
rev_train2,labels_train2=loadData('train.txt')
#print(rev_train2,labels_train2)

#get pos and neg lexicon
posLex=loadLexicon('positive-words.txt')
negLex=loadLexicon('negative-words.txt')

#find coordinates of rev_train
train_coordinates=[]
for review_train in rev_train:
        coordinates=getCoordinate(review_train)
        train_coordinates.append(coordinates)

predictions=[]
for r_test in rev_test:
        #print(r_test)
        r_test_cord=getCoordinate(r_test)
        neighbourDict=getNeighbourDistance(r_test_cord, train_coordinates)
        topKNeighbours=findNeighbours(neighbourDict, 5)
        answer=voteLabels(topKNeighbours)
        predictions.append(answer[0][0])

#print(predictions)
acc=getAccuracy(labels_test, predictions)
print(acc)
#print(rev_train, labels_train)
#print(posLex)