# -*- coding: utf-8 -*-
"""
@author: Carlos Romera de Blas, Matemática y Física, AlCP-2
"""
import random as rnd
import matplotlib.pyplot as plt
import time

# Suma de matrices
def suma(A,B):
    n=len(A)
    C=[]
    for i in range(n):
        C.append([])
        for j in range (n):
            C[i].append(0)  
            C[i][j]=A[i][j]+B[i][j]            
    return C

# Resta de matrices
def resta(A,B):
    n=len(A)
    C=[]
    for i in range(n):
        C.append([])
        for j in range (n):
            C[i].append(0)  
            C[i][j]=A[i][j]-B[i][j]            
    return C

# Multiplicación de Strassen:
def mult_strassen(A,B):
    n=len(A)
    if n == 1:
        return [[A[0][0]*B[0][0]]]
    impar=n%2!=0
    if(impar):
        for i in range (n):
            A[i]=A[i]+[0]
            B[i]=B[i]+[0]
        A=A+[[0]*(n+1)]
        B=B+[[0]*(n+1)]
    n+=1
   
    A11, A12, A21, A22= [], [], [], []
    B11, B12, B21, B22= [], [], [], []
    for i in range((n//2)):
        A11 = A11 + [A[i][:(n//2)]]
        B11 = B11 + [B[i][:(n//2)]]
        
        A12 = A12 + [A[i][(n//2):]]
        B12 = B12 + [B[i][(n//2):]]
        
        A21 = A21 + [A[(n//2) + i][:(n//2)]]
        B21 = B21 + [B[(n//2) + i][:(n//2)]]
        
        A22 = A22 + [A[(n//2) + i][(n//2):]]
        B22 = B22 + [B[(n//2) + i][(n//2):]]
        
    M1=mult_strassen(suma(A11,A22),suma(B11,B22))
    M2=mult_strassen(suma(A21,A22),B11)
    M3=mult_strassen(A11,resta(B12,B22))
    M4=mult_strassen(A22,resta(B21,B11))
    M5=mult_strassen(suma(A11,A12),B22)
    M6=mult_strassen(resta(A21,A11),suma(B11,B12))
    M7=mult_strassen(resta(A12,A22),suma(B21,B22))
    
    C11=suma(resta(suma(M1,M4),M5),M7)
    C12=suma(M3,M5)
    C21=suma(M2,M4)
    C22=suma(suma(resta(M1,M2),M3),M6)

    C1, C2 = [], []
    for i in range((n//2)):
        C1 = C1 + [C11[i] + C12[i]]
        C2 = C2 + [C21[i] + C22[i]]
    C = C1 + C2

    if(impar):
        for i in range (n):
            C[i].pop()
        C.pop()
        
    return C

# Programa para ver visualmente el tamaño de las matrices 
# frente al tiempo que tarda en multiplicarlas:
def grafica():
    mindigs = 1
    maxdigs = 50
    digstep = 1
    
    numdigs = []
    tiempos = []
     
    n = mindigs
    while n <= maxdigs:
       A = []
       B = []
       for i in range(n):
           A.append([])
           B.append([])
           for j in range (n):
               A[i].append(rnd.uniform(-1000.0,1000.0))
               B[i].append(rnd.uniform(-1000.0,1000.0))


       ini = time.time()
       mult_strassen(A, B)
       fin = time.time()
       numdigs += [n]
       t = fin-ini
       tiempos += [t]
       n += digstep
    
    plt.plot(numdigs, tiempos, "g-")
    plt.grid(b=True, which='major',axis='both', color='w', linestyle='--', linewidth=0.7)
    plt.xlabel('n=len(A)=len(B)')
    plt.ylabel('tiempo [seg]')
    ax = plt.gca()
    ax.set_facecolor((0.0, 0.0, 0.0))
    plt.savefig("mult_strassen.png")
    plt.show()
    plt.clf()