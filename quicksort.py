# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:43:40 2024

@author: lizbe
"""

def quickSort(lista):
    if(len(lista)<=1):
        return lista
    else:
        pivot= lista[-1]
        izq=[]
        der=[]
        for i in range(len(lista)-1):
            if(lista[i]<=pivot):
                izq.append(lista[i])
            elif(lista[i]>pivot):
                der.append(lista[i])
        return quickSort(izq)+[pivot]+quickSort(der)

print(quickSort([12,5,7,1,9]))