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
parser = English()


adr=AdrDetection()

a=input("Ktora metoda ma byc uzyta do danych testowych? Wybierz litere:\na-metoda podstawowa\nb-metoda human method\nc-metoda z wykorzystaniem WordNet\n\n")
if a=='a':
    adr.basicMethod()
if a=='b':
        adr.humanMethod()
if a=='c':
    adr.wordNetMethod()
adr.printAllData()


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

train = tweetsWithoutDrugs[:50]
with open("trainLabels.txt", "r") as ins:
    labelsTrain = []
    for line in ins:
        line=line.replace('\n','')
        labelsTrain.append(line)
print(labelsTrain)

test = tweetsWithoutDrugs[-400:]
labelsTestTemp = []
for i in range(len(tweetsWithoutDrugs)):
    labelsTestTemp.append('null')


for i in range(len(adr.finalData)):
    labelsTestTemp[adr.finalData[i][0]]=adr.adrList[adr.finalData[i][2][0]]

labelsTest=labelsTestTemp[-400:]


# trenowanie
pipe.fit(train, labelsTrain)

# test
preds = pipe.predict(test)

print("\n\n-----WYNIK-----\n\n")
for (sample, pred) in zip(test, preds):
    print(sample, ":", pred)
print("Dokladnosc: ", accuracy_score(labelsTest, preds)*100)


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
    
