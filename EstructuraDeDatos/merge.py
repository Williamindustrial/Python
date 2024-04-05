# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:43:13 2024

@author: lizbe
"""

def merge_sort(lista):
    # Verificamos si la lista tiene más de un elemento
    if len(lista) > 1:
        # Dividimos la lista en mitades
        mitad = len(lista) // 2
        mitad_izquierda = lista[:mitad]
        mitad_derecha = lista[mitad:]

        # Llamada recursiva para ordenar las mitades
        merge_sort(mitad_izquierda)
        merge_sort(mitad_derecha)
        
        print("List",lista)
        print("IZ",mitad_izquierda)
        print("DER",mitad_derecha)
        # Fusionamos las mitades ordenadas
        i = j = k = 0
        while i < len(mitad_izquierda) and j < len(mitad_derecha):
            if mitad_izquierda[i] < mitad_derecha[j]:
                lista[k] = mitad_izquierda[i]
                i += 1
            else:
                lista[k] = mitad_derecha[j]
                j += 1
            k += 1

        # Completamos la fusión si quedan elementos en una de las mitades
        while i < len(mitad_izquierda):
            lista[k] = mitad_izquierda[i]
            i += 1
            k += 1

        while j < len(mitad_derecha):
            lista[k] = mitad_derecha[j]
            j += 1
            k += 1
        print(lista)
# Ejemplo de uso
lista = [12, 5, 7, 1, 9]
merge_sort(lista)
print("Lista ordenada:", lista)