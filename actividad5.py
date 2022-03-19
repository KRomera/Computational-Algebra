# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 20:21:11 2021

@author: Carlos Romera de Blas, Matemática y Física, AlCP-2
"""
'''
Por un lado veamos que solo es necesario estudiarlo para a<N,
porque se a>N podemos escribirlo como a=n*N+x, con x<N y se tiene:
a=(n*)

'''

import math
import time

# Si no se quiere usar el gcd de math, se puede usar el siguiente programa,
# sin embargo computacionalmente tarda menos el de math, por lo que es el que se utiliza

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


#El siguiente programilla estudia si un numero es primo:
    
def isPrime(n) :
    if (n <= 1) :
        return False
    if (n <= 3) :
        return True
    if (n % 2 == 0 or n % 3 == 0) :
        return False
    i = 5
    while(i * i <= n) :
        if (n % i == 0 or n % (i + 2) == 0) :
            return False
        i = i + 6
    return True

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


# Los números compuestos n >= 2 que son pseudoprimos de Fermat 
# fuertes se llaman números de Carmichael

# Se define el programa para cada cualquier n \in N, por lo que se puede
# observar que para cualquier primo la condición se cumple si se obvia la 
# condición que estudia si el numero es primo o no

def isCarmichael(n):

    if isPrime(n):
        return False
    for a in range(2,n):
        if math.gcd(a,n)==1:
            if potencia_mod(a,n-1,n)!=1:
                return False
    return True



# Este programa calcula los m primeros números de Carmichael
def main(m):
    numCarmichael=[];
    i=2
    while len(numCarmichael)<m:
        if isCarmichael(i):
            numCarmichael+=[i]
        i+=1
    return numCarmichael

# Estre programa calcula el tiempo que se tarda en calcular los m primeros
# números de Carmichael

def tiempo(m):
    ini=time.time()
    main(m)
    fin=time.time()
    return (fin-ini)

# Para la entrega mostramos por pantalla directamente lo que nos pide el enunciado:
print(main(10))