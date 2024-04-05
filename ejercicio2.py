# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 16:24:01 2024

@author: lizbe
"""

def algoritmoEuclides(a,b):
    while(b!=0):
        c=b
        b= a % b
        a= c
    return a

print(algoritmoEuclides(150, 39))

def algoritmoBusquedaBinaria(lista, objetivo):
    izq= 0
    derecha=len(lista)-1
    while(izq<=derecha):
        med=round((derecha+izq)/2)
        if(lista[med]==objetivo):
            return med
        elif (lista[med]>objetivo):
            derecha=med-1
        else:
            izq= med+1
lista=[]
for i in range(1,23,2):
    lista.append(i)
print(lista)
# O(log(n))
print(algoritmoBusquedaBinaria(lista, 19))

lista=[]
for i in range(1,23,2):
    lista.append(i)
print(lista)
print(algoritmoBusquedaBinaria(lista, 19))