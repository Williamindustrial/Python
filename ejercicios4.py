# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 07:50:44 2024

@author: lizbe
"""



def fibonacci(n):
    if n <= 1:
        return n
    else:
        # Calculamos fibonacci(n-1) y fibonacci(n-2)
        fibonacci_n_minus_1 = fibonacci(n - 1)
        fibonacci_n_minus_2 = fibonacci(n - 2)
        
        # Sumamos los resultados
        resultado = fibonacci_n_minus_1 + fibonacci_n_minus_2
        
        # Mostramos los resultados intermedios
        print("----------------", n)
        print(f"Fibonacci({n-1}) = {fibonacci_n_minus_1}")
        print(f"Fibonacci({n-2}) = {fibonacci_n_minus_2}")
        print(f"Fibonacci({n}) = {resultado}")
        
        return resultado

# Calculamos fibonacci(5)
#resultado = fibonacci(6)
#print("El término 5 de la secuencia de Fibonacci es:", resultado)

def factorial(n):
    if(n<=1):
        return n
    else: 
        print("----------------", n)
        fac= n*factorial(n-1)
        return fac
        
print(factorial(4))


def sumaDigitos(n):
    if(n<10):
        return n
    else:
        ultimoDigito= n%10
        SinUltimoDigito= n//10
        suma= sumaDigitos(SinUltimoDigito)+ultimoDigito
        return suma
print(sumaDigitos(152))

def conteoRegresivo(n):
    if(n<=1):
        return n
    else:
        print(n)
        anterior= conteoRegresivo(n-1)
        return anterior

print(conteoRegresivo(13))

def invertirCadena(cadena):
    if(len(cadena)<=1):
        return cadena
    else:
        return cadena[-1]+invertirCadena(cadena[:-1])
print(invertirCadena("Hola mundo"))

def recorridoLista(lista):
    if(len(lista)<=1):
        return lista[0]
    else:
        return lista[0]+recorridoLista(lista[1:])
print(recorridoLista([1,2,3,4]))

def insertion_sort(Lista):
    ListaOrdenada=[]
    for i in range(len(Lista)):
        actual=Lista[i]
        ListaOrdenada.append(actual)
        if(i>0):
            j=len(ListaOrdenada)-2
            while(ListaOrdenada[j]>actual and j>=0):
                ListaOrdenada[j+1]=ListaOrdenada[j] 
                ListaOrdenada[j]=actual
                j=j-1
    return ListaOrdenada

print(insertion_sort([12,5,7,1,9]))

def bubble_sort(Lista):
    for i in range(len(Lista)):
        for j in range(0,len(Lista)-i-1):
            if(Lista[j]>Lista[j+1]):
                mayor=Lista[j]
                Lista[j]=Lista[j+1]
                Lista[j+1]=mayor
    return Lista

def selection_sort(Lista):
    for i in range(len(Lista)):
        menorIndex=i
        for j in range(i,len(Lista)):
            if(Lista[j]< Lista[menorIndex]):
                menorIndex=j
        menor= Lista[menorIndex]
        Lista[menorIndex]=Lista[i]
        Lista[i]=menor
    return Lista

print(bubble_sort([12,5,7,1,1,9]))
print(selection_sort([12,5,7,1,12,9]))
            
        
        
        
        
        
        
        
        