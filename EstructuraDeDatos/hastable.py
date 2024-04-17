# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 12:38:36 2024

@author: lizbe
"""

class node:
    
    def __init__ (self, key, value):
        self.key = key 
        self.value = value 
        self.next=None
        
        
class hasTable:
    
    def __init__(self, capacity):
        self.size = 0
        self.capacity=capacity
        self.table = [None] * capacity
        
    def _hash(self, key): 
        return hash(key) % self.capacity 
    
    
    def hash_func(self, key):
        hash_value = 0
        for char in key:
            hash_value += ord(char)  # Sumar los valores ASCII de los caracteres de la clave
        return hash_value % self.capacity  
    
    
    
    def set(self, key, value):
        index= self.hash_func(key)
        flag= True
        if(flag):
            flag2=True
            current= self.table[index]
            while (current!=None):
                if(current.key==key):
                    current.value=value
                    flag2=False
                    break
                else: 
                    current=current.next
            if(flag2):
                nnode= node(key, value)
                nnode.next=self.table[index]
                self.table[index]=nnode
                self.size+=1
                
    def get(self, key):
          index= self.hash_func(key)
          flag= True
          current= self.table[index]
          while(current!=None):
              if(current.key== key):
                  return current.value
                  flag= False
                  break
              else:
                  current= current.next
          if(flag):
              return None
    def delete(self, key):
        index= self.hash_func(key)
        current= self.table[index]
        if(current!=None and current.key==key):
            self.table[index]=None
        else:
            follow=current.next
            while(follow!=None):
                if(follow.key==key):
                    current.next=follow.next
                follow=follow.next
            
        

has= hasTable(5)
has.set("A", 1)
has.set("B", 2) 
has.set("N", 3)  
has.set("D", 2) 
has.set("I", 2) 
has.delete("D")
             
       
        

                
        
    

