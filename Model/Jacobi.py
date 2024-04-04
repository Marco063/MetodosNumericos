import numpy as np
from fractions import Fraction

LIMIT = 10000
DECIMALES = 6


# FUNCIONES

def leer():
    A = []
    B = []
    Xt = []
    tamanio = int(input('Ingrese el tamaño del sistema de ecuacines: '))
    for i in range(tamanio):
        fila = []
        for j in range(tamanio):
            nulo = True
            while nulo != False:
                aux = Fraction(input('Ingrese el valor de X' + str(j + 1) + ": "))
                if i == j and aux == 0:
                    print("¡¡No puede haber un 0 en la diagonal principal!!")
                else:
                    fila.append(float(aux))
                    nulo = False
        A.append(fila)
        aux2 = Fraction(input('Ingrese el resultado de esta ecuacion: '))
        B.append(float(aux2))
    print("Si desea ingresar el valor  de Xt ingrese 1 de lo contrario oprima cualquier tecla")
    if input() == "1":
        for i in range(tamanio):
            aux = Fraction(input('Ingrese el valor de Xt0-' + str(i + 1) + ": "))
            Xt.append(float(aux))
    else:
        for i in range(tamanio):
            Xt.append(0)
    print("---------------------------------------------------------------------------------------------------------")

    return A, B, Xt


def imprimir_ecuaciones(A, B):
    ecuacionFrac = ""
    ecuacionDec = ""
    for i in range(len(A)):
        for j in range(len(A)):
            ecuacionFrac += "(" + str(Fraction(A[i][j]).limit_denominator(LIMIT)) + ")X" + str(j + 1)
            ecuacionDec += str(round(A[i][j], DECIMALES)) + "X" + str(j + 1)
            if j != len(A) - 1:
                ecuacionFrac += " + "
                ecuacionDec += " + "
        ecuacionFrac += " = " + str(Fraction(B[i]).limit_denominator(LIMIT)) + "\n"
        ecuacionDec += " = " + str(round(B[i], DECIMALES)) + "\n"
    print(ecuacionDec)
    print(ecuacionFrac)


def imprimir_info(A, B, Xt, err, error, i):
    XtDec = ""
    XtFrac = ""
    errorDec = ""
    errorFrac = ""
    aproximacion = ""
    for j in range(len(Xt)):
        XtDec += str(round(Xt[j], DECIMALES)) + "\t"
        XtFrac += str(Fraction(Xt[j]).limit_denominator(LIMIT)) + "\t"
        errorDec += str(round(error[j], DECIMALES)) + "\t"
        errorFrac += str(Fraction(error[j]).limit_denominator(LIMIT)) + "\t"
        aprox = 0
        for k in range(len(Xt)):
            aprox += A[j][k] * Xt[k]
        aproximacion += "\t" + str(Fraction(aprox).limit_denominator(LIMIT)) + " ~ " + str(
            Fraction(B[j]).limit_denominator(LIMIT)) + " <--> " + str(round(aprox, DECIMALES)) + " ~ " + str(
            round(B[j], DECIMALES)) + "\n"
    print("---------------------------------------------------------------------------------------------------------")
    print("Iteracion " + str(i) + ":")
    print("-->Xt" + str(i) + ":")
    print("\t" + XtFrac)
    print("\t" + XtDec)
    print("-->Error (" + str(round(err, DECIMALES)) + "):")
    print("\t" + errorFrac)
    print("\t" + errorDec)
    print("-->Aproximacion:")
    print(aproximacion)


def despejar(A, B):
    C = []
    for i in range(len(A)):  # 0 a 3
        fila = []
        aux = A[i]
        for j in range(len(A)):
            if i == j:
                fila.append(1)
            else:
                fila.append((aux[j] * -1) / aux[i])
        fila.append(B[i] / aux[i])
        C.append(fila)
    print("---------------------------------------------------------------------------------------------------------")
    print("Considere los siguientes despejes para el correcto desarrollo del sistema de ecuaciones")
    despejeDec = ""
    despejeFrac = ""
    for i in range(len(A)):
        despejeDec += "X" + str(i + 1) + " = "
        despejeFrac += "X" + str(i + 1) + " = "
        for j in range(len(A)):
            if i != j:
                despejeDec += "(" + str(round(C[i][j], DECIMALES)) + ")X" + str(j + 1) + " + "
                despejeFrac += "(" + str(Fraction(C[i][j]).limit_denominator(LIMIT)) + ")X" + str(j + 1) + " + "
        despejeDec += str(round(C[i][-1], DECIMALES)) + "\n"
        despejeFrac += str(Fraction(C[i][-1]).limit_denominator(LIMIT)) + "\n"
    print(despejeDec)
    print(despejeFrac)

    return C


def calcular(A, B, Xt0):
    C = despejar(A, B)
    err = 1
    iteracion = 0
    while err >= 0.0001 and iteracion < 50:
        Xti = []
        for i in range(len(Xt0)):
            suma = 0
            for j in range(len(Xt0)):
                if i != j:
                    suma += C[i][j] * Xt0[j]
            suma += C[i][-1]
            Xti.append(round(suma, 6))

        # err = calc_error(Xt0, Xti)
        errores = []
        aux = 0
        for i in range(len(Xt0)):
            errores.append(round(abs(Xt0[i] - Xti[i]), 6))
            if errores[i] > aux:
                aux = errores[i]
        err = aux

        iteracion += 1
        Xt0 = Xti
        imprimir_info(A, B, Xt0, err, errores, iteracion)
    if iteracion >= 50:
        print("El metodo diverge")


def calc_error(Xt0, Xti):
    raiz = 0
    suma = 0
    aux = []
    for i in range(len(Xt0)):
        aux.append(pow((Xti[i] - Xt0[i]), 2))
        suma += aux[i]
    raiz = np.sqrt(suma)
    return raiz


# DEFINICION MATRICES

# A = np.array([
#     [4, -1, 0, 0],
#     [-1, 4, -1, 0],
#     [0, -1, 4, -1],
#     [0, 0, -1, 4]
# ], float)
#
# B = [1, 1, 1, 1]
#
# A = np.array([
#     [1 / 2, 0, 0, -1 / 4],
#     [1 / 2, 2, -1 / 3, 0],
#     [-1, 0, 3, 0],
#     [0, 1, -2, 7 / 3]
# ], float)
#
# B = [1 / 8, 1 / 6, 1 / 2, 1 / 2]
#
# Xt = [0, 0, 0, 0]

# EJECUCION

A, B, Xt = leer()
print("Para el sistema de ecuaciones planteado a continuacion:")
imprimir_ecuaciones(A, B)
print("Se determinaran los valores aproximados de X mediante Jacobi partiendo de:")
print("Xt = ", Xt)

calcular(A, B, Xt)
