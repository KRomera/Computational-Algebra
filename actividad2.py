# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 20:01:58 2021

@author: Carlos Romera de Blas, Matemática y Física, AlCP-2
"""


def bolasCajas(n):
    
    #Se considera la configuración inicial como el turno 0
    lista=[1]*n
    turno=0
    posUltBola=0
    posAux=0

    # Lo ejecuto hasta volver a la posición inicial, para ello se debe dar
    #  la situación de que todas las bolas se encuentren en una única caja
    while lista[posUltBola] !=n:
        turno+=1
 
        while lista[posUltBola]>0:
            posAux+=1
            lista[posUltBola]-=1
            lista[(posUltBola+posAux) % n]+=1
        posUltBola=(posUltBola + posAux) % n
        posAux=0
        
    # Por último devolvemos el número de turnos necesarios 
    # para conseguir la configuración inicial:
    return turno+1
        
            
        
    
    