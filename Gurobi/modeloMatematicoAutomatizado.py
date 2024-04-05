# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 11:58:28 2023

@author: PC
"""

import  matplotlib.pyplot as plt  
import  numpy as npi
import math
from gurobipy import *
import os
import errno
from time import time
import matplotlib.pyplot as plt
import numpy as np
import random

direccionFJS=r"C:\Users\PC\OneDrive - Universidad de la Sabana\mantenimiento\Instances FJS"
direccionST= r"C:\Users\PC\Desktop\Nueva carpeta (2)"
direccionSol=r"C:\Users\PC\Desktop\Nueva carpeta (3)"
def solucionarProblema(instance: str):
    direccionGuardarSol=direccionSol+"/"+instance
    direccion= direccionFJS+"/"+instance
    #direccion="/Users\Asus\Dropbox\Instancias\edata\ela02.fjs"
    instanciaFJS = open(direccion)
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
    
    
    direccion2=direccionST+"/"+instance
    instanciaSetup = open(direccion2)
    contadorMaquinas=-1
    contadorLineas=0
    setup={}
    start={}
    setupM={}
    frecuencia={}
    duracion={}
    for  linea in instanciaSetup:
        line= linea.split()
        if(contadorLineas==0):
            contadorMaquinas=contadorMaquinas+1
            contadorLineas=contadorLineas+1
            frecuencia[contadorMaquinas]=int(line[0])
            duracion[contadorMaquinas]=int(line[1])
            
        else:
            if(line[0]=='-'):
                contadorLineas=0
                m=contadorMaquinas
                setup[(m,0,0)]=0
                start[(m,0)]=0
                setupM[(m,0)]=0
            else:
                m=contadorMaquinas
                i=contadorLineas
                if(i<numeroPedidos+1):
                    setupM[(m,i)]= int(line[numeroPedidos])
                for j in range(numeroPedidos):
                    if(contadorLineas<=numeroPedidos):
                        setup[m,i,j+1]=int(line[j])
                    else:
                        start[(m,j+1)]=int(line[j])
                contadorLineas=contadorLineas+1
    
    print(setup)
    
    
    model = Model('FJSP')
    # Variables
    x= model.addVars(arcos, vtype= GRB.BINARY, name='x')
    xm= model.addVars(arcos, vtype= GRB.BINARY, name='xm')
    sk= model.addVars([k for k in maquinas],vtype=GRB.INTEGER, name='sk')
    P=model.addVars([(i,j) for i,j in TPA],vtype= GRB.INTEGER, name='P')
    SM=model.addVars([(i,j,k) for i,j in TPA for k in maquinas],vtype= GRB.BINARY, name='Sm')
    IT=model.addVars([(i,j) for i,j in TPA],vtype= GRB.CONTINUOUS, name='IT')
    TM=model.addVars([(m,i,j) for m in maquinas for i,j in TPA], name= 'TM')
    TA=model.addVars([(m,i,j) for m in maquinas for i,j in TPA], name= 'TA')
    BM=model.addVars([(i,j)  for i,j in TPA], name= 'BM')
    ST=model.addVars([(m,i,j) for m in maquinas for i,j in TPA], name= 'TA')
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
    
    #model.addConstrs((x[m,i,j,k,l]==1) >>(TM[m,k,l]>=TM[m,i,j] +P[i,j]+setup[m,i,k]) for m in maquinas for i,j in TPA for k,l in TPA if(k,l)!=(0,0))
    model.addConstrs((x[m,i,j,k,l]==1) >>(TM[m,i,j]>=IT[i,j]) for m in maquinas for i,j in TPA for k,l in TPA)
    model.addConstrs((x[m,i,j,k,l]==1) >>(IT[i,j]>=TM[m,i,j]) for m in maquinas for i,j in TPA for k,l in TPA)
    
    Ci=model.addVars([(i) for i in range(numeroPedidos)],vtype=GRB.INTEGER)
    model.addConstrs(Ci[i]==IT[i+1,operacionesxpedido[i]]+P[i+1,operacionesxpedido[i]] for i in range(numeroPedidos))
    model.addConstrs(ym>=IT[i+1,operacionesxpedido[i]]+P[i+1,operacionesxpedido[i]]for i in range(numeroPedidos))
    
    model.addConstrs((xm[m,i,j,k,l]==1)>>(x[m,i,j,k,l]==1) for m in maquinas for i,j in TPA for k,l in TPA)
    model.addConstrs(TA[m,k,l]>= TA[m,i,j] +P[k,l]-100000*(1-x[m,i,j,k,l]) -100000*(xm[m,i,j,k,l]) for m in maquinas for i,j in TPA for k,l in TPA)
    model.addConstrs(TA[m,i,j]<=frecuencia[m]   for i,j in TPA for m in maquinas)
    
    model.addConstrs((xm[m,i,j,k,l]==1)>>(TM[m,k,l]>=TM[m,i,j] +P[i,j]+setupM[m,i]+duracion[m]+start[m,k]) for m in maquinas for i,j in TPA for k,l in TPA if(i,j)!=(0,0))
    #model.addConstrs((xm[m,i,j,k,l]==1)>>(TM[m,k,l]>=TM[m,i,j] +P[i,j]+setupM[m,i]+duracion[m]+start[m,k] ) for m in maquinas for i,j in TPA for k,l in TPA if(i,j)!=(0,0))
    
    model.addConstrs(TM[m,k,l]>=TM[m,i,j] +P[i,j] +setup[m,i,k] -100000*(1-x[m,i,j,k,l]) for m in maquinas for i,j in TPA for k,l in TPA if(i,j)!=(0,0) and (k,l)!=(0,0) )
    
    model.addConstrs(TM[m,k,l]>=start[m,k] -100000*(1-x[m,0,0,k,l]) for m in maquinas  for k,l in TPA)
    
    
    model.addConstrs((xm[m,i,j,k,l]==1)>>(TA[m,k,l]>=P[k,l]) for m in maquinas for i,j in TPA for k,l in TPA)
    
    model.setObjective(ym,GRB.MINIMIZE)
    
    
    start_time = time()
    model.Params.timeLimit=3600*3
    model.optimize()
    elapsed_time = time() - start_time
    creardirectorio(direccionGuardarSol)
    model.write(direccionGuardarSol+'\solution.lp')
    model.write(direccionGuardarSol+'\solution.json')
    #escribir(model,direccionGuardarSol,elapsed_time,x,maquinas,TPA,IT,P,rutas,ITV,ubicaciones,xv,Distancia)
    Gap=model.MIPGap
    if(Gap<100):
        model.write(direccionGuardarSol+'\solution.sol')
        escribir(model, direccionGuardarSol, elapsed_time, maquinas, x, xm, P, IT, setupM, setup, duracion, start,TPA)
        graficar(model, direccionGuardarSol, elapsed_time, maquinas, x, xm, P, IT, setupM, setup, duracion, start, TPA,ym,instance,numeroPedidos)
def creardirectorio(direccionGuardarSol):
        try:
            os.mkdir(direccionGuardarSol)
        except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                    
def escribir(model,direccionGuardarSol,elapsed_time,maquinas,x,xm,P,IT,setupM,setup,duracion,start,TPA):
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
    Gap=model.MIPGap
    if(Gap<100):
        for m in maquinas:
            Linea='Machine: '+str(m+1)+'>>-'
            initial = (0,0)
            follow=(0,0)
            Continuar=True
            while(Continuar):
                initial=follow
                for k,l in TPA:
                    i=initial[0]
                    j=initial[1]
                    a=False
                    if (x[m,i,j,k,l].x>0.99):
                        if(xm[m,i,j,k,l].x>0.99 and k>0):
                            a=True
                        if (i>0):
                            final=abs(P[i,j].x)
                            Linea=Linea +'('+str(i)+'-'+str(j)+')'
                            if(k==0):
                                Linea=Linea+ '('+str(round(IT[i,j].x))+'-'+str(round(IT[i,j].x+final))+')'
                            else:
                                Linea=Linea+ '('+str(round(IT[i,j].x))+'-'+str(round(IT[i,j].x+final))+')-'
                            if(i!=0):
                                if(a):
                                    Linea=Linea+'(S)('+str(setupM[m,i])+ ')-(M)('+str(round(duracion[m]))+')-(S)('+str(start[m,k])+')'
                                else:
                                    if(k!=0):
                                        Linea=Linea+'(S)('+str(setup[m,i,k])+ ')'
                            else:
                                Linea=Linea+'(S)('+str(start[m,k])+')'
                        else:
                            Linea=Linea+'(S)('+str(start[m,k])+')'
                        follow=(k,l)
                        
                if(follow==(0,0)):
                    Continuar=False
            file.write(Linea+"\n")
def listCadena(model,direccionGuardarSol,elapsed_time,maquinas,x,xm,P,IT,setupM,setup,duracion,start,TPA):
    ListaCadena=[]
    for m in maquinas:
        Linea='Machine: '+str(m+1)+'>>'
        initial = (0,0)
        follow=(0,0)
        Continuar=True
        while(Continuar):
            initial=follow
            for k,l in TPA:
                i=initial[0]
                j=initial[1]
                a=False
                if (x[m,i,j,k,l].x>0.99):
                    if(xm[m,i,j,k,l].x>0.99 and k>0):
                        a=True
                    if (i>0):
                        final=abs(P[i,j].x)
                        Linea=Linea +'-('+str(i)+'-'+str(j)+')'
                        if(k==0):
                            Linea=Linea+ '('+str(round(IT[i,j].x))+'-'+str(round(IT[i,j].x+final))+')'
                        else:
                            Linea=Linea+ '('+str(round(IT[i,j].x))+'-'+str(round(IT[i,j].x+final))+')'
                        if(i!=0):
                            if(a):
                                Linea=Linea+'-(S-'+str(i)+'-M'+')('+str(round(IT[i,j].x+abs(P[i,j].x)))+'-'+str(round(IT[i,j].x+abs(P[i,j].x)+setupM[m,i]))+ ')-(M-'+str(i)+'-'+str(j)+')('+str(round(IT[i,j].x+abs(P[i,j].x)+setupM[m,i]))+'-'+str(round(IT[i,j].x+abs(P[i,j].x)+setupM[m,i]+duracion[m]))+')-(S-M-'+str(k)+')('+str(round(IT[i,j].x+abs(P[i,j].x)+setupM[m,i]+duracion[m]))+'-'+str(round(IT[i,j].x+abs(P[i,j].x)+setupM[m,i]+duracion[m]+start[m,k]))+')'
                            else:
                                if(k!=0):
                                    Linea=Linea+'-(S-'+str(i)+'-'+str(k)+')('+str(round(IT[i,j].x+abs(P[i,j].x)))+'-'+str(round(IT[i,j].x+abs(P[i,j].x)+setup[m,i,k]))+ ')'
                        else:
                            Linea=Linea+'-(S-'+str(i)+'-'+str(k)+')('+str(start[m,k])+')'
                    else:
                        Linea=Linea+'-(S-0-'+str(k)+')('+str(0)+'-'+str(start[m,k])+')'
                    follow=(k,l)
            if(follow==(0,0)):
                Continuar=False
        ListaCadena.append(Linea)
    return ListaCadena

def crear_gantt(maquinas, ht):
    # Parámetros:
    hbar = 10
    tticks = 10
    nmaq = len(maquinas)
  
    plt.figure(figsize=(19,10))
    # Creación de los objetos del plot:
    fig, gantt = plt.subplots()
    

    # Diccionario con parámetros:
    diagrama = {
        "fig": fig,
        "ax": gantt,
        "hbar": hbar,
        "tticks": tticks,
        "maquinas": maquinas,
        "ht": ht
    }
    size=nmaq
    fig.set_figheight(size*2)
    fig.set_figwidth(size*3)

    # Etiquetas de los ejes:
    gantt.set_xlabel("Time",fontsize=15)
    gantt.set_ylabel("Resources",fontsize=15)

    # Límites de los ejes:
    gantt.set_xlim(0, ht)
    gantt.set_ylim(0, nmaq*hbar)

    # Divisiones del eje de tiempo:
    gantt.set_xticks(range(0, ht, 10), minor=True)
    #gantt.grid(True, axis='x')

    # Divisiones del eje de máquinas:
    gantt.set_yticks(range(hbar, nmaq*hbar, hbar), minor=True)
    #gantt.grid(True, axis='y', which='minor')

    # Etiquetas de máquinas:
    gantt.set_yticks(np.arange(hbar/2, hbar*nmaq - hbar/2 + hbar,
                            hbar))
    vc=[]
    for i in maquinas:
        if(i[0]=='M'):
            a=i.replace("M","")
            st='$M_{'+str(a)+'}$'
            vc.append(st)
        elif(i[0]=='P'):
            a=i.replace("P","")
            st='$J_{'+str(a)+'}$'
            vc.append(st)
        else:
            a=i.replace("V","")
            st='$V_{'+str(a)+'}$'
            vc.append(st)
    gantt.set_yticklabels(vc)

    return diagrama

# Función para armar tareas:
def agregar_tarea(diagrama, t0, d, maq, nombre, color, lb):
    maquinas = diagrama["maquinas"]
    hbar = diagrama["hbar"]
    gantt = diagrama["ax"]
    ht = diagrama["ht"]

    # Chequeos:
    assert t0 + d <= ht, "La tarea debe ser menor al horizonte temporal."
    assert t0 >= 0, "El t0 no puede ser negativo."
    assert d >= 0, "La duración d debe ser positiva."

    # Color:
    if color == None:
        #color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        color= selectcolor()

    # Índice de la máquina:
    imaq = maquinas.index(maq)
    # Posición de la barra:
    gantt.broken_barh([(t0, d)], (hbar*imaq+hbar/4-0.5, hbar/2+1),
                      facecolors=(color), label=lb)
    # Posición del texto:
    if(d<120):
      gantt.text(x=(t0 + d/2), y=(hbar*imaq + hbar/2),
                    s=f"{nombre}({t0}-{t0+d})", va='center', ha='center', color='Black',size=5,rotation=90)
      #gantt.text(x=(t0 + d/2 +15), y=(hbar*imaq + hbar/2),
           #         s=f"({t0}-{t0+d})", va='center', ha='center', color='Black',size=16,rotation=90)
    else:
      gantt.text(x=(t0 + d/2), y=(hbar*imaq + hbar/2),
                    s=f"{nombre}({t0}-{t0+d})", va='center', ha='center', color='Black',size=5,rotation=90)
      #gantt.text(x=(t0 + d/2), y=(hbar*imaq + hbar/2-1.5),
                   # s=f"({t0}-{t0+d})", va='center', ha='center', color='Black',size=16)
    #lg=plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left',fontsize=50)
        

def mostrar(instance):
    lg=plt.legend(bbox_to_anchor=(1, 1), loc='upper left',fontsize=7)
    plt.xticks(fontsize= 12)
    plt.yticks(fontsize=12)
    plt.savefig(direccionSol+'/'+instance+'/gannt.pdf', dpi=2000, 
                bbox_inches='tight')
    plt.show()    


def cadenaCaracteres(cadena, Machine,operations):
    print(cadena)
    cadena=cadena.replace(">>",")")
    ca=cadena.split(')-(')
    subMachine=ca[0].split(': ')
    for i in range(1,len(ca)):
        a=ca[i]
        b=a.split(')(')
        b[1]=b[1].replace(",00","")
        b[1]=b[1].replace("-",",")
        final=[]
        final.append(b[0])
        tiempos=b[1].split(',')
        if(tiempos[0]==''):
            tiempos[0]=0
        operations[b[0]+','+str(i)+str(Machine)]={'Machine':'M'+str(Machine),'Start':int(tiempos[0]),'End': int(tiempos[1].replace(")",""))}
    return str(Machine)

def graficar(model,direccionGuardarSol,elapsed_time,maquinas,x,xm,P,IT,setupM,setup,duracion,start,TPA,ym,intance,numeroPedidos):
    machines = []
    ht=int(ym.x)+10
    cm=1
    operations={}
    #operations['M-0,'+str(0)+str(0)]={'Machine':'M'+str(0),'Start':int(0),'End': int(1)}
    #operations['S-0,'+str(0)+str(0)]={'Machine':'M'+str(0),'Start':int(0),'End': int(1)}
    #for i in range(numeroPedidos):
     #   operations[str(i+1)+'-0,'+str(0)+str(0)]={'Machine':'M'+str(0),'Start':int(0),'End': int(0)}
    ListaCadena= listCadena(model,direccionGuardarSol,elapsed_time,maquinas,x,xm,P,IT,setupM,setup,duracion,start,TPA)
    for cadena in ListaCadena:
        machines.append('M'+cadenaCaracteres(cadena,Machine=cm,operations=operations))
        cm=cm+1
    diagrama= crear_gantt(maquinas=machines,ht=ht)
    color={'1':'r','2':'#DC143C','3':'#00FFFF','4':'#00008B','5':'#008B8B','6':'#B8860B','7':'#006400','8':'#8B008B','9':'#FF8C00','10':'#FFD700','11':'#ADFF2F','S':'#FFFF00','M':'#8B008B'}
    valoresB={'1':False,'2':False,'3':False,'4':False,'5':False,'6':False,'7':False,'8':False,'9':False,'10':False,'11':False,'S':False,'M':False}
    key= sorted(operations.keys())
    for k in key:
        operation= k
        a=operation.split('-')[0]
        op=operations.get(operation)
        label='_'+a
        if(valoresB[a]==False):
            label=a
            if(label!='S' and label!='M'):
                label='$J_'+str(a)+'$'
            elif (label!='S'):
                label='$Maint$'
            else:
                label='$Setup$'
            valoresB[a]=True
            
        name=operation.split(',')[0]
        if(operation.split(',')[0].split('-')[0]=='M' or operation.split(',')[0].split('-')[0]=='S'):
            name=''
            if(operation=='S-M-1,13'):
                print(op['End']-op['Start'])
                print(op['Machine'])
                
                agregar_tarea(diagrama,op['Start'], op['End']-op['Start'], op['Machine'], name,'r',label)
        else: 
            name='('+name.split('-')[1]+')'
        if(op['End']-op['Start']>0):
            agregar_tarea(diagrama,op['Start'], op['End']-op['Start'], op['Machine'], name,color[a],label)
    mostrar(instance=intance)
    
def leerCarpeta():
    contenido = os.listdir(direccionFJS)
    for i in range(16,len(contenido)):
        instancia= contenido[i]
        solucionarProblema(instancia)
#leerCarpeta()
#
solucionarProblema("Sfjs110.txt")