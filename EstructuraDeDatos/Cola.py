# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 16:24:25 2024

@author: lizbe
"""

class nodo:
    def __init__(self, dato):
        self.anterior=None
        self.siguiente=None
        self.dato=dato

class queue():
    def __init__(self):
        self.Inicio=None
        self.Final= None
        self.size=0
    
    def Enqueue(self, dato):
        Nodo= nodo(dato)
        if(self.Inicio== None):
            self.Inicio=Nodo
            self.Final= Nodo
            self.size=self.size+1
        else:
            self.Final.siguiente=Nodo
            Nodo.anterior=self.Final
            self.Final= Nodo
            self.size=self.size+1
    def Dequeue(self):
        if(self.Inicio== None):
            print("La cola esta vacía")
        else:
            self.Inicio= self.Inicio.siguiente
            if(self.Inicio!=None):
                self.Inicio.anterior=None
            self.size=self.size-1
    def Peek(self):
        if(self.Inicio== None):
            return "La cola esta vacía"
        else:
            return self.Inicio.dato
    def Empty(self):
        if(self.size==0):
            return  True
        else:
            return False
    def Size(self):
        return self.size

cola=queue()   
  
cola.Enqueue(1)
cola.Enqueue(2)
cola.Enqueue(3)
print("A", cola.Peek())
cola.Dequeue()  
print("B", cola.Peek())
print("Size" , str(cola.Size()))
cola.Dequeue()  
print("C", cola.Peek())
print("Size" , str(cola.Size()))
cola.Dequeue()  
print("D", cola.Peek())
print("Size" , str(cola.Size()))
print("E", cola.Peek())
print("Size" , str(cola.Size()))
 
        
        