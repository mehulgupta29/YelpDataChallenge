
"""
A simple script that demonstrates how we classify textual data with sklearn.

"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import re
from nltk.corpus import stopwords
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier


stopLex=[]
#read the reviews and their polarities from a given file
def loadData(fname):
    reviews=[]
    labels=[]
    stopLex=stopwords.words('english')
    f=open(fname)
    for line in f:
        review,rating=line.strip().split('\t')
        review = re.sub('<[a-zA-Z]+>', '', review)
        review = re.sub('n\'t', ' not', review)
        review = re.sub('\.+', ' ', review)
        review = re.sub('[^a-zA-Z\d\.]', ' ', review)
        review = re.sub(' +', ' ', review)
        reviews.append(review.lower())
        labels.append(int(rating))
    f.close()
    return reviews,labels

#read the reviews and their polarities from a given file
def loadDataTestFile(fname):
    reviews=[]
    labels=[]
    stopLex=stopwords.words('english')
    f=open(fname)
    for line in f:
        review=line.strip()
        review = re.sub('<[a-zA-Z]+>', '', review)
        review = re.sub('n\'t', ' not', review)
        review = re.sub('\.+', ' ', review)
        review = re.sub('[^a-zA-Z\d\.]', ' ', review)
        review = re.sub(' +', ' ', review)
        reviews.append(review.lower())
    f.close()
    return reviews

#output function
def out(fname, results):
        fout = open(fname, 'w')
        for result in results:
                #print(result)
                fout.write(str(result))
                fout.write("\n")
        fout.close()


rev_train,labels_train=loadData('reviews_train.txt')
rev_test=loadDataTestFile('reviews_test.txt')
rev_test, labels_test=loadData('reviews_test.txt')


#Build a counter based on the training dataset
counter = CountVectorizer(ngram_range=(1,2), max_df=0.41, min_df=0, strip_accents='unicode', stop_words=stopLex)
counter.fit(rev_train)

#count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(rev_train)#transform the training data
counts_test = counter.transform(rev_test)#transform the testing data


param_grid = {'C': [0.01, 0.1, 1], 'tol':[0.0001, 0.00001, 0.001 ], 'max_iter': [10, 100, 1000] }

clf = GridSearchCV(LogisticRegression(penalty='l2'), param_grid, cv=5)

clf.fit(counts_train, labels_train)
print clf.best_params_
LR=LogisticRegression(C=clf.best_params_['C'], tol=clf.best_params_['tol'], max_iter=clf.best_params_['max_iter'], class_weight='balanced', solver ='lbfgs', multi_class='multinomial')

LR.fit(counts_train,labels_train)

pred=LR.predict(counts_test)
print accuracy_score(pred,labels_test)
#write to output file
out('out.txt', pred)

#print accuracy
#print(accuracy_score(pred,labels_test))
