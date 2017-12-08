'''
Created on 4 gru 2017

@author: Witek
'''

class Dictionary:
    
    ######   ZMIENNE
    
    adrs=[] #tablica tablic z odpowiadaj¹cymi numerem glownym lekom z drugs, elementem tablicy jest tablica z roznymi skutkami ubocznymi'''
            #(pierwsza jest liczba procent u ilu wystepuje'''
    
    
    drugs=[] #'''tablica tablic z lekami (kilka nazw w jednym elemencie tablicy)'''
    
    
    tweets=[] #'''tablica z wypowiedziami ludzi, jedna wypowiedz to jeden element'''
    
    
    pairsTweetDrug=[] #'''para oznaczajaca w jakim tweecie znaleziono lek i - numer tweetu, j - jaki lek znaleziono'''
    
    
    adrList=[] #'''lista wszystkich skutkow ubocznych zawartych w danych '''
    
    
    finalData=[]

 
 
    ######    FUNKCJE
    
    def getDrugTemp(self,fileName):
        lines=[]
        drugtemp=[]
        
        f=open(fileName,'r')
        for line in f:
            line=line.lower()
            lines.append(line)
            split=line.split(",")
            adrhelp=split[0].split("-")
            drugtemp.append(adrhelp)
            '''drugtemp ostatni element zerowy'''
        return drugtemp
        
    def getAdrTemp(self,fileName):
        lines=[]
        adrtemp=[]

        f=open(fileName,'r')
        for line in f:
            line=line.lower()
            lines.append(line)
            split=line.split(",")
            adrhelp=[]
            for i in range(1,len(split)-1):
                adrhelp.append(split[i])
            adrtemp.append(adrhelp)
            '''adrtemp ostatni element zerowy'''
        return adrtemp
        
    def readDrugsAndAdrsToArrays(self):
        fileName=input("Podaj nazwe pliku z lekami i skutkami ubocznymi do wczytania: ")
        self.drugs=self.getDrugTemp("data.txt") #dac zmienna fileName!!!
        self.adrs=self.getAdrTemp("data.txt")   #dac zmienna fileName!!!
        print(self.drugs)
        #print(self.adrs)

    def createListOfAdrs(self):
        spl=[[] for i in range(len(self.adrs))]
        splfull=[]
        for i in range(0,len(self.adrs)):
            for j in range(0,len(self.adrs[i])):
                help=self.adrs[i][j].split('-')
                spl[i].append(help)
            splfull.append(spl[i])
        #print(splfull)
        for i in range(0,len(splfull)):
            for j in range(0,len(splfull[i])):
                for k in range(0,len(splfull[i][j])):
                    if not self.adrList and not splfull[i][j][k].isdigit():
                        self.adrList.append(splfull[i][j][k])
                    if splfull[i][j][k] not in self.adrList and not splfull[i][j][k].isdigit():
                        self.adrList.append(splfull[i][j][k])
                        
        print(self.adrList)
        
    def readTweetsToArray(self):
        fileName=input("Podaj nazwe pliku z danymi wolnych wypowiedzi pacjentow: ")
        with open('tweets.txt', 'r') as myfile:
            data=myfile.read().replace('\n', '')
            data=data.lower()
        self.tweets=data.split(';;;;;;')
        #print(self.tweets)
        
    def findPairTweetDrug(self):
        for i in range(0,len(self.tweets)):
            for j in range(0,len(self.drugs)-1):
                for k in range(0,len(self.drugs[j])):   
                    if self.drugs[j][k] in self.tweets[i]: 
                        pair=[i,j] 
                        '''para oznaczajaca w jakim tweecie znaleziono lek i - numer tweetu, j - jaki lek znaleziono'''
                        self.pairsTweetDrug.append(pair)
        print(self.pairsTweetDrug)
    
    def basicMethod(self):
        adrsFromTweet=[]
        triple=[]
        self.readDrugsAndAdrsToArrays()
        self.readTweetsToArray()
        self.createListOfAdrs()
        self.findPairTweetDrug()
        
        for i in range(0,len(self.pairsTweetDrug)):    
            adrsFromTweet=self.getAdrsFromTweetForDrug(self.pairsTweetDrug[i])
            if adrsFromTweet:
                triple=[]
                triple=[self.pairsTweetDrug[i][0],self.pairsTweetDrug[i][1],adrsFromTweet]
                self.finalData.append(triple)
        print ("FINAL DATA: ", self.finalData)
        
    def getAdrsFromTweetForDrug(self, pair): 
        '''funkcja pobiera jeden element z tablicy par tweetow-lekow i zwraca liste numerow skutkow znalezionych w tweecie z tym lekiem'''
        adrNrsFromTweet=[]
        for i in range(0,len(self.adrList)):
            if self.adrList[i] in self.tweets[pair[0]]:
                adrNrsFromTweet.append(i)
        return adrNrsFromTweet
        
        