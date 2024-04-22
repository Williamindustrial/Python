# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:24:29 2024

@author: lizbe
"""

from queue import LifoQueue

class node:
    
    def __init__(self,dato):
        self.dato=dato
        self.anteriores={}
        self.siguientes={}
        self.Entrada=0
        self.Salida=0
    
    
    def setSiguiente(self, node, flujo):
        self.siguientes[node]  ={ "Nodo": node.dato, "capacidad":flujo, "usado":0}
        node.setAnteriores(self, flujo)
    
    def setAnteriores(self, node, flujo):
        self.anteriores[node]  ={"Nodo":node.dato,  "capacidad":flujo, "usado":0}
    
        
O=node(("0"))
A=node("A")
B=node("B")
C=node("C")
D=node("D")
E=node("E")
F=node("F")
T=node("T")

O.setSiguiente(A, 8)
O.setSiguiente(B, 5)
A.setSiguiente(C, 4)
A.setSiguiente(D, 5)
B.setSiguiente(E, 4)
C.setSiguiente(F, 2)
C.setSiguiente(B, 3)
C.setSiguiente(E, 6)
D.setSiguiente(T, 6)
E.setSiguiente(F, 3)
E.setSiguiente(T, 6)
F.setSiguiente(T, 4)


def buscarMayorRuta(nodoInicio, nodoFin):
    nodoActual=nodoInicio
    maxFlujo=float("inf")
    Ruta= []
    while(nodoActual!=nodoFin):
        Ruta.append(nodoActual)
        maxArista=0
        nodoMaxSiguiente=None
        for nodoVecino in nodoActual.siguientes:
            if(maxArista<nodoActual.siguientes[nodoVecino]["capacidad"] and nodoActual.siguientes[nodoVecino]["capacidad"]>0):
                maxArista=nodoActual.siguientes[nodoVecino]["capacidad"]
                nodoMaxSiguiente=nodoVecino
                
        if(nodoMaxSiguiente==None and nodoActual!= nodoFin):
            return (None,None)
        else:
            nodoActual=nodoMaxSiguiente
            if(nodoActual==nodoFin):
                Ruta.append(nodoFin)
            if(maxArista<maxFlujo):
                maxFlujo=maxArista
    return (Ruta,maxFlujo)
            

def descotarFlujo(source, sink):
    Terminar=False
    while(Terminar==False):
        print("-------------------")
        Ruta, FlujoOcupado =buscarMayorRuta(source, sink)
        if(Ruta==None):
            Terminar=True
        else:
            while(Ruta[0]!=sink):
                NodoActual= Ruta.pop(0)
                Nodosiguiente=Ruta[0]
                print(NodoActual.dato)
                NodoActual.siguientes[Nodosiguiente]["capacidad"]=NodoActual.siguientes[Nodosiguiente]["capacidad"]-FlujoOcupado
                NodoActual.siguientes[Nodosiguiente]["usado"]=NodoActual.siguientes[Nodosiguiente]["usado"]+FlujoOcupado
                
                Nodosiguiente.anteriores[NodoActual]["capacidad"]=Nodosiguiente.anteriores[NodoActual]["capacidad"]-FlujoOcupado
                Nodosiguiente.anteriores[NodoActual]["usado"]=Nodosiguiente.anteriores[NodoActual]["usado"]+FlujoOcupado
            print(Nodosiguiente.dato)
                
Ruta=descotarFlujo(O, T)

        
        
        



