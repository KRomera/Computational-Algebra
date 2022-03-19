# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 18:01:56 2021

@author: Carlos Romera de Blas, Matemática y Física, AlCP-2
"""
import math
import random as rand
import matplotlib.pyplot as plt

# Teorema del numero primo
def thPrimeNumber(x):
    cotaInf=int(x/(math.log(x)+2))
    cotaSup=int(x/(math.log(x)-4))
    print('La cantidad de numeros primeros en el intervarlo', [1,x], 'esta acotada tal que', cotaInf,'< \pi(',x,')<',cotaSup)
    return


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


# Incluimos el potencia_mod iterativo

def lista_de_bits(k):
   l = []
   while k > 0:
      l += [k%2]
      k //= 2
   return l

def potencia_mod(a, k, N):             # 0 <= a < N, k >= 0, N >= 2
   r = 1
   l = lista_de_bits(k)
   n = len(l)
   for i in range(n):
      r = multiplicar_mod(r, r, N)
      if l[n-1-i] == 1:
         r = multiplicar_mod(r, a, N)
   return r

# Simbolo de Jacobi
def jacobi(a, n):
    a %= n
    val = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                val = -val
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            val = -val
        a %= n
    if n == 1:
        return val
    else:
        return 0


# Nuestro algoritmo de Solovay-Strassen:
def generar_primo(n,k):
    cnt=0
    done=False
    while not done:
        N=rand.randint(10**(n-1),10**n-1)
        if N%2!=0 and N>=3: #Condiciones para el test de solovay-strassen
            for i in range(k):
                a=rand.randint(1,N-1) 
                if gcd_binario(a,N)!=1:
                    break
                valUno=jacobi(a,N)
                valDos=potencia_mod(a,(N-1)//2,N)
                if restar_mod(valUno,valDos,N)!=0:
                    break
            cnt+=1  # Se hace la cuenta de cnt para numeros impares >=3 
            done= i==(k-1)
    p=N   
    return (p,cnt)

# Nuestra función que genera el histograma en intervalos de 100:
def generar_histograma():
    Cnts=[]
    for i in range(200):
        aux=generar_primo(300,20)
        Cnts+=[aux[1]]
    print(Cnts)
    intervalos=range(0,max(Cnts)+200,100)
    plt.hist(x=Cnts, bins=intervalos, color='#F2AB6D', rwidth=0.85)
    plt.xlabel('cnt')
    plt.ylabel('frecuencia')
    plt.title('Histograma para generar_primo(300,20)')
    plt.savefig("histograma.png")
    plt.show()
    plt.clf()
    
    