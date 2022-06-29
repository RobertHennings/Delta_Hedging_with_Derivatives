#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 18:42:11 2020

@author: Robert_Hennings
"""
def main():
    
    #Main two parameters to edit for individual use cases:
    #Strike Price K for the european Call Option (Trader expects that the underlying is going up in the future) 
    K = 31
    #Number of Trading Days for which the Experiment should be observed
    Trading_days = 50
    #Importing all necessay libraries
    import pandas as pd
    import numpy as np
    import scipy.stats as si
    from sympy import init_printing
    import matplotlib.pyplot as plt 
    import matplotlib
    # setting Resolution from matplotlib to a higher Standard
    plt.rcParams['figure.dpi'] = 600
    #Reading in the downloaded csv file from yahoo finance for the Apple Stock
    globals()["df"] = pd.read_csv ("/Users/Robert_Hennings/Dokumente/IT Weiterbildung/Python Data Analysis /AbbeV/Meine Projekte/Static Hedging Strategies/AAPL.csv")
    #Checking basic Information of the loaded data, NaNs, Basic Statistcics, and so on
    globals()["df"].describe()
    globals()["df"].info()
    globals()["df"].isna()
    globals()["df"].count()
    #Dropping all unnecessary data/columns
    globals()["df"].drop(globals()["df"].columns[2:len(globals()["df"].columns)-2], axis=1, inplace=True)
    globals()["df"].drop(["Open", "Volume"], axis=1, inplace=True)
    #Everything that is left is the Date and the Adj Close column
    
    #Now there is taken a specific 10 day period to show the basic mechanics of the shown exapmles
    # df_new=df[:10]  
    globals()["df_new"] = globals()["df"][:Trading_days]
    #Transforming the Date column to its correct Datatype, datetime
    # globals()["df_new"]["Date"] = pd.to_datetime(globals()["df_new"]["Date"])
    #this goes with the indication of the lines which we want here the first 10 however it go also special this then by indication
    #first 10 lines are available with date and closing price
    #in the first period (day) the hedged portfolio has to be set up!
    #creation of a new column for the option value of each course
    #filling this column with the function values 
    
    #The created column should now be filled with the function values for the BSM Call options, each of which takes the S values from column 2.         
    # init_printing()
    #The single steps to create a delta and later on a delta gamma neutral position
    """
    1) Calculating the fair price for the Call option using the BSM formula
    2) Calculating the amount of calls in the whole position value (not necessary in this code example)
    3) Calculating the Delta for one Call using the Delta formula
    4) Delta for one Call (not necessary in this code example)
    5) Delta for the whole position (not necessary in this code example)
    6) Making the position delta neutral by investint in the underlying
    
    Sidetask: What is the Profit/ Loss (P/L) for the portfolio when the underlying price S jumps to 100 $?
    
    """
   
    ################################################################### Step 1) #####################################
    #Creating the formula for a plain vanilla european call
    def euro_vanilla_call(S, K, T, r, sigma):
        """
        Parameters
        ----------
        S : TYPE int
            Spot price
        K : TYPE int
            Strike price
        T : TYPE int
            Time to maturity
        r : TYPE int
            Interest rate
        sigma : TYPE int
            Volatility of underlying asset
    
        Returns
        -------
        call : TYPE int
            Returns the fair value of a plain vanilla european call option.
        """
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        call = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
        
        return call
    #Now applying the created formula for the option pricing and saving its values into a new column for the selected 10 days
    globals()["df_new"]['BSM Price'] = euro_vanilla_call(globals()["df_new"]['Adj Close'], K, 1, 0.05, 0.25) 
    #Now we want to hedge in the first period, calculate the underlying quantity and introduce a function for the P/L of the portfolio.
    
    #Check again if this really subtracts the difference of the individual column values of the Adj Close from each other per day to show the change.
    #Basically just the normal Return of the stock
    globals()["df_new"]['Difference'] = globals()["df_new"]['Adj Close'].diff()
    print("Check")
    ################################################################### Step 3) #####################################
    #Now creating the formula to compute the Delta of the held position
    def Delta_Call(S, K, T, r, sigma):
        """
        Parameters
        ----------
        S : TYPE int
            Spot price
        K : TYPE int
            Strike price
        T : TYPE int
            Time to maturity
        r : TYPE int
            Interest rate
        sigma : TYPE int
            Volatility of underlying asset
    
        Returns
        -------
        delta : TYPE
            Returns the Delta value of a plain vanilla european call option.
    
        """
        #Calculating the Delta Value of the financial product according to the BSM formula
        delta = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T)) 
                                                                    
        return delta
    #Testing the computation of the Delta Value
    Delta_Call(globals()["df_new"]['Adj Close'], K, 1, 0.05, 0.25)
    #Applying this formula to the given Data and saving its values in a new column
    globals()["df_new"]['Delta Option'] = Delta_Call(globals()["df_new"]['Adj Close'], K, 1, 0.05, 0.25) #Deltas of the options were now calculated and stored extra in a column
    print("Check")
    ################################################################### Step 6) #####################################
    #Now creating the formula to see how the exposure can be hedged
    def Hedge_Underlying(D):
        """
        Parameters
        ----------
        D : TYPE int 
            To calculate the amount of the underlying that is 
            necessary to hedge the Delta exposure, the Delta
            needs to be the Input Parameter.
    
        Returns
        -------
        MengeUnderlying : TYPE int
            The amount of the underlying that is necessary to hedge against Delta exposure.
    
        """
        MengeUnderlying = D*(-1)
        #Now we want to hedge on 2020-08-02, for this we need a 
        #function to set up the P/L of the portfolio and initially we need 
        #to calculate the amount of underlying to get delta =0
        return MengeUnderlying
    
    #Test the formula
    Hedge_Underlying(globals()["df_new"]['Delta Option'])
    #Apply the formula and save its results into a new column
    globals()["df_new"]['HedgeMengeUnder'] = Hedge_Underlying(globals()["df_new"]['Delta Option']) #now a function for the P/L of the portfolio must be set up, could work with if and under reference name to the difference value of the column difference to indicate whether the underlying has risen or fallen, insert the P/L of the underlying position as a column for the first time
    
    ################################################################### Sidetask #####################################
    #At first calculating the profits/losses from the initial set up short position in the underlying, 
    #losses since the underlying rises in price
    def PL_Underlying_Position(Diff):
        PL = globals()["df_new"]['Difference']*Diff  
        return PL
    #Applying the P/L formula of the underlying to the given data and saving its results into a new column
    #Now our hedging value of the underlying was multiplied with the fluctuations 
    #of the underlying which gives us the fluctuation or profit or loss of our 4.18511 underlying position.
    globals()["df_new"]['P/LUnderl'] = PL_Underlying_Position(globals()["df_new"].loc[0,'HedgeMengeUnder'])  
    
    #Now the fair BSM Call price has to be computed for each new price of the underlying
    #The differences of the individual BSM prices to the different S values must be calculated from the original value and output as column
    #If this is fixed as a new column, the P/L formula for the whole portfolio is formed by adding the individual column entries of the P/L Underly column and the newly created column with the differences of the BSM prices from the original value.
    
    def PL_BSM(ActualBSMPrice,InitialBSMPrice):
        PLBSM = ActualBSMPrice-InitialBSMPrice 
        #The difference of the individual BSM prices at the different S is 
        #calculated from the original value at which hedging was performed.
        return PLBSM
    
    globals()["df_new"]['P/LBSM'] = PL_BSM(globals()["df_new"]['BSM Price'],globals()["df_new"].loc[0,'BSM Price'])
    
    #Now the P/L formula can be formed for the entire portfolio 
    #by adding the two columns: P/LBSM and P/LUnderly
    
    def PL_Total(PL_BSM, PL_Underlying):
        PLTotal = PL_BSM + PL_Underlying
        return PLTotal
    
    globals()["df_new"]['P/L Total'] = PL_Total(globals()["df_new"]['P/LBSM'],globals()["df_new"]['P/LUnderl']) 
    print("Check")
    #Now in the column P/LTotal the portfolio value of the hedged portfolio should appear 
    #which varies slightly in dependence of the different parameters, this could one 
    #now still plot and look whether this logically and computationally everything goes so
    #For plotting now at the x axis the S value should stand and at the 
    #y axis the value of our portfolio thus the individual entries of the column P/L Total 
    #depending on the S
    plt.plot(globals()["df_new"]['Date'], globals()["df_new"]['Adj Close'], label="Price Underlying",color="#015092")
    plt.plot(globals()["df_new"]['Date'], globals()["df_new"]['P/L Total'], label="P/L Total", color="#a1cd08")
    plt.legend()
    plt.xticks(fontsize=6,rotation=45)
    plt.title("The P/L of the Delta-Hedged Portfolio in dependence of the movement of the underlying stock")
    plt.xlabel("Trading Days")
    plt.ylabel("Stock Price and P/L Total Amount")
    plt.hlines(y=K,xmin=0,xmax=Trading_days,colors="black")
    plt.hlines(y=0,xmin=0,xmax=Trading_days,colors="black")
    plt.show()
                                
    globals()["df_new"]["Total Gain/Loss if closed on that Day"] = globals()["df_new"]["P/L Total"].cumsum()
    print("Check for Final")
    #will man wissen was der finale P/L ist bis zu einer gewissen Periode muss man die einzelnen P/L Total Werte bis hin zu dieser Periode aufsummieren cumsum                          
    #wenn man jetzt mehr als die verwendeten 10 werte nutzt könnte man noch den Durchschnitt des P/L Total bilden wan dann ja ungefähr 0 sein sollte ca oder ggf sogar dann Profit hängt halt von der betrachteten Underlying Periode ab!
    
    plt.plot(globals()["df_new"]['Date'], globals()["df_new"]['Adj Close'], label="Price Underlying", color="#015092")
    plt.plot(globals()["df_new"]['Date'], globals()["df_new"]['Total Gain/Loss if closed on that Day'], label="Total Gain/Loss", color="#a1cd08")
    plt.legend()
    plt.xticks(fontsize=6, rotation=45)
    plt.title("Total Gain/Loss of the Delta-Hedged Portfolio in dependence of the movement of the underlying stock")
    plt.xlabel("Trading Days")
    plt.ylabel("Stock Price and Total Gain/Loss")
    plt.hlines(y=K,xmin=0,xmax=Trading_days,colors="black")
    plt.hlines(y=0,xmin=0,xmax=Trading_days,colors="black")
    plt.show()
    print("Check Final")
    
if __name__ == "__main__":
    main()