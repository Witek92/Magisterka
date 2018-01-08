'''
Created on 21 lis 2017

@author: Witek
'''
from program.AdrDetection import AdrDetection

if __name__ == '__main__':
    adr=AdrDetection()
    a=input("Ktora metoda? Wybierz litere:\na-metoda podstawowa\nb-metoda human method\nc-metoda z wykorzystaniem WordNet\n")
    if a=='a':
        adr.basicMethod()
    if a=='b':
        adr.humanMethod()
    if a=='c':
        adr.wordNetMethod()
    adr.fillTable()
    adr.printAllData()
    