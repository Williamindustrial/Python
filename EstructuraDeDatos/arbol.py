# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:38:40 2024

@author: lizbe
"""

class node:
    def __init__(self, key):
        self.key=key
        self.right=None
        self.left=None
        self.root=None

class tree():
    
    def __init__(self):
        self.root=None
        self.size=0
    
    def add(self, key, raiz=None):
        if(self.root==None):
            self.root= node(key)
        else: 
            if(raiz==None):
                raiz= self.root
            if(key<raiz.key):
                if(raiz.left==None):
                    nodeA=node(key)
                    nodeA.root=raiz
                    raiz.left= nodeA
                    
                else:
                    self.add(key,raiz.left)
            else: 
                if(raiz.right==None):
                    nodeA=node(key)
                    nodeA.root=raiz
                    raiz.right=nodeA
                else: 
                    self.add(key, raiz.right)
        self.size=self.size+1
                    
    def search(self, key, raiz=None):
        if(raiz==None):
            raiz=self.root
        if(key==raiz.key):
            return raiz
        else:
            if( key<raiz.key):
                return self.search(key, raiz.left)
            else:
                return self.search(key, raiz.right)
            
    
    def delate(self, key):
        nodeA=self.search(key)
        if(nodeA.left==None and nodeA.right==None):
            self.delateleaf(key, nodeA)
        elif (nodeA.left!=None or nodeA.right!=None):
            if(nodeA.left!=None and nodeA.right!=None):
                self.delateTwoSon(key, nodeA)
            else:
                self.delateUniqueSon(key, nodeA)
        self.size=self.size-1
            
    
    def delateleaf(self, key, nodeA):
        root= nodeA.root
        if(root.left!=None):
            if(root.left.key==key):
                root.left=None
        if(root.right!=None):
            if(root.right.key==key):
                root.right=None
            
    
    def delateUniqueSon(self, key, nodeA):
        root= nodeA.root
        if(root.left.key==key):
            if(nodeA.left!=None):
                root.left= nodeA.left
            else:
                root.left= nodeA.right
        elif(root.right.key==key):
            if(nodeA.left!=None):
                root.right= nodeA.left
            else:
                root.right= nodeA.right
    
    def delateTwoSon(self, key, NodeA):
        nodoB= self.searchless(NodeA)
        flag=False
        if(NodeA.root==None):
            flag=True
        else:
            pA=NodeA.root
        nodoB.left=NodeA.left
        nodoB.right=NodeA.right
        if(flag==False):
            if(pA.left.key==key):
                pA.left=nodoB
            elif(pA.right.key==key):
                pA.right=nodoB
            self.delateleaf(nodoB.key, nodoB)
        else:
            self.root=nodoB
            self.delateleaf(nodoB.key, nodoB)
        
                
    def searchless(self, nodeInitial):
        LbranchRight= nodeInitial.right
        while(LbranchRight.left!=None):
            LbranchRight= LbranchRight.left
        return LbranchRight
            
    
    def inOrder(self, root=None, lista=None):
        if(root==None):
            current=self.root
            lista=[]
        else:
            current=root
        if(current.left!=None):
            self.inOrder(current.left,lista)
        lista.append(current.key)
        if(current.right!=None):
            self.inOrder(current.right,lista)
        return lista
    
    
    def posOrden(self, root=None, lista=None):
        if(root==None):
            current=self.root
            lista=[]
        else:
            current=root
        if(current.left!=None):
            self.posOrden(current.left,lista)
        if(current.right!=None):
            self.posOrden(current.right,lista)
        lista.append(current.key)
        
        return lista
    
    
    def preOrden(self, current=None, lista=None):
        if(current==None):
            current= self.root
            lista=[]
        lista.append(current.key)
        print(current.key)
        if(current.left!=None):
            self.preOrden(current.left,lista)
        if(current.right!=None):
            self.preOrden(current.right,lista)
        return lista
        
                
                    
                    
tr=  tree()
tr.add(10)
tr.add(5)
tr.add(12)
tr.add(11)
tr.add(15)
tr.add(3)
tr.add(7)
tr.add(6)



preorden=tr.preOrden()
inorden= tr.inOrder()
posorder= tr.posOrden()

tr.delate(5)

preorden1=tr.preOrden()
inorden1= tr.inOrder()
posorder1= tr.posOrden()



        