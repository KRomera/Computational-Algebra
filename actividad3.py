# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 13:15:15 2021

@author: Carlos Romera de Blas, Matemáticas y Física, ALCP-2
"""


    
''' La clave del problema reside en encontrar los n's con los que 
no existe una estrategia para ganar, o lo que es lo mismo, los n's
con los que puede ganar el que no empieza si hace bien la estrategia.
De esta manera, para ganar, la estrategia es siempre dejar al segundo con
un n perdedor. Por ejemplo, si le dejas solo con una piedra tiene posición
perdedora, igualmente si le dejas con 4, también pues posteriormente quite 1
o 2 piedras, tu quitaras 2 o 1 dejandole siempre la ultima piedra. De esta
manera, teniendo en cuenta que se pueden quitar 1, 2 o 6 piedras,
obtenemos una sucesión de números perdedores que viene dada por:
        a_(2m)=7m+1
        a_(2m+1)=7m+4  m=0,....,
Siendo los primeros valores de la sucesión a_0=1, a_1=4, y la sucesión:
    S= {1,4,8,11,15,18,22,...}
Con este programa básicamente se comprueba si n pertenece a la sucesión
como términoa_(2m) o a_(2m+1) para cierto m,
para determinar si existe estrategia ganadora o no. '''

def rapid_es_posible_ganar_con_n_piedras(n):
   if (n-1)%7==0 or (n-4)%7==0:
       return False
   else:
       return True
    
''' De manera menos efeciente pero para utilizar programación dinámica, y 
suponiendo que no existe la sucesión de términos encontrada,
se tendría el programa buscado: '''

def es_posible_ganar_con_n_piedras(n):
    loser=[False]+[True]*(n-1)
    for i in range (1,n):
        for j in (1,2,6):
            if i+1-j>0:   
                if loser[i-j]==False:
                    loser[i]=True
                    break
            loser[i]=False
    return loser[n-1]

    
