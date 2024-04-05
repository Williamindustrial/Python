# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:30:07 2024

@author: lizbe
"""

def ordenamentoBinario(lista:list, numero:int, inicio:int=0):
    if(len(lista)<=1 ):
        if(numero==lista[0]):
            return inicio
        else:
            return None
    else:
        posMedioA=len(lista)//2
        if(numero<lista[posMedioA]):
            return ordenamentoBinario(lista[:posMedioA], numero, inicio)
        else:
            return ordenamentoBinario(lista[posMedioA:], numero, posMedioA+inicio)

print(ordenamentoBinario([1,2,3,5,8,15,18,54],3))

