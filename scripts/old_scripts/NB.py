"""
A simple script that demonstrates how we classify textual data with sklearn.

"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import re
from nltk.corpus import stopwords


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

rev_train,labels_train=loadData('reviews_train.txt')
rev_test,labels_test=loadData('reviews_test.txt')

#Build a counter based on the training dataset
counter = CountVectorizer(ngram_range=(1,2), max_df=0.41, min_df=0, strip_accents='unicode')
counter.fit(rev_train)

#count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(rev_train)#transform the training data
counts_test = counter.transform(rev_test)#transform the testing data

#train classifier
#clf = MultinomialNB()
clf = LogisticRegression(solver="lbfgs", max_iter= 10000000, multi_class='multinomial', tol=0.00000001, class_weight='balanced')

#train all classifier on the same datasets
clf.fit(counts_train,labels_train)

#use hard voting to predict (majority voting)
pred=clf.predict(counts_test)

#print accuracy
print(accuracy_score(pred,labels_test))