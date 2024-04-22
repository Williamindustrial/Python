# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:07:49 2024

@author: lizbe
"""

class nodo():
    def __init__ (self, dato):
        self.dato= dato
        self.siguiente=None
    
class LinkedList():
    def __init__(self):
        self.head = None
        self.size=0
    
    def add( self, dato):
        nuevoNodo= nodo(dato=dato)
        if  self.head==None:
            self.head= nuevoNodo
        else:
            actual= self.head
            while actual.siguiente!= None:
                actual=actual.siguiente
            actual.siguiente=nuevoNodo
        self.size=self.size+1
    
    def add_first(self, dato):
        actualF= self.head
        nuevoNodo= nodo(dato=dato)
        self.head=nuevoNodo
        nuevoNodo.siguiente= actualF
        self.size=self.size+1
    def add_pos(self, dato, pos):
        if(self.size-1>=pos):
            if(pos==0):
                self.add_first(dato)
            else:
                nuevoNodo= nodo(dato=dato)
                nodoActual=self.head
                contadorPos=0
                while(nodoActual.siguiente!= None) and (contadorPos+1<pos):
                    contadorPos=contadorPos+1
                    nodoActual= nodoActual.siguiente
                actualF= nodoActual.siguiente
                nodoActual.siguiente= nuevoNodo
                nuevoNodo.siguiente= actualF
            self.size=self.size+1
                

    def getFirst(self):
        return self.head.dato
    
    def getLast(self):
        actual=self.head
        while actual.siguiente!= None:
            actual=actual.siguiente
        return actual.dato
    
    def get(self, pos):
        nodoActual=self.head
        contadorPos=0
        while(nodoActual.siguiente!= None) and (contadorPos<pos):
            contadorPos=contadorPos+1
            nodoActual= nodoActual.siguiente
        return nodoActual.dato
    
    def delateFirst(self):
        self.head=self.head.siguiente
        self.size=self.size-1
    
    def delateLast(self):
        actual=self.head
        siguiente= actual.siguiente
        while siguiente.siguiente!= None:
            actual=actual.siguiente
            siguiente=siguiente.siguiente
        actual.siguiente= None
        self.size=self.size-1
    
    def delatePos(self, pos):
        nodoActual=self.head
        contadorPos=0
        NodoAnterior= None
        while(nodoActual.siguiente!= None) and (contadorPos<pos):
            contadorPos=contadorPos+1
            NodoAnterior=nodoActual
            nodoActual= nodoActual.siguiente
        NodoAnterior.siguiente= nodoActual.siguiente
        self.size=self.size-1
                
    def Size(self):
        return self.size         

L= LinkedList()
L.add(1)
L.add(2)
L.add(3)
L.add_first(10)
L.add_first(50)
L.add_pos(12, 2)
print(L.Size())
for i in range(L.Size()):
    print(L.get(i))