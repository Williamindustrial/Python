# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 18:37:37 2023

@author: PC
"""

import  matplotlib.pyplot as plt  
import  numpy as npi
import math
from gurobipy import *
import os
import errno
from time import time

def leerdata(direcionFJS,direccionVRP,direccionGuardarSol,nombreInstancia,rutas):
    instanciaFJS = open(direcionFJS)
    contador=0
    contadorPedidos=0
    pedidos=[]
    maquinas=[]
    operacionesxpedido=[]
    TPA={}
    numeroPedidos=0
    numeroMaquinas=0
    for  line in instanciaFJS:
        linea= line.split()
        if(contador==0):
            numeroPedidos=int(linea[0])
            numeroMaquinas=int(linea[1])
            maquinas=range(numeroMaquinas)
            pedidos=range(1,numeroPedidos+1)
            dicInitial= {}
            for m in range(numeroMaquinas):
                dicInitial[m]=0
            TPA[(0,0)]=dicInitial
        else:
            print(linea)
            numeroOperacionesPedido= int(linea[0])
            operacionesxpedido.append(numeroOperacionesPedido)
            contadorElementoLista=1
            for operacion in range(numeroOperacionesPedido):
                Maquinas= int(linea[contadorElementoLista])
                MachinesTime={}
                for maquina in range(Maquinas):
                    maquina= int(linea[contadorElementoLista+1])-1
                    tiempo= int(linea[contadorElementoLista+2])
                    contadorElementoLista=contadorElementoLista+2
                    MachinesTime[maquina]=tiempo
                contadorElementoLista=contadorElementoLista+1
                TPA[(contadorPedidos+1,operacion+1)]= MachinesTime
            contadorPedidos= contadorPedidos+1
        contador=contador+1
    print(pedidos)
    PM={}
    TP={}
    for i,j in TPA:
        arreglo={}
        ar2={}
        for machine in maquinas:
            bol= False
            for maquina in TPA[i,j]:
                if(machine==maquina):
                    bol= True
            if(bol==True):
                arreglo[machine]=1
                ar2[machine]=TPA[i,j][machine]
            else:
                arreglo[machine]=0
                ar2[machine]=0
        PM[(i,j)]=arreglo
        TP[(i,j)]=ar2
    print(TPA)
    arcos=[(m,i,j,k,l) for m in maquinas for i,j in TPA for k,l in TPA ]
    model = Model('FJSP-CVRPRT')
    x= model.addVars(arcos, vtype= GRB.BINARY, name='x')
    sk= model.addVars([k for k in maquinas],vtype=GRB.INTEGER, name='sk')
    P=model.addVars([(i,j) for i,j in TPA],vtype= GRB.INTEGER, name='P')
    SM=model.addVars([(i,j,k) for i,j in TPA for k in maquinas],vtype= GRB.BINARY, name='Sm')
    IT=model.addVars([(i,j) for i,j in TPA],vtype= GRB.INTEGER, name='IT')
    TM=model.addVars([(m,i,j) for m in maquinas for i,j in TPA], name= 'TM')
    ym = model.addVar(vtype=GRB.INTEGER, name= 'makespan')
    
    model.addConstrs(quicksum(SM[i,j,m] for m in maquinas)==1 for i,j in TPA if i>0)
    model.addConstrs(PM[i,j][m]>= SM[i,j,m] for i,j in TPA for m in maquinas if i>0)
    
    model.addConstrs((SM[i,j,k]==1) >> (P[i,j]==TP[i,j][k]) for i, j in TP for k in maquinas)
    #model.addConstrs((P[i,j]>=TP[i,j][k]*SM[i,j,k]) for i, j in TP for k in maquinas)
    
    model.addConstrs(IT[i,j]+P[i,j]<=IT[i,j+1] for i,j in TPA if(i>0) and (j<operacionesxpedido[i-1]))
    model.addConstrs(SM[i,j,m]>=x[m,i,j,k,l]for m,i,j,k,l in arcos)
    
    
    model.addConstrs(quicksum(x[m,i,j,k,l] for k,l in TPA if(k,l)!=(i,j))==SM[i,j,m] for m in maquinas for i,j in TPA if(i>0))
    model.addConstrs(quicksum(x[m,i,j,k,l] for i,j in TPA if(k,l)!=(i,j))==SM[k,l,m] for m in maquinas for k,l in TPA if(k>0))
    
    model.addConstrs(quicksum(x[m,0,0,k,l] for k,l in TPA)==1 for m in maquinas)
    model.addConstrs(quicksum(x[m,i,j,0,0] for i,j in TPA)==1 for m in maquinas)
    
    model.addConstrs((x[m,i,j,k,l]==1) >>(TM[m,k,l]>=TM[m,i,j] +P[i,j]) for m in maquinas for i,j in TPA for k,l in TPA if(k,l)!=(0,0))
    model.addConstrs((x[m,i,j,k,l]==1) >>(TM[m,i,j]>=IT[i,j]) for m in maquinas for i,j in TPA for k,l in TPA)
    model.addConstrs((x[m,i,j,k,l]==1) >>(IT[i,j]>=TM[m,i,j]) for m in maquinas for i,j in TPA for k,l in TPA)
    
    Ci=model.addVars([(i) for i in range(numeroPedidos)],vtype=GRB.INTEGER)
    model.addConstrs(Ci[i]==IT[i+1,operacionesxpedido[i]]+P[i+1,operacionesxpedido[i]] for i in range(numeroPedidos))
    model.addConstrs(ym>=IT[i+1,operacionesxpedido[i]]+P[i+1,operacionesxpedido[i]]for i in range(numeroPedidos))
    
    instancia = open(direccionVRP)
    contador =0
    ubicaciones={}
    contadorOrder=0
    contadorProduct=0
    for  line in instancia:
        if contador >8 and contador<=(numeroPedidos+1)*5+8:
            linea= line.split()
            if(contadorProduct==5):
                contadorProduct=0
                contadorOrder=contadorOrder+1
            ubicaciones[(int(contadorOrder),int(contadorProduct))]={'x':int(linea[1]),'y':int(linea[2]), 'w':int(linea[3])}
            contadorProduct=contadorProduct+1
        contador=contador+1
    Distancia={}
    arcosVRP=[(r,i,j,k,l) for r in range(rutas) for i,j in ubicaciones for k,l in ubicaciones]
    for ubicacion in ubicaciones:
        for ubicacion2 in ubicaciones:
            if(ubicacion!=ubicacion2):
                x1=int(ubicaciones[ubicacion]['x'])
                x2=int(ubicaciones[ubicacion2]['x'])
                y1=int(ubicaciones[ubicacion]['y'])
                y2=int(ubicaciones[ubicacion2]['y'])
                Distancia[(ubicacion, ubicacion2)]= int(round(npi.hypot(x1-x2, y1-y2))*60/17)
    
    print(ubicaciones)
    ITV=model.addVars([(r) for r in range(rutas)], vtype=GRB.INTEGER)
    Bina=model.addVars([(i,j,r) for i,j in ubicaciones for r in range(rutas)], vtype=GRB.BINARY, name='B')
    U=model.addVars([(r,i,j)  for r in range(rutas) for i,j in ubicaciones], vtype=GRB.INTEGER)
    xv= model.addVars(arcosVRP, vtype= GRB.BINARY, name='xv')
    TTV=model.addVars([(r) for r in range(rutas)], vtype=GRB.INTEGER)
    CRMAX= model.addVar(vtype=GRB.INTEGER)
    model.addConstrs((Bina[i,j,r]==1)>>(ITV[r]>=Ci[i-1]) for i,j in ubicaciones for r in range(rutas)  if i>0)  
    model.addConstrs(quicksum(Bina[i,j,r] for r in range(rutas))==1 for i,j in ubicaciones if (i,j)!=(0,0))
    model.addConstrs(quicksum(xv[r,i,j,k,l] for k,l in ubicaciones if(k,l)!=(i,j))==Bina[i,j,r] for r in range (rutas) for i,j in ubicaciones if (i,j)!=(0,0))
    model.addConstrs(quicksum(xv[r,i,j,k,l] for i,j in ubicaciones if(i,j)!=(k,l))==Bina[k,l,r] for r in range (rutas) for k,l in ubicaciones if (k,l)!=(0,0))
    model.addConstrs(quicksum(xv[r,0,0,k,l] for k,l in ubicaciones)==1 for r in range (rutas))
    model.addConstrs(quicksum(xv[r,i,j,0,0] for i,j in ubicaciones)==1 for r in range (rutas))
    model.addConstrs((U[r,i,j]+1<=50*(1-xv[r,i,j,k,l])+U[r,k,l]) for r,i,j,k,l in arcosVRP if(i,j)!=(k,l) and (k,l)!=(0,0))
    model.addConstrs((TTV[r]==quicksum(Distancia[(i,j),(k,l)]*xv[r,i,j,k,l] for i,j in ubicaciones 
                                          for k,l in ubicaciones if(i,j)!=(k,l)))for r in range(rutas))
    model.addConstrs(ITV[r]==ITV[r-1]+120 for r in range(rutas) for i in ubicaciones if r>0)
    model.addConstrs(ITV[r]==0 for r in range(rutas)  if r==0)
    #model.addConstrs(ITV[r]<=ym for r in range(rutas) for i in ubicaciones )
    #model.addConstrs(ITV[r]>=Ci[i-1]+60 for r in range(rutas) if r==0)
    model.addConstrs((CRMAX>=TTV[r]+ ITV[r]*(1-xv[r,0,0,0,0])) for r in range(rutas))
    
    model.setObjective(CRMAX,GRB.MINIMIZE)
   # model.Params.Threads = 8
   # model.Params.NodefileStart = 0.5 

    start_time = time()
    model.Params.timelimit=25200
    model.optimize()
    elapsed_time = time() - start_time
    creardirectorio(direccionGuardarSol)
    model.write(direccionGuardarSol+'\solution.lp')
    model.write(direccionGuardarSol+'\solution.json')
    escribir(model,direccionGuardarSol,elapsed_time,x,maquinas,TPA,IT,P,rutas,ITV,ubicaciones,xv,Distancia)
    Gap=model.MIPGap
    if(Gap<100):
        model.write(direccionGuardarSol+'\solution.sol')
   # https://www.gurobi.com/documentation/9.5/refman/matlab_grb.html
def creardirectorio(direccionGuardarSol):
        try:
            os.mkdir(direccionGuardarSol)
        except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
def escribir(model,direccionGuardarSol,elapsed_time,x,maquinas,TPA,IT,P,rutas,ITV,ubicaciones,xv,Distancia):
    file=open(direccionGuardarSol+"\SolutionInfo.txt",'w')
    file.write("Objective function: "+ str(round(model.ObjVal,2)))
    file.write("\n")
    file.write("Final time: "+ str(round(model.ObjVal,2)))
    file.write("\n")
    file.write("CPU-Time: "+ str(elapsed_time))
    file.write("\n")
    file.write("GAP: "+ str(model.MIPGap))
    #file.write("\n")
    #file.write("Best bound: "+ str(model.objboundc))
    file.write("\n")
    file.write("Best bound: "+ str(model.objbound))
    file.write("\n")
    file.write("\n")
    file.write("Scheduling")
    file.write("\n")
    Gap=model.MIPGap
    if(Gap<100):
        for m in maquinas:
            Linea='Machine '+str(m)+':'
            initial = (0,0)
            follow=(0,0)
            Continuar=True
            while(Continuar):
                initial=follow
                for k,l in TPA:
                    i=initial[0]
                    j=initial[1]
                    if (x[m,i,j,k,l].x>0.99):
                        final=abs(IT[i,j].x+P[i,j].x)
                        if(initial!=(0,0)):
                            Linea=Linea+ '('+str(i)+'-'+str(j)+')'+'('+str(round(abs(IT[i,j].x)))+'-'+str(round(final))+') '
                        follow=(k,l)
                if(follow==(0,0)):
                    Continuar=False
            print(Linea)
            file.write(Linea+"\n")
        
        file.write("End-Scheduling")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("Routes")
        file.write("\n")
        for r in range(rutas):
            Linea='Route '+str(r)+':'
            file.write(Linea+"\n")
            initial = (0,0)
            follow=(0,0)
            Continuar=True
            tiempoVisita= ITV[r].x
            while(Continuar):
                initial=follow
                for k,l in ubicaciones:
                    i,j=initial
                    if (xv[r,i,j,k,l].x>0.99):
                        Linea=('['+str(initial)+']'+'['+str(ubicaciones[i,j]['x'])+', '+str(ubicaciones[i,j]['y'])+', '+str(tiempoVisita)+']')
                        file.write(Linea+"\n")
                        try:
                            tiempoVisita=tiempoVisita+Distancia[(i,j),(k,l)]
                        except:
                            print(0)
                        follow=(k,l)
                if(follow==(0,0)):
                    Linea=('['+str(follow)+']'+'['+str(ubicaciones[0,0]['x'])+', '+str(ubicaciones[0,0]['y'])+', '+str(tiempoVisita)+']')
                    file.write(Linea+"\n")
                    Continuar=False
    
        file.write("End-Route")
numeroR=0
def lector(direccion,direccionVRP,guardar):
    contenido = os.listdir(direccion)
    contenidoVRP=os.listdir(direccionVRP)
    LowerBound=[600,609,655,550,568,503,833,762,845,878,866,
                1087,960,1053,1123,1111,892,707,842,796,857,
                895,832,950,881,894,1089,1181,1116,1058,1147]
    
    inicio=5
    for i in range(inicio, len(contenido)):
        print(i)
        direccion1=direccion+'/'+str(contenido[i])
        direccion2=direccionVRP+'/'+str(contenidoVRP[i])
        direccion3=guardar+'/TRM'+(str(i))
        instancia='/TRM'+(str(i))
        numeroR=math.floor(LowerBound[i]/120)
        print(direccion1)
        print(direccion2)
        print(direccion3)
        leerdata(direccion1,direccion2,direccion3, instancia,10)

lector('/Users\PC\OneDrive - Universidad de la Sabana\MDGP\Combined Job-Shop and VRP\Instances example',
       '/Users\PC\OneDrive - Universidad de la Sabana\MDGP\Conference paper\solomon\SolomonIntance' ,
       '/Users\PC\Documents\exp')
