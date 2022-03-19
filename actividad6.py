# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 13:45:39 2021


@author: Carlos Romera de Blas, Matemática y Física, AlCP-2
"""

import math
import time
import random as rand


# Maximo comun divisor de dos numeros
def gcd_binario(x,y):    # (x,y) != (0,0)
    done=False
    d=1
    while not done:
        x = abs(x)
        y = abs(y)
        xespar = x%2 == 0
        yespar = y%2 == 0
        if x == 0:           # caso base: gcd(0,y)=y
            m = y
            done =True
        elif y == 0:         # caso base: gcd(x,0)=x
            m = x
            done=True
        elif xespar and yespar:
            d*=2
            x,y=x//2, y//2
        elif xespar:
            x//=2
        elif yespar:
            y//=2
        elif x > y:
            x,y=y, x-y
        else:
            x,y=x, y-x
    return d*m

# Estos programas son para optimizar computacionalmente las operaciones en N/ZN

def sumar_mod (a, b, N): # 0 <= a,b < N, N >= 1
    c = a + b
    if c >= N:
        c -= N
    return c

def restar_mod (a, b, N): # 0 <= a,b < N, N >= 1
    c = a - b
    if c < 0:
        c += N
    return c

def multiplicar_mod (a, b, N): # 0 <= a,b < N, N >= 1
    c = a * b
    c %= N
    return c

def potencia_mod (a, k, N): # 0 <= a < N, k >= 0, N >= 2
    if k == 0: # caso base (k = 0)
        r = 1 # convencion : 0^0 = 1
    elif k % 2 == 0: # k es par (k > 0)
        r = potencia_mod (a, k//2 , N)
        r = multiplicar_mod (r, r, N)
    else : # k es impar (k > 0)
        r = potencia_mod (a, k -1, N)
        r = multiplicar_mod (a, r, N)
    return r

# Criba de Eratostenes, booleano de numeros primos menores o iguales que n:
def cribEras(n) :
    primos=[0,0]+[1]*(n-1)
    for i in range(2,int(len(primos)**(1/2))+1):
        if primos[i]==1:
            for j in range (2*i,len(primos),i):
                    primos[j]=0
    return primos


# El siguiente programa factoriza un número N
# Para ello utiliza el p-1 método de Pollard, introduciendo un B
def main(N,B):
    boolPrime=cribEras(B)   
    done=False   
    # Se ejecuta el algoritmo hasta encontrar 'y' no trivial
    while not done:
        a=rand.randint(1,N)
        x=gcd_binario(a,N)
        if x !=1 and x!=N:
            return x
        y=a
        # En vez de calcular beta se eleva 'y' a p un total de ceil(log_p(N)) veces
        # para todo p primo <= B
        for p in range(B+1):
            if boolPrime[p]:
                for i in range (0,math.ceil(math.log(N,p))):
                    y=potencia_mod(y,p,N)
        y=gcd_binario(y-1,N)
        if y!=1 and y!=N:
            done=True
    return y

# Este programa muestra el resultado y el tiempo que tarda en calcularlo por pantalla
def tiempo(N,B):
    ini=time.time()
    x=main(N,B)
    fin=time.time()
    return [x,fin-ini]


# Para la entrega mostramos por pantalla directamente lo que nos pide el enunciado:
N=1542201487980564464479858919567403438179217763219681634914787749213
B=100
factorUno=main(N,B)
factorDos=N//factorUno # Se divide // para que no lo escriba de forma cientifica
print ('N=',factorUno,'*',factorDos)