# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 17:52:44 2024

@author: lizbe
"""

class nodo:
    def __init__(self, dato):
        self.dato=dato
        self.siguiente=None

class Pila:
    def __init__(self):
        self.top=None
        self.size=0
        
    def Push(self,dato):
        Nodo= nodo(dato)
        if(self.top==None):
            self.top= Nodo
        else: 
            auxiliar= self.top
            self.top= Nodo
            self.top.siguiente=auxiliar
        self.size=self.size+1
            
    def pop(self):
       if(self.top==None):
           return "La pila esta vacía"
       else:
           self.top= self.top.siguiente
           self.size=self.size-1
           
    def Peek(self):
        if(self.top== None):
            return "La pila esta vacía"
        else:
            return self.top.dato
        
    def Empty(self):
        if(self.size==0):
            return  True
        else:
            return False
        
    def Size(self):
        return self.size
           
P = Pila()
P.Push(1)    
P.Push(2)  
P.Push(3)    
P.pop()