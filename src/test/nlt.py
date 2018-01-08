from nltk.tokenize import word_tokenize 
from nltk.corpus import wordnet
synonyms = []
for syn in wordnet.synsets('cold'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
print(synonyms)
mytext = "My doctor recommended me vitapap . Till now the only drug reaction I have is that I have to vomit . Maybe I'm a little bit anxious too." 
print(word_tokenize(mytext))