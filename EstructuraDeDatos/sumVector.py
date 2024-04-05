# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 08:26:28 2024

@author: lizbe
"""


vector=[1,2,3,4,5,6,7,8]
    
def sumVector(vector):
    if(len(vector)==1):
        return vector[0]
    else:
        mitad=len(vector)//2
        izq=vector[:mitad]
        der=vector[mitad:]
        iz= sumVector(izq)
        de= sumVector(der)
        return iz + de

#suma=sumVector(vector)/8

def multiplicacion(vector):
    if(len(vector)==1):
        return vector[0]
    else:
        medio= len(vector)//2
        der= vector[:medio]
        izq= vector[medio:]
        li=multiplicacion(izq)
        ld= multiplicacion(der)
        return li*ld

print(multiplicacion(vector))

def media(vector):
    if(len(vector)==1):
        return (vector[0],1)
    else:
        medio= len(vector)//2
        izq= vector[:medio]
        der= vector[medio:]
        li=media(izq)
        ld=media(der)
        return ((li[0]*li[1]+ld[0]*ld[1])/len (vector),len (vector))
    
def media1(vector):
    if(len(vector)==1):
        return vector[0]
    else:
        medio= len(vector)//2
        izq= vector[:medio]
        der= vector[medio:]
        li=media1(izq)
        ld=media1(der)
        aux=li+ld
        return aux/2
    
        
print(media(vector))    
print(media1(vector))

def comparacionDosVectores(v1,v2):
    if(len(v1)==1 or len(v2)==0):
        if(len(v1)==len(v2)):
            if(v1[0]==v2[0]):
                return 1
            else:
                return 0
        else:
            return 0
    else:
        medio= len(v1)//2
        izq1= v1[:medio]
        izq2= v2[:medio]
        der1= v1[medio:]
        der2= v2[medio:]
        li= comparacionDosVectores(izq1, izq2)
        ld= comparacionDosVectores(der1, der2)
        return li*ld
    
vector2=[1,2,4,5,6]
vector1=[199,2,124,4,6]
isA=comparacionDosVectores(v1=vector1, v2=vector2)

def maximo(v1):
    if(len(v1)==1):
        return v1[0]
    else:
        medio= len(v1)//2
        izq=v1[:medio]
        der=v1[medio:]
        li=maximo(izq)
        ld=maximo(der)
        if(li>ld):
            return li
        else:
            return ld
        
def minimo(v1):
    if(len(v1)==1):
        return v1[0]
    else:
        medio= len(v1)//2
        izq=v1[:medio]
        der=v1[medio:]
        li=minimo(izq)
        ld=minimo(der)
        if(li<ld):
            return li
        else:
            return ld
        
#minimo=minimo(vector1)     

def minmax(v1):
    if(len(v1)==1):
        return (v1[0],v1[0])
    else:
        medio= len(v1)//2
        izq=v1[:medio]
        der=v1[medio:]
        li=minmax(izq)
        ld=minmax(der)
        if(li[0]<ld[0]):
            resultado=(li[0],li[1])
            if(ld[1]>li[1]):
                resultado=(li[0],ld[1])
            return resultado
        else:
            if(li[1]>ld[1]):
                return (ld[0],li[1])
            else:
                return ld
    
#mn= minmax(vector1)
        
    
    
        
        
        
        
        
        
        