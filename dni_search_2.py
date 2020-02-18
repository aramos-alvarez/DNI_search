# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from IPython import display



def DNIs_in_string(string):
#"Returns a list of DNIs from a string (it could be a file converted in string previously)"
#"DNI FORMATS supports 15412562-D 15412562 D 15412562D"

    DNIs =  re.findall(r'\d+', string)
    length = len(DNIs)
    list_good_DNIs = []
    for _ in range(length):
       
        if len(DNIs[_]) == 8:
             list_good_DNIs.append(DNIs[_])
    DNIs = list_good_DNIs
            
        
    count_list = 0
    
    for _ in range(len(DNIs)):
        b = string.find(DNIs[count_list])+8
        
        try:
            if string[b] == ' ' or string[b] == '-':
#                print(DNIs[count_list])
                letter = string[b+1]
                
            else: 
                letter = string[b]
                
            DNIs[count_list] = DNIs[count_list] + letter
        except IndexError:
            DNIs.remove(DNIs[count_list])
    
        
        count_list += 1
    
    #check uniques values
    dataframe = pd.DataFrame(DNIs)
    DNIs = list(dataframe[0].unique())
    return DNIs

if __name__ == '__main__':

    
    os.chdir(r'C:\Users\aramos\Desktop')
    
    dataframe = pd.read_csv('dni_text.txt', encoding = "ISO-8859-1", header = None)
    dataframe = dataframe.fillna('')
    dataframe[2] = dataframe[2]+ dataframe[3]
    dataframe= dataframe[[0,1,2]]
    
    MASK = (dataframe[0] == 1) & (dataframe[1] > 0)
    dataframe = dataframe[MASK]
    dataframe[2] = dataframe[2].apply(str)
    dataframe[2] = dataframe[2].apply(DNIs_in_string)
    output_dataframe = pd.DataFrame()
    output_dataframe['ROW'] = dataframe.index +1 
    output_dataframe['DNIs found'] = list(dataframe[2])
    print('OUTPUT DATAFRAME:\n ==============')
    display.display(output_dataframe)