# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:43:54 2024

@author: lizbe
"""
import timeit
import matplotlib.pyplot as plt

def bucleFor(n):
    suma=n
    for i in range(n):
        n=n+i

def bucleDobleFor(n):
    suma=n
    for i in range(n):
        for j in range(n):
            n=n+i
def IF(n):
    n=10
    b=n
    if(n<10):
        b=n

def sentencia(n):
    n=10


def grafica():
    tiempos=[]
    tiempos2=[]
    y=[]
    for i in range(1000):
        n_value=i
        execution_Time = timeit.timeit(lambda: sentencia(n_value), number=100)
        execution_Time2 = timeit.timeit(lambda: bucleFor(n_value), number=100)
        tiempos.append(execution_Time)
        tiempos2.append(execution_Time2)
        y.append(i)
    plt.scatter(y, tiempos, color='blue', marker='*', label=" Condicional")
    plt.scatter(y, tiempos2, color='red', marker='*', label="For")
    plt.xlabel("n")
    plt.ylabel("Seconds")
    plt.legend()
    


if __name__ == "__main__":
    grafica()