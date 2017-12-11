'''
Created on 4 gru 2017

@author: Witek
'''
import plotly.plotly as py
import plotly.graph_objs as go
from _overlapped import NULL

class Dictionary:
    
    ######   ZMIENNE
    
    adrs=[] #tablica tablic z odpowiadaj¹cymi numerem glownym lekom z drugs, elementem tablicy jest tablica z roznymi skutkami ubocznymi'''
            #(pierwsza jest liczba procent u ilu wystepuje'''
    
    drugs=[] #'''tablica tablic z lekami (kilka nazw w jednym elemencie tablicy)'''
    
    tweets=[] #'''tablica z wypowiedziami ludzi, jedna wypowiedz to jeden element'''
    
    pairsTweetDrug=[] #'''para oznaczajaca w jakim tweecie znaleziono lek i - numer tweetu, j - jaki lek znaleziono'''
    
    adrList=[] #'''lista wszystkich skutkow ubocznych zawartych w danych '''
    
    finalData=[] #Tablica z trojkami cyfr - 1. numer tweetu, 2. numer leku 3. tablica skutków
    
    percents=[] #Tablica o takiej samej wielkosci co adry, na miejscach adrow sa cyfry oznaczajace procenty wystepowania
    
    adrswithoutpercent=[] #To samo co tablica adrs[] tylko z usunietymi procentami

    adrsWithoutPercentUpgraded=[]
    
    sumsOfDrugs=[] #Tablica sum ilosci wystepowan tweetow o danych lekach
 
    sumsOfAdrs=[]
 
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
            for i in range(1,len(split)): ##########################################
                split[i]=split[i].replace('\n','')
                split[i]=split[i].replace(';','')
                adrhelp.append(split[i])
            adrtemp.append(adrhelp)
        return adrtemp
        
    def readDrugsAndAdrsToArrays(self):
        fileName=input("Podaj nazwe pliku z lekami i skutkami ubocznymi do wczytania: ")
        self.drugs=self.getDrugTemp("data.txt") #dac zmienna fileName!!!
        self.adrs=self.getAdrTemp("data.txt")   #dac zmienna fileName!!!
        
    def printAllData(self):
        #print("\nADRY W ODPOWIEDNIEJ KOLEJNOSCI:\n",self.adrs)
        print("\nDRUGS W ODPOWIEDNIEJ KOLEJNOSCI:\n", self.drugs)
        #print("\nTWEETY LUDZI:\n",self.tweets)
        print("\nLISTA WSZYSTKICH ADROW:\n",self.adrList)
        print("\nFINAL DATA CZYLI TWEET, LEK, SKUTKI:\n",self.finalData,"\n")
        print("\nADRY BEZ PROCENTOW:\n",self.adrswithoutpercent)
        #print("\nPERCENTY SAME:\n",self.percents)
        print("\nADRY UZUPELNIONE O ODCZYTANE SKUTKI:\n",self.adrsWithoutPercentUpgraded)

        
    def createListOfAdrs(self):
        spl=[[] for i in range(len(self.adrs))]
        splfull=[]
        for i in range(0,len(self.adrs)):
            for j in range(0,len(self.adrs[i])):
                help=self.adrs[i][j].split('-')
                spl[i].append(help)
            splfull.append(spl[i])
        for i in range(0,len(splfull)):
            for j in range(0,len(splfull[i])):
                for k in range(0,len(splfull[i][j])):
                    if not self.adrList and not splfull[i][j][k].isdigit():
                        self.adrList.append(splfull[i][j][k])
                    if splfull[i][j][k] not in self.adrList and not splfull[i][j][k].isdigit():
                        self.adrList.append(splfull[i][j][k])
                                
    def readTweetsToArray(self):
        fileName=input("Podaj nazwe pliku z danymi wolnych wypowiedzi pacjentow: ")
        with open('tweets.txt', 'r') as myfile:
            data=myfile.read().replace('\n', '')
            data=data.lower()
        self.tweets=data.split(';;;;;;')
        
    def findPairTweetDrug(self):
        for i in range(0,len(self.tweets)):
            for j in range(0,len(self.drugs)-1):
                for k in range(0,len(self.drugs[j])):   
                    if self.drugs[j][k] in self.tweets[i]: 
                        pair=[i,j] 
                        '''para oznaczajaca w jakim tweecie znaleziono lek i - numer tweetu, j - jaki lek znaleziono'''
                        self.pairsTweetDrug.append(pair)
 
    def getAdrsFromTweetForDrug(self, pair): 
        '''funkcja pobiera jeden element z tablicy par tweetow-lekow i zwraca liste numerow skutkow znalezionych w tweecie z tym lekiem'''
        adrNrsFromTweet=[]
        for i in range(0,len(self.adrList)):
            if self.adrList[i] in self.tweets[pair[0]]:
                adrNrsFromTweet.append(i)
        return adrNrsFromTweet
       
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
    
        self.upgradeAdrWithNewAdrs()
        
    def createFirstColumnInTable(self):
        column=[]
        for i in range(0,len(self.adrsWithoutPercentUpgraded)):
            for j in range(0,len(self.adrsWithoutPercentUpgraded[i])):
                if j==0:
                    column.append(self.drugs[i][0])
                else:
                    column.append('')
            #column.append('')
        return column
    
    def separatePercentFromAdr(self):
        for i in range(0,len(self.adrs)):
            temp=[]
            temp2=[]
            for j in range(0,len(self.adrs[i])):
                temp.append('')
                temp2.append(self.adrs[i][j])
            self.percents.append(temp)
            self.adrswithoutpercent.append(temp2)   
        for i in range(0,len(self.adrs)):
            for j in range(0,len(self.adrs[i])):
                split=self.adrs[i][j].split('-')
                if split[0].isdigit():
                    temp=split[0]+'-'
                    self.adrswithoutpercent[i][j]=self.adrs[i][j].replace(temp,'')
                    self.percents[i][j]=split[0]
        
    def upgradeAdrWithNewAdrs(self):
        self.separatePercentFromAdr()
        for i in range(0,len(self.adrswithoutpercent)):
            temp=[]
            for j in range (0,len(self.adrswithoutpercent[i])):
                temp.append(self.adrswithoutpercent[i][j])
            self.adrsWithoutPercentUpgraded.append(temp)
            
        for i in range(0, len(self.finalData)):
            for j in range(0,len(self.finalData[i][2])):
                if self.adrList[self.finalData[i][2][j]] not in self.adrswithoutpercent[self.finalData[i][1]]:
                    self.adrsWithoutPercentUpgraded[self.finalData[i][1]].append(self.adrList[self.finalData[i][2][j]])
                    self.percents[self.finalData[i][1]].append('')
                    
    def createAdrColumnInTable(self):
        column=[]
        for i in range(0,len(self.adrsWithoutPercentUpgraded)):
            for j in range(0,len(self.adrsWithoutPercentUpgraded[i])):
                split=self.adrsWithoutPercentUpgraded[i][j].split('-')
                column.append(split[0])
        return column
    
    def createDeclaredColumnInTable(self):
        column=[]
        for i in range(0,len(self.percents)):
            for j in range(0,len(self.percents[i])):
                if self.percents[i][j]=='':
                    column.append('?')
                else:
                    display=self.percents[i][j]+' %'
                    column.append(display)
        return column 
    
    def isOneAdrFromDrug(self,element,element2):
        for i in range(0,len(self.adrsWithoutPercentUpgraded[element2])):
                if self.adrList[element] in self.adrsWithoutPercentUpgraded[element2][i]:
                    return True
        return False
    
    def whichAdrFromDrug(self, element, element2):
        for i in range(0,len(self.adrsWithoutPercentUpgraded[element2])):
                if self.adrList[element] in self.adrsWithoutPercentUpgraded[element2][i]:
                    return i
        return NULL
     
    def calculatePercentageOfAdr(self):
        for i in range(0,len(self.drugs)):
            self.sumsOfDrugs.append(0)
        for i in range(0,len(self.adrsWithoutPercentUpgraded)):
            temp=[]
            for j in range(0,len(self.adrsWithoutPercentUpgraded[i])):
                temp.append(0)
            self.sumsOfAdrs.append(temp)
        for i in range(0,len(self.drugs)):
                for j in range(0,len(self.pairsTweetDrug)):
                        if self.pairsTweetDrug[j][1]==i:
                            self.sumsOfDrugs[i]=self.sumsOfDrugs[i]+1
        for i in range(0,len(self.finalData)):
            for j in range(0,len(self.finalData[i][2])):
                for k in range(0, len(self.adrsWithoutPercentUpgraded)):
                    if self.isOneAdrFromDrug(self.finalData[i][2][j],k) and self.finalData[i][1]==k:
                        self.sumsOfAdrs[k][self.whichAdrFromDrug(self.finalData[i][2][j],k)]=self.sumsOfAdrs[k][self.whichAdrFromDrug(self.finalData[i][2][j],k)]+1
        print(self.sumsOfDrugs)
        print(self.sumsOfAdrs)
                        
    def createReadColumnInTable(self):
        column=[]
        for i in range(0,len(self.adrsWithoutPercentUpgraded)):
            for j in range(0,len(self.adrsWithoutPercentUpgraded[i])):
                if self.sumsOfDrugs[i]!=0:
                    temp=self.sumsOfAdrs[i][j]/self.sumsOfDrugs[i]*100
                    temp=str(temp)+' %'
                    column.append(temp)
                else:
                    column.append('X')
        return column
                
        
    def fillTable(self):
        cellsh=dict(values=[self.createFirstColumnInTable(),
                           self.createAdrColumnInTable(),
                           self.createDeclaredColumnInTable(),
                           self.createReadColumnInTable()])
        trace = go.Table(
        header=dict(values=['Lek', 'Skutki uboczne','deklarowane','odczytane']),
        cells=cellsh)
     
        data = [trace] 
        py.plot(data, filename = 'example_table')
        
        