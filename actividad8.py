# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 21:30:07 2021

@author: Carlos Romera de Blas, Matemáticas y Física, ALCP-2
"""




'''Algoritmos principales pedidos en el enunciado del problema:'''

# Algoritmo principal que calcula el producto de los polinomios f y g 
# en el anillo (Z/pZ)[x], donde f, g, y el resultado están representados 
# por la lista sus coeficientes (enteros entre 0 y p-1), 
# empezando por el término independiente.

# Observación: Si el polinomio es de grado d>=0, corresponderá con una lista 
# de longitud d+1, y el polinomio nulo será representado por la lista vacía []. 
# Por ejemplo, la llamada mult_pol_mod([1,2,3], [4,5], 7) debe devolver 
# [4,6,1,1], ya que (1+2x+3x^2)*(4+5x)=4+6x+x^2+x^3 en (Z/7Z)[x].

def mult_pol_mod(f,g,p):
    deg_f = len(f)-1
    deg_g = len(g)-1
    if deg_f == -1 or deg_g == -1:
        return []

    # Buscamos la potencia k de 2 tal que n=2^k > deg_f + deg_g
    n,k=1,0
    while n <= deg_f + deg_g:
        n *= 2
        k += 1

    # Rellenamos de ceros porque los polinomios se establece que deben ser
    # de longitud n=2^k para ejecutar el algoritmo mult_ss_mod(f,g,k,p)
    f += [0]*(n - deg_f + 1)
    g += [0]*(n - deg_g + 1)
    
    # Ejecutamos el algoritmo secundario:
    h = mult_ss_mod(f, g, k, p)
    
    # Eliminamos los ceros de la derecha que son innecesarios, 
    # evitando el error asegurandonos primero que h no es []
    while h and h[-1] == 0:
        h.pop()
        
    # Obteniendo la solución:
    return h

# Algoritmo secundario que calcula el producto de los polinomios f y g 
# en el anillo (Z/pZ)[x]/<x^2^k+1>, donde f, g, y el resultado están 
# representados por la lista sus 2^k coeficientes (enteros entre 0 y p-1), 
# empezando por el término independiente.

# Observación: En esta función, las listas que representan f, g, y el 
# resultado son de longitud exactamente 2^k. Por ejemplo, la llamada 
# mult_ss_mod([1,2,3,4], [4,5,6,6], 2, 7) deberá devolver [3,6,4,0], 
# ya que (1+2x+3x^2+4x^3)*(4+5x+6x^2+6x^3)=3+6x+4x^2 en (Z/7Z)[x]/<x^4+1>. 
# Esta función debe implementar el método de Schonhage-Strassen de forma 
# recursiva con casos bases k=0,1,2.

def mult_ss_mod(f,g,k,p):
    k1 = k // 2
    k2 = k - k1
    n1,n2= 2**k1,2**k2
    
    # Casos base k=0,1,2. Se utiliza la definición propia de convolución en mod p
        #(v \* w)_i=\sum_{j+l=i} v_j*w_l % p - \sum_{j+l=i+2^k} v_j*w_l % p 
    if k == 0:
        return [f[0] * g[0] % p]
    elif k == 1:
        return [(f[0] * g[0] - f[1] * g[1]) % p, (f[0] * g[1] + f[1] * g[0]) % p]
    elif k == 2:
        return [(f[0] * g[0] - f[1] * g[3] - f[2] * g[2] - f[3] * g[1]) % p,
                (f[0] * g[1] + f[1] * g[0] - f[2] * g[3] - f[3] * g[2]) % p,
                (f[0] * g[2] + f[1] * g[1] + f[2] * g[0] - f[3] * g[3]) % p,
                (f[0] * g[3] + f[1] * g[2] + f[2] * g[1] + f[3] * g[0]) % p]
    
    # Descomponemos como indica el método de Schonhage-Strassen:
        # f = f0(x) + f1(x)x^n1 + f2(x)x^(2*n1) + · · · + fn2−1(x)x^((n2−1)*n1)
        # g = g0(x) + g1(x)x^n1 + g2(x)x^(2*n1) + · · · + gn2−1(x)x^((n2−1)*n1)
    # Definimos:
        #f_weird = [f0(u)] + [f1(u)]y + [f2(u)]y^2 + · · · + [fn2−1(u)]y^(n2−1)
        # g_weird = [g0(u)] + [g1(u)]y + [g2(u)]y^2 + · · · + [gn2−1(u)]y^(n2−1)
    # Donde f_weird,g_weird in Zp[u]/<u^(2*n1)+1> [y],es decir, 
    # sus coeficientes f_weird[i] y g_weird[i] son de Zp[u]/<u^(2*n1)+1>,
    # con lo que tenemos que añadir n1 ceros, 
    # Añadir que f_weird[i]=fi(u) y g_weird[i]=gi(u) y además
    # deg(fi(u)), deg(gi(u)) < n_1

    f_weird = [[f[j] for j in range(i*n1, (i+1)*n1)] + ([0]*n1) for i in range(n2)]
    g_weird = [[g[j] for j in range(i*n1, (i+1)*n1)] + ([0]*n1) for i in range(n2)]

    # Calculamos h_weird = f_weird * g_weird (mod y^n2 + 1)
    h_weird = negaconvolucion(f_weird, g_weird, k1, k2, p)

    # Deshacemos h_weird a h, para eso usamos el bucle siguiente que calcula:
        # h_weird[0][:n1] + op(h_weird[0][n1:],h_weird[1][:n1]) 
        # + op(h_weird[1][n1:],h_weird[2][:n1]) 
        # + op(h_weird[2][n1:],h_weird[3][:n1]) 
        # + ... + op(h_weird[n2−2][n1:],h_weird[n2−1][:n1])
    h = [(x-y) % p for (x, y) in zip(h_weird[0][:n1], h_weird[n2-1][n1:])]
    for i in range(1, n2):
        h += [(x+y) % p for (x, y) in zip(h_weird[i-1][n1:], h_weird[i][:n1])]

    return h

'''Se incorpora el algoritmo necesario para calcular la negaconvoloción
en mult_ss_mod'''

# Algoritmo de la negaconvolución: si se interpretan a los vectores v,w de R^n 
# como elementos [v]; [w] en R[x]\<x^(2^k) + 1>, la negaconvolución corresponde 
# con el producto [v]*[w] en R[x]\<x^(2^k) + 1>.
# Además sea xi en R una raiz 2n-ésima de la unidad y sea 
# a=[1,xi,xi^2,....,xi^(n-1)] en R^n se tiene que: 
# v \* w = a^(-1) *idft_n(dft_n(a*v)*dft_n(a*w))
# donde \* representa la negaconvolución 
# y * el producto coordenada a coordenada

def negaconvolucion(f_weird,g_weird,k1,k2,p):
    n1,n2=2**k1,2**k2
    v,w=f_weird,g_weird
    
    # Como xi = [u^(2*n1/n2)] entonces la potencia es pow_xi = 2*n1/n2
    pow_xi = (2*n1)//n2

    # En la negaconvolución se define a = (1,xi,xi^2,...,xi^(n2-1),
    # por tanto exp_a = (0, pow_xi, pow_xi*2, ..., pow_xi*(n2-1))
    exp_a = [pow_xi*i for i in range(n2)]

    # Calculamos a*v y a*w
    # Al ser a potencias de u, creamos posteriormente prod_red que
    # permitirá multiplicar una función por u^poow y reducir módulo <u^(2*n1)+1>
    av = [prod_red(v[i], exp_a[i], 2*n1, p) for i in range(n2)]
    aw = [prod_red(w[i], exp_a[i], 2*n1, p) for i in range(n2)]

    # Calculamos las DFT, con raíz n2 ésima
    dftav = dft(av, pow_xi*2, p)
    dftaw = dft(aw, pow_xi*2, p)

    # Calculamos el producto de forma recursiva, 
    # donde dtfav[j] y dftaw[j] están en Zp[u]/<u^2n1 +1> 
    # y 2*n1 = 2*2^k1 por tanto mandamos k1+1
    prod = [mult_ss_mod(dftav[i], dftaw[i], k1+1, p) for i in range(n2)]

    # Calculamos la IFFT, con raíz n2 ésima
    inv_dft = idft(prod, pow_xi*2, p)

    # Multiplicamos por a^(-1)
    # Como a = (1,xi,xi^2,...,xi^(n2-1) y 
    # exp_a = (0, pow_xi, pow_xi*2, ..., pow_xi*(n2-1))
    # Entonces a_inv = (1,xi^-1,xi^-2,...,xi^-1*(n2-1))
    # Teniendo: invpow_a = (0, pow_xi*-1, pow_xi*-2, ..., pow_xi*-(n2-1)) 
    # invpow_a= (0, 2n2-pow_xi, 2n2-2*pow_xi, ..., 2n2-pow_xi*(n2-1))
    # Usando que xi^(-i) = xi^(2*n2-i) <=> pow_xi*(-i) = pow_xi*(2*n2-i)
    invpow_a = [2*n2*pow_xi - pow_xi*i for i in range(n2)]

    # Calculamos finalmente la negaconvolución como: a^-1*idft
    h_weird = [prod_red(inv_dft[i], invpow_a[i], 2*n1, p)
                for i in range(n2)]

    return h_weird
    
''' Se incorporan una serie de alguritmos auxiliares para la negaconvoloción: '''

# Algoritmo que calcula la multiplicación de un polinomio 
# f(u) por u^poow y lo reduce módulo <u^n+1> en Zp, es decir,
# prod=f(u)*u^poow (mod u^n+1)
def prod_red(f, poow, n, p):
    
    if poow == 0:
        return f

    prod = [0]*n
    
    # Si la potencia (poow) por la que multiplicamos es mayor que grado 
    # del polinomio por lo que f[0] comienza restando.
    # En caso contrario entonces f[0] comienza sumando.
    # En resumen el signo cambia cada n pasos: n(resta), 2*n(suma), 3*n(resta)
    signo = 1 if poow <= len(f) else -1

    # Observación: multiplicar por una poow de u es 
    # añadir ceros a la izquierda del polinomio f
    for i in range(len(f)):
        signo = -signo if (i+poow) % n == 0 else signo
        prod[(i+poow) % n] = (prod[(i+poow) % n] + signo * f[i]) % p

    return prod


# Algoritmo de Cooley-Tuckey modificado para un polinomio de polinomios en listas

def dft(f, pow_xi, p):
    n2 = len(f)
    n1_2 = len(f[0])  # longitud de los coeficientes
    if n2 == 1:
        return f
    f_even = [[0]*n1_2] * (n2//2)
    f_odd = [[0]*n1_2] * (n2//2)
    for i in range(n2//2):
        f_even[i] = f[2*i]
        f_odd[i] = f[2*i+1]
    a_even = dft(f_even, pow_xi*2, p)
    a_odd = dft(f_odd, pow_xi*2, p)
    a = [[0]*n1_2] * n2
    for i in range(n2//2):
        # a[i] = a_even[i] + pow_xi*i * a_odd[i]
        # a[i+n2//2] = a_even[i] - pow_xi*i * a_odd[i]

        # Calculamos pow_xi*i * a_odd[i] gracias a la función prod_red, 
        # definida anteriormente
        aux2 = prod_red(a_odd[i], pow_xi*i, n1_2, p)
        a[i] = [(a_even[i][j] + aux2[j]) % p
                for j in range(n1_2)]  # coordenada a coordenada
        a[i+n2//2] = [(a_even[i][j] - aux2[j]) % p
                      for j in range(n1_2)]
    return a



# Algoritmo que calcula la transformada inversa
# utilizando que D(xi)^(-1) = 1/n * D(1/xi)
def idft(a, pow_xi, p):

    # [u^(4*n1)] = 1 por tanto [u^k][u^(-k]) = [u^k][u^(4*n1 - k)]
    n2 = len(a)
    n1_2 = len(a[0])
    res = dft(a, 2*n1_2-pow_xi, p)

    # Calculamos el inverso de n2
    inv = pow(n2, -1, p)

    for i in range(n2):
        for j in range(n1_2):
            res[i][j] = (res[i][j] * inv) % p
    return res