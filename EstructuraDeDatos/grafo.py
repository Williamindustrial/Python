# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:16:32 2024

@author: lizbe
"""
from queue import LifoQueue
from queue import Queue

class node:
    
    def __init__(self,dato):
        self.dato=dato
        self.anteriores=[]
        self.siguientes=[]
        self.visitado=False
        self.descrubierto=False
    
    def addAnterior(self, node):
        self.anteriores.append(node)
    
    def addSiguientes(self, node):
        self.siguientes.append(node)


A= node("A")
B= node("B")
C= node("C")
D= node("D")
E= node("E")
F= node("F")

A.addSiguientes(B)
B.addSiguientes(C)
B.addSiguientes(D)
B.addSiguientes(E)
D.addSiguientes(F)

def profundidad(raiz):
    raiz.descrubierto=True
    siguientes= raiz.siguientes
    for nodoSiguiente in siguientes:
        if(nodoSiguiente.visitado==False):
            nodoSiguiente.descrubierto=True
            profundidad(nodoSiguiente)
    raiz.visitado=True
    print(raiz.dato)

def anchura(raiz):
    cola = Queue()
    actual=raiz
    cola.put(actual)
    while( cola.empty()==False):
        actual.visitado=True
        actual= cola.get()
        for nodoSiguiente in actual.siguientes:
            cola.put(nodoSiguiente)
        print(actual.dato)
anchura(A)
            
            



        
        
