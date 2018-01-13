from nltk.tokenize import word_tokenize 
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from AdrDetection import AdrDetection
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
import string
import re
from spacy.lang.en import English
import spacy
from cProfile import label
from random import randint
import plotly.plotly as py
import plotly.graph_objs as go

parser = English()


adr=AdrDetection()

a=input("Ktora metoda ma byc uzyta do danych testowych? Wybierz litere:\na-metoda podstawowa\nb-metoda human method\nc-metoda z wykorzystaniem WordNet\n\n")
if a=='a':
    adr.basicMethod()
if a=='b':
        adr.humanMethod()
if a=='c':
    adr.wordNetMethod()
#adr.printAllData()

tweetsWithoutDrugs=[] #lista tweetow, ale z wycietymi nazwami lekow
for i in range(len(adr.tweets)):
    tweetsWithoutDrugs.append('')

for i in range(len(adr.tweets)):
    for j in range(len(adr.drugs)):
        for k in range(len(adr.drugs[j])):
            if adr.drugs[j][k] in adr.tweets[i]:
                tweetsWithoutDrugs[i]=adr.tweets[i].replace(adr.drugs[j][k],'') 



# deklaracja smieci
STOPLIST = set(stopwords.words('english') + ["n't", "'s", "'m", "ca"] + list(ENGLISH_STOP_WORDS))
SYMBOLS = " ".join(string.punctuation).split(" ") + ["-----", "---", "...", "“", "”", "'ve"]



#struktura do oczyszczania tekstu
class CleanTextTransformer(TransformerMixin):
    """
    Convert text to cleaned text
    """

    def transform(self, X, **transform_params):
        return [cleanText(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}
    
#czyszczenie
def cleanText(text):
    text = text.strip().replace("\n", " ").replace("\r", " ")
    text = text.replace("&amp;", "and").replace("&gt;", ">").replace("&lt;", "<")
    text = text.lower()
    return text


# tokenizacja i lematyzacja
def tokenizeText(sample):

    tokens = parser(sample)

    lemmas = []
    for tok in tokens:
        lemmas.append(tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_)
    tokens = lemmas
    tokens = [tok for tok in tokens if tok not in STOPLIST]
    tokens = [tok for tok in tokens if tok not in SYMBOLS]

    while "" in tokens:
        tokens.remove("")
    while " " in tokens:
        tokens.remove(" ")
    while "\n" in tokens:
        tokens.remove("\n")
    while "\n\n" in tokens:
        tokens.remove("\n\n")

    return tokens



# Tworzenie wektora
vectorizer = CountVectorizer(tokenizer=tokenizeText, ngram_range=(1,1))
clf = LinearSVC()
# Tworzenie pipeline'a
pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', vectorizer), ('clf', clf)])



#        DANE
trainNumber=20
testNumber=78


labelsTestTemp = []
for i in range(len(tweetsWithoutDrugs)):
    labelsTestTemp.append('null')


for i in range(len(adr.finalData)):
    labelsTestTemp[adr.finalData[i][0]]=adr.adrList[adr.finalData[i][2][0]]


'''
train = tweetsWithoutDrugs[:trainNumber]
test = tweetsWithoutDrugs[-testNumber:]
labelsTrain=labelsTestTemp[:trainNumber]
labelsTest=labelsTestTemp[-testNumber:]
'''

# DANE LOSOWE

## LOSOWANIE DLA DANYCH TRENUJACYCH
trainInts=[]
for i in range(trainNumber):
    a=randint(0,len(tweetsWithoutDrugs)-1)
    if a not in trainInts:
        trainInts.append(a)
    else:
        while a in trainInts:
            a=randint(0,len(tweetsWithoutDrugs)-1)
        trainInts.append(a)
train=[]            
labelsTrain=[]
for i in range(trainNumber):
    train.append(tweetsWithoutDrugs[trainInts[i]])
    labelsTrain.append(labelsTestTemp[trainInts[i]])

## LOSOWANIE DLA DANYCH TESTOWYCH, MUSZA BYC INNE NIZ DO TRENOWANIA

testInts=[]
for i in range(testNumber):
    a=randint(0,len(tweetsWithoutDrugs)-1)
    if a not in trainInts and a not in testInts:
        testInts.append(a)
    else:
        while a in trainInts or a in testInts:
            a=randint(0,len(tweetsWithoutDrugs)-1)
        testInts.append(a)
test=[]            
labelsTest=[]
for i in range(testNumber):
    test.append(tweetsWithoutDrugs[testInts[i]])
    labelsTest.append(labelsTestTemp[testInts[i]])

# trenowanie
pipe.fit(train, labelsTrain)

# test
preds = pipe.predict(test)


 
 
### POCZATEK ALGORYTMYU MASZYNOWEGO

def fillTableMachine():
        cellsh=dict(values=[createFirstColumnInTableMachine(),
                           adr.createAdrColumnInTable(),
                           adr.createDeclaredColumnInTable(),
                           adr.createReadColumnInTable()])
        trace = go.Table(
        header=dict(values=['Lek', 'Skutki uboczne','deklarowane','odczytane']),
        cells=cellsh)
     
        data = [trace] 
        py.plot(data, filename = 'result_presentation_table')

def createFirstColumnInTableMachine():
        column=[]
        for i in range(0,len(adr.adrsWithoutPercentUpgraded)):
            for j in range(0,len(adr.adrsWithoutPercentUpgraded[i])):
                if j==0:
                    column.append(adr.drugs[i][0])
                else:
                    column.append('')
            #column.append('')
        return column

def calculatePercentageOfAdrMachine():
        for i in range(0,len(adr.drugs)):
            adr.sumsOfDrugs.append(0)
        for i in range(0,len(adr.adrsWithoutPercentUpgraded)):
            temp=[]
            for j in range(0,len(adr.adrsWithoutPercentUpgraded[i])):
                temp.append(0)
            adr.sumsOfAdrs.append(temp)
        for i in range(0,len(adr.drugs)):
                for j in range(0,len(adr.pairsTweetDrug)):
                        if adr.pairsTweetDrug[j][1]==i:
                            adr.sumsOfDrugs[i]=adr.sumsOfDrugs[i]+1
        for i in range(0,len(adr.finalData)):
                for k in range(0, len(adr.adrsWithoutPercentUpgraded)):
                    if adr.isOneAdrFromDrug(adr.finalData[i][2],k) and adr.finalData[i][1]==k:
                        adr.sumsOfAdrs[k][adr.whichAdrFromDrug(adr.finalData[i][2],k)]=adr.sumsOfAdrs[k][adr.whichAdrFromDrug(adr.finalData[i][2],k)]+1
        #print(self.sumsOfDrugs)
        #print(self.sumsOfAdrs)

def upgradeAdrWithNewAdrsMachine():
    adr.separatePercentFromAdr()
    for i in range(0,len(adr.adrswithoutpercent)):
        temp=[]
        for j in range (0,len(adr.adrswithoutpercent[i])):
            temp.append(adr.adrswithoutpercent[i][j])
        adr.adrsWithoutPercentUpgraded.append(temp)
            
    adr.finalData.sort(key=lambda x: x[0])
    for i in range(0, len(adr.finalData)):
        if adr.adrList[adr.finalData[i][2]] not in adr.adrswithoutpercent[adr.finalData[i][1]] and adr.adrList[adr.finalData[i][2]] not in adr.adrsWithoutPercentUpgraded[adr.finalData[i][1]]:
            adr.adrsWithoutPercentUpgraded[adr.finalData[i][1]].append(adr.adrList[adr.finalData[i][2]])
            adr.percents[adr.finalData[i][1]].append('X')

def getAdrNo(s):
    for i in range(len(adr.adrList)):
        if adr.adrList[i] == s:
            return i
        
def getDrugNo(s):
    for i in range(len(adr.drugs)):
        if adr.pairsTweetDrug[i][0]==s:
            return adr.pairsTweetDrug[i][1]
def getTweetDrugIndex(s):
    for i in range(len(adr.pairsTweetDrug)):
        if adr.pairsTweetDrug[i][0]==s:
            return i
    return -1
        
adr.adrsWithoutPercentUpgraded=[]
adr.adrswithoutpercent=[]
adr.percents=[]
adr.sumsOfAdrs=[]
adr.finalData=[]
triple=[]

#testInts.sort(key=None, reverse=False)
        
for i in range(testNumber):
    if preds[i]!='null' :    
        triple=[]
        triple=[testInts[i],adr.pairsTweetDrug[getTweetDrugIndex(testInts[i])][1],getAdrNo(preds[i])]
        adr.finalData.append(triple)


    
upgradeAdrWithNewAdrsMachine()
calculatePercentageOfAdrMachine()
#adr.printAllData()
fillTableMachine()
### KONIEC

print("\n\n-----WYNIK-----\n\n")
for (sample, pred) in zip(test, preds):
    print(sample, ":", pred)
print("\n\n----DOKLADNOSC----: ", accuracy_score(labelsTest, preds)*100," %\n\n")


print("Dane po tokenizacji i lematyzacji:")
pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', vectorizer)])
transform = pipe.fit_transform(train, labelsTrain)

vocab = vectorizer.get_feature_names()

for i in range(len(train)):
    s = ""
    indexIntoVocab = transform.indices[transform.indptr[i]:transform.indptr[i+1]]
    numOccurences = transform.data[transform.indptr[i]:transform.indptr[i+1]]
    for idx, num in zip(indexIntoVocab, numOccurences):
        s += str((vocab[idx], num))
    print("Probka {}: {}".format(i, s))
    
