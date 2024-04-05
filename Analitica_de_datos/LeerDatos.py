# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 07:47:02 2022

@author: Asus
"""

import os
direccion= '/Users\Pc\Desktop\MATH MODEL 1.1\SIMH\SIMH/'
contenidoCarpeta= os.listdir(direccion)

instancias={}
for conCarpeta1 in contenidoCarpeta: 
    replica={}
    for i in range(300):
        direccion2=direccion+str(conCarpeta1)+'/'+str(i+1)+'/'
        contenidoCarpeta2= os.listdir(direccion2)
        print(conCarpeta1)
        rutas={}
        for conCarpeta2 in contenidoCarpeta2: 
            nombrearchivo= conCarpeta2.split(".")
            if(nombrearchivo[0]=='Routes'):
                ruta={}
                print(conCarpeta2)
                direccion3=direccion2+'/'+conCarpeta2
                resultado= open(direccion3)
                contador =0
                for  line in resultado:
                    if(contador<2):
                        numero= line.split(" ")
                        print(numero[-1])
                        if(contador==0):
                            final= float(numero[-1].split(",")[0])
                            ruta['CRI']=final
                        if(contador==1):
                            final= float(numero[-1])
                            ruta['CPU-TIME']=final
                    contador=contador+1
                rutas[conCarpeta2.split('.')[0]]= ruta
            if(conCarpeta2=='Best.txt'):
                ruta={}
                direccion3=direccion2+'/'+conCarpeta2
                resultado= open(direccion3)
                contador =0
                for  line in resultado:
                    if(contador==1):
                        tiempo= line.split(" ")[2]
                        ruta['CPU-TIME']=float(tiempo)
                    contador=contador+1
                rutas[conCarpeta2.split('.')[0]]= ruta
        replica[i]=rutas
    instancias[conCarpeta1]= replica

#writer=pd.ExcelWriter('Reporte.xlsx')

for inst in instancias:
    replica=instancias[inst]
    for i in range(300):
        rutas=replica[i]
        CRMAX= 0
        CRIAUX=0
        for route in rutas:
            if(route=="Best"):
                CRIAUX= rutas[route]['CPU-TIME']
            else:
                CRI=rutas[route]['CRI']
                if(CRI>CRMAX):
                    CRMAX=CRI
        rutas['CRMAX']= CRMAX
        
    


for i in range(30):
    file=open('/Users\Pc\Desktop\MATH MODEL 1.1\SIMH/'+"ruta"+str(i+1)+".csv",'w')
    for instancia in  instancias:
        inst=instancias[instancia]
        linea=''+instancia+';'
        print(instancia)
        for replica in inst:
            REPLICA=inst[replica]
            for ruta in REPLICA:
                if(ruta=="Route "+str(i+1)):
                    RUTA=REPLICA[ruta]
                    linea+=str(RUTA['CRI'])+";"
        file.write(linea)
        file.write("\n")
file.close()

file=open('/Users\Pc\Desktop\MATH MODEL 1.1\SIMH/'+"\CRMAX2.csv",'w')
for instancia in  instancias:
    inst=instancias[instancia]
    linea=''+instancia+';'
    print(instancia)
    for replica in inst:
        Rep=inst[replica]
        linea+=str(Rep['CRMAX'])+";"
    file.write(linea)
    file.write("\n")
file.close()

