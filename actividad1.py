# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 22:41:40 2021

@author: Carlos Romera, ALCP 2, FÍSICA Y MATEMÁTICAS
"""

# Con la siguiente función calculamos el decimal n-ésimo de Champernowne
def d(n):
    i=1         # i indica el numero de cifras máximas del número 
                # en el que se encuentra el digito que buscamos.
    k=9         # k es el numero de cifras que recogen numeros
                # con menos cifras que i+1.
    pre=0       # pre es la cantidad de numeros con menos cifras que i.
    kaux=0      # kaux es el numero de cifras que recogen numeros
                # con menos cifras que i.
                
    while n>k:
        kaux=k
        k+=(i+1)*9*10**i    # Con este bucle calculamos los valores 
        pre+=9*10**(i-1)    # de las variables  anteriores para n
        i=i+1
        
    var=n-kaux              # var es el numero de cifras en el grupo de
                            # numeros de i cifras.
    caux=var//i             # caux es el numero de numeros con i cifras hasta n.
    c=pre+caux              # c es el numero de numeros completos, es decir,
                            # que todas sus cifras se encuentran en menor 
                            # o igual posición que n.
    mod=var%i               # mod es el modulo al calcular caux, es decir,
                            # la posición del decimal que buscamos a partir 
                            # de la última cifra del último número completo.
                            
    if mod !=0:
        # Se aisla el digito, primero se eliminan las 
        # cifras, del numero en el que se encuentra el digito, a
        # la derecha del digito y posteriormente las de la izquierda:
        return ( (c + 1) // (10 ** (i - mod) ) ) % 10       
    else :  
        # Se aisla el digito, eliminando las cifras, 
        # del numero en el que se encuentra el digito, a la izquierda del digito
        return c%10
    
     # De esta manera se obtiene el decimal n-ésimo de Chapernowne
    

# Utilizando la función anterior es trivial calcular la solución del problema:
def problema1_5():
    return d(1)*d(10)*d(100)*d(1000)*d(10000)*d(100000)*d(1000000)