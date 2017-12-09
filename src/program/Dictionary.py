'''
Created on 4 gru 2017

@author: Witek
'''
import plotly.plotly as py
import plotly.graph_objs as go

class Dictionary:
    
    ######   ZMIENNE
    
    adrs=[] #tablica tablic z odpowiadaj¹cymi numerem glownym lekom z drugs, elementem tablicy jest tablica z roznymi skutkami ubocznymi'''
            #(pierwsza jest liczba procent u ilu wystepuje'''
    
    
    drugs=[] #'''tablica tablic z lekami (kilka nazw w jednym elemencie tablicy)'''
    
    
    tweets=[] #'''tablica z wypowiedziami ludzi, jedna wypowiedz to jeden element'''
    
    
    pairsTweetDrug=[] #'''para oznaczajaca w jakim tweecie znaleziono lek i - numer tweetu, j - jaki lek znaleziono'''
    
    
    adrList=[] #'''lista wszystkich skutkow ubocznych zawartych w danych '''
    
    
    finalData=[]
    
    percents=[]
    
    adrswithoutpercent=[]

 
 
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
        print("\nADRY W ODPOWIEDNIEJ KOLEJNOSCI:\n",self.adrs)
        print("\nDRUGS W ODPOWIEDNIEJ KOLEJNOSCI:\n", self.drugs)
        #print("\nTWEETY LUDZI:\n",self.tweets)
        print("\nLISTA WSZYSTKICH ADROW:\n",self.adrList)
        print("\nFINAL DATA CZYLI TWEET, LEK, SKUTKI:\n",self.finalData,"\n")
        #print("\nADRY BEZ PROCENTOW:\n",self.adrswithoutpercent)
        #print("\nPERCENTY SAME:\n",self.percents)
        
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
    
    def createFirstColumnInTable(self):
        column=[]
        for i in range(0,len(self.adrs)):
            for j in range(0,len(self.adrs[i])):
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
        
    def createAdrColumnInTable(self):
        column=[]
        for i in range(0,len(self.adrswithoutpercent)):
            for j in range(0,len(self.adrswithoutpercent[i])):
                split=self.adrswithoutpercent[i][j].split('-')
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
        
    
    def fillTable(self):
        cellsh=dict(values=[self.createFirstColumnInTable(),
                           self.createAdrColumnInTable(),
                           self.createDeclaredColumnInTable(),
                           [95, 85, 75, 95]])
        trace = go.Table(
        header=dict(values=['Lek', 'Skutki uboczne','deklarowane','odczytane']),
        cells=cellsh)
     
        data = [trace] 
        py.plot(data, filename = 'example_table')
        
        