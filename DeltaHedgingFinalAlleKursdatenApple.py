#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 11:08:04 2020

@author: Robert_Hennings
"""


import pandas as pd
df = pd.read_csv ("AAPL.csv")
del df['Open']
del df['High']
del df['Low']
del df['Close']
del df['Volume']        #Jetzt sind nur noch das Datum als Spalte und die Schlusskurse als Spalte zum Datum vorhanden

                        #Jetzt soll ein spezifischer 10 Tageszeitraum ausgewählt werden, andem die Startegie aufgesetzt wird und über die ausgewählte Periode betrachtet wird
                        #dies geht mit der Angabe der Zeilen die wir wollen hier die ersten 10 aber es gehen auch spezielle dies dann durch Angabe
df_new=df[:2517]          #Alle Zeilen der Apple Datei liegen vor mit Datum und Schlusskurs
                        #in erster Periode soll nun gehedgtes Portfolio aufgesetzt werden!
                        #Erstellung einer neuen Spalte für den Optionswert zu jedem Kurs
                        #Befüllung dieser Spalte mit den Funktionswerten 
                        #Die Erstellte Spalte soll nun mit den Funktionswerten für die BSM Optionen Call befüllt werden die jeweils die S Werte aus der Spalte 2 nimmt

import numpy as np
import scipy.stats as si
from sympy import init_printing
init_printing()

def euro_vanilla_call(S, K, T, r, sigma):
    
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    call = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    
    return call

euro_vanilla_call(df_new['Adj Close'], 100, 1, 0.05, 0.25)

df_new['BSM Price'] = euro_vanilla_call(df_new['Adj Close'], 100, 1, 0.05, 0.25) #Jetzt sind die Call Optionspreise nach BSM mit den festgelegten Inputparametern festgelegt
                                                                                #Nun soll in der ersten Periode gehedged werden , es muss die Underlying Menge kalkuliert werden und eine Funktion für den P/L des Portfolios eingeführt werden

df_new['Difference'] = df_new['Adj Close'].pct_change()                         #Nochmal checken ob der hier wirklich die Differenz der einzelnen Spaltenwerte des Adj Close voneinander je tag abzieht um so die Veränderung darzustellen
     
def Delta_Call(S, K, T, r, sigma):
         delta = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))                                                          #Jetzt muss noch das Delta der Option ausgerechnet werden
                                                                
         return delta

Delta_Call(df_new['Adj Close'], 100, 1, 0.05, 0.25)

df_new['Delta Option'] = Delta_Call(df_new['Adj Close'], 100, 1, 0.05, 0.25)    #Deltas der Optionen wurden nun berechnet und extra in einer Spalte abgelegt
  
def Hedge_Underlying(D):
    MengeUnderlying = 0-df_new['Delta Option']
                                                                                #Jetzt soll gehedged werden am 2020-08-02, dafür bedarf es einer Funktion um den P/L des Portfolios aufzusetzen und anfänglich muss die Menge an Underlying berechnet werden um delta =0 zu erzeieln
    return MengeUnderlying
Hedge_Underlying(df_new['Delta Option'])

df_new['HedgeMengeUnder'] = Hedge_Underlying(df_new['Delta Option'])            #jetzt muss eine Funktion für den P/L des Portfolios aufgestellt werden, könnte mit if funktionieren und unter Bezugname zum Differenzwert der Spalte Differenz um anzuzeigen ob das Underlying gestiegen oder gefallen ist, erstmalden P/L der Underlying Position als Spalte einfügen

def PL_Underlying_Position(Diff):
    PL = df_new['Difference']*df_new.loc[0,'HedgeMengeUnder']                   #ich brauche hier den Wert 4.18511 der als Vorfaktor gelten soll!
    
    return PL
df_new['P/LUnderl'] = PL_Underlying_Position(df_new.loc[0,'HedgeMengeUnder'])  #Jetzt wurde unser Hedging Wert des Underlyings mit den Schwankungen des Underlyings multipliziert was uns die Schwanlung bzw Profit oder Loss unserer 4.18511 Underlying Position angibt
                                                                                #Es müssen die Differenzen der einzelnen BSM Preise zu den unterscheidlichen S werten von dem Ursprungswert berechnet werden und als Spalte ausgegeben werden
                                                                                #stehen diese fest als neue Spalte wird dann die P/L Formel für das ganze Portfolio gebildet indem die einzelnen Spalteneinträge der Spalte P/L Underly und der neu geschaffenen Spalte mit den Differenzen der BSM Preise vom Ursprungswert addiert werden

def PL_BSM(DiffBSM):
    PLBSM = df_new['BSM Price']-df_new.loc[0,'BSM Price']                       #Es wird die Differenz der einzelnen BSM Preise zu den unterscheidlichen S berechnet vom Ursprungswert ausgehend bei dem gehedged wurde
    return PLBSM
df_new['P/LBSM'] = PL_BSM(df_new['BSM Price']-df_new.loc[0,'BSM Price'])
                                                                                #Jetzt kann die P/L Formel für das gesamte Portfolio gebildet werden indem die Zwei Spalten addiert werden: P/LBSM und P/LUnderly

def PL_Total(DiffTotal):
    PLTotal = df_new['P/LBSM'] - df_new['P/LUnderl']
    
    return PLTotal
df_new['P/L Total'] = PL_Total(df_new['P/LBSM'] - df_new['P/LUnderl'])          #Jetzt sollte in der Spalte P/LTotal der Portfoliowert des gehedgten Portfolios erscheinen der in Abhängigkeit der verscheidenen Parameter leicht schwankt, dies könnte man jetzt noch aufplotten und schauen ob dies logisch und rechnerisch alles so hinkommt
                                                                                #Zum plotten sollen jetzt an der x Achse der S Wert stehen und an der y Achse der Wert unseres Portfolios also die einzelnen Einträge der Spalte P/L Total in Abhängigkeit von dem S

                   
df_new['Adj Close'].plot(x='Adj Close',y='P/L Total')                   

df_new.plot(x='Adj Close',y='P/L Total')                                

df.plot(x='Date', y='Adj Close')
df_new.plot(x='Date',y='BSM Price')
