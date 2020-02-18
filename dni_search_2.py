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
import shutil


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
    
    #INPUT
    name_file = 'dni_text.txt'
    
    os.chdir(r'C:\Users\aralvarez\Desktop')
    
    shutil.copy(name_file, 'duplicate.txt')
    name_file = 'duplicate.txt'
    #Maximum number of comma in dataframe 20
    def line_prepender(filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(line.rstrip('\r\n') + '\n' + content)
    line_prepender(name_file, '0 ,0 , , , , , , , , , , , , , , ,')
    

    #LOAD DATA
    dataframe = pd.read_csv(name_file, encoding = "ISO-8859-1", header = None)
    
    os.remove(name_file)
    
    dataframe = dataframe.drop(0, axis = 0)
    dataframe = dataframe.fillna('')

    #DataFrame should have 3 columns the last one with a string
    for i in range(3, dataframe.keys().size):
        dataframe[2] = dataframe[2]+ dataframe[i]
        
    dataframe= dataframe[[0,1,2]]
    dataframe[2] = dataframe[2].apply(str)

    MASK = (dataframe[0] == 1) & (dataframe[1] > 0)
    dataframe = dataframe[MASK]
    
    dataframe[2] = dataframe[2].apply(DNIs_in_string)
    output_dataframe = pd.DataFrame()
    output_dataframe['ROW'] = dataframe.index 
    output_dataframe['DNIs found'] = list(dataframe[2])
    print('OUTPUT DATAFRAME:\n ==============')
    display.display(output_dataframe)
    output_dataframe.to_csv('output_dni.csv', index = False)