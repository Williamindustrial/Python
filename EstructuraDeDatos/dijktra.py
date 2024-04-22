# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:59:19 2024

@author: lizbe
"""

from queue import LifoQueue

class node:
    
    def __init__(self,dato):
        self.dato=dato
        self.vecinos={}
        self.Selecionado=False
        self.Etiqueta= float("inf")
        self.anterior=None
    
    def addVecinos(self, node, distancia,inversion= True):
        self.vecinos[node]=distancia
        if(inversion):
            node.addVecinos(self, distancia, False)
    

Q =node("Q")
W=node("W")
R=node("R")
M=node("M")
A=node("A")
Z=node("Z")

# Relaciones
Q.addVecinos(R,5)
Q.addVecinos(W,4)
W.addVecinos(M,3)
R.addVecinos(Z,8)
R.addVecinos(M,3)
R.addVecinos(A,2)
M.addVecinos(Z,6)
A.addVecinos(Z,5)

def dijkstra(inicio, fin):
    inicio.Etiqueta=0
    Listaposibilidades=[]
    Listaposibilidades.append(inicio)
    while(len(Listaposibilidades)>0):
        menorEtiqueta=float("inf")
        nodoActual=None
        for nodo in Listaposibilidades:
            if(nodo.Etiqueta<menorEtiqueta):
                menorEtiqueta=nodo.Etiqueta
                nodoActual=nodo
        nodoActual.Selecionado=True
        Listaposibilidades.remove(nodoActual)
        for vecino in nodoActual.vecinos:
            if(vecino.Selecionado==False):
               Listaposibilidades.append(vecino)
               etiquetaNueva= nodoActual.Etiqueta+vecino.vecinos[nodoActual]
               if(etiquetaNueva<vecino.Etiqueta):
                   vecino.Etiqueta=etiquetaNueva
                   vecino.anterior=nodoActual
    actual=fin
    while(actual!=None):
        print(actual.dato)
        actual= actual.anterior
dijkstra(W, Z)


        
                   
        
        
               
    
    
    
    
    
    
    
    
    