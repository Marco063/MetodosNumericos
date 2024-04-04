import numpy as np
from fractions import Fraction

LIMIT = 1000
DECIMALES = 6

# FUNCIONES

# def leer():
#     A = []
#     B = []
#     Xt = []
#     tamanio = int(input('Ingrese el tamaño del sistema de ecuacines: '))
#     for i in range(tamanio):
#         fila = []
#         for j in range(tamanio):
#             nulo = True
#             while nulo != False:
#                 aux=Fraction(input('Ingrese el valor de X' + str(j + 1) + ": "))
#                 if i == j and aux == 0:
#                     print("¡¡No puede haber un 0 en la diagonal principal!!")
#                 else:
#                     fila.append(float(aux))
#                     nulo = False
#         A.append(fila)
#         aux2 = Fraction(input('Ingrese el resultado de esta ecuacion: '))
#         B.append(float(aux2))
#     print("Si desea ingresar el valor  de Xt ingrese 1 de lo contrario oprima cualquier tecla")
#     if input() == "1":
#         for i in range(tamanio):
#             aux = Fraction(input('Ingrese el valor de Xt0-' + str(i + 1) + ": "))
#             Xt.append(float(aux))
#     else:
#         for i in range(tamanio):
#             Xt.append(0)
#     print("---------------------------------------------------------------------------------------------------------")
#
#     return A, B, Xt

def imprimir_ecuaciones(A, B):
    ecuacionFrac = ""
    ecuacionDec = ""
    for i in range(len(A)):
        for j in range(len(A)):
            ecuacionFrac += "("+str(Fraction(A[i][j]).limit_denominator(LIMIT)) + ")X" + str(j + 1)
            ecuacionDec += str(round(A[i][j], DECIMALES)) + "X" + str(j + 1)
            if j != len(A) - 1:
                ecuacionFrac += " + "
                ecuacionDec += " + "
        ecuacionFrac += " = " + str(Fraction(B[i]).limit_denominator(LIMIT))+"\n"
        ecuacionDec += " = " + str(round(B[i], DECIMALES))+"\n"
    # print(ecuacionDec)
    # print(ecuacionFrac)
    return ecuacionDec, ecuacionFrac

def imprimir_info(A, B, Xt, err, error, i):
    XtDec = ""
    XtFrac = ""
    errorDec = ""
    errorFrac= ""
    aproximacion = ""
    for j in range(len(Xt)):
        XtDec += "X" + str(j+1) + " = " + str(round(Xt[j], DECIMALES)) + "\n"
        XtFrac += "X" + str(j+1) + " = " +str(Fraction(Xt[j]).limit_denominator(LIMIT)) + "\n"
        errorDec += "E" + str(j+1) + " = " +str(round(error[j], DECIMALES)) + "\n"
        errorFrac += "E" + str(j+1) + " = " +str(Fraction(error[j]).limit_denominator(LIMIT)) + "\n"

        aprox = 0
        for k in range(len(Xt)):
            aprox += A[j][k] * Xt[k]
        aproximacion += "F" + str(j+1) + " = " + str(Fraction(aprox).limit_denominator(LIMIT)) + " ~ " + str(Fraction(B[j]).limit_denominator(LIMIT))+" <--> "+str(round(aprox, DECIMALES)) + " ~ " + str(round(B[j], DECIMALES))+"\n"
    # print("---------------------------------------------------------------------------------------------------------")
    # print("Iteracion " + str(i) + ":")
    # print("-->Xt" + str(i) + ":")
    # print("\t" + XtFrac)
    # print("\t" + XtDec)
    # print("-->Error (" + str(round(err, DECIMALES)) + "):")
    # print("\t" + errorFrac)
    # print("\t" + errorDec)
    # print("-->Aproximacion:")
    # print(aproximacion)
    return XtFrac, XtDec, str(round(err, DECIMALES)), errorDec, errorFrac, aproximacion

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
    # print("---------------------------------------------------------------------------------------------------------")
    # print("Considere los siguientes despejes para el correcto desarrollo del sistema de ecuaciones")
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
    # print(despejeDec)
    # print(despejeFrac)

    return C, despejeDec, despejeFrac

def calcular(A, B, Xt0):
    try:
        C, desDec, despFrac = despejar(A, B)
        err = 1
        iteracion = 0
        resultado = ""
        while float(err) >= 0.0001 and iteracion < 50:
            Xti = Xt0.copy()
            for i in range(len(Xt0)):
                suma = 0
                for j in range(len(Xt0)):
                    if i != j:
                        suma += C[i][j] * Xti[j]
                suma += C[i][-1]
                Xti[i] = suma
            # err = calc_error(Xt0, Xti)
            errores = []
            aux = 0
            for i in range(len(Xt0)):
                errores.append(abs(Xt0[i] - Xti[i]))
                if errores[i] > aux:
                    aux = errores[i]
            err = aux

            iteracion += 1
            Xt0 = Xti
            # XtFrac,XtDec, str(round(err, DECIMALES)), errorDec,errorFrac,aproximacion
            XtFrac, XtDec, err, errorDec, errorFrac, aproximacion = imprimir_info(A, B, Xt0, err, errores, iteracion)

            # aux = "Iteracion:"+ str(iteracion) + "\nXt en fraccionarios:\n" +str(XtFrac)+ "" \
            #         "Xt en decimales:\n"+ str(XtDec) + "\nErrores: " + str(err) + "\nError en decimal: "+ str(errorDec)+"" \
            #         "\nError en fraccion" +str(errorFrac) +"\nAproximacion:\n"+aproximacion + "\n"
            # print(aux)
            resultado += ("Iteracion: " + str(iteracion) + "\nXt en fraccionarios:\n" + XtFrac + "\nXt en decimales:\n" + XtDec + "\nError: " + err + "\nErrores en decimal:\n" + str(errorDec) + "\nErrores en fraccion: \n" + errorFrac + "\nAproximacion:\n" + aproximacion + "\n")
        if iteracion >= 50:
            resultado = "El método diverge"
        return resultado, desDec, despFrac, iteracion
    except:
        resultado = "Error, verifique que la información ingresada sea correcta, de ser así el método diverge"
        return resultado, "", "", ""

# def calc_error(Xt0, Xti):
#     raiz = 0
#     suma = 0
#     aux = []
#     for i in range(len(Xt0)):
#         aux.append(pow((Xti[i] - Xt0[i]), 2))
#         suma += aux[i]
#     raiz = np.sqrt(suma)
#     return raiz


# DEFINICION MATRICES

# A = np.array([
#     [4, -1, 0, 0],
#     [-1, 4, -1, 0],
#     [0, -1, 4, -1],
#     [0, 0, -1, 4]
# ], float)
#
# B = [1, 1, 1, 1]

# A = np.array([
#     [1 / 2, 0, -1 / 4, 0],
#     [1 / 3, 7 / 6, 0, 9 / 10],
#    [1 / 8, -3 / 4, 3 / 2, 0],
#     [-2, 3 / 2, 3 / 8, 7 / 2]
# ], float)
#
# B = [1/3, 1/2, 1/6, 1/4]

# Xt = [0, 0, 0, 0]


# EJECUCION

# A, B, Xt = leer()
# print("Para el sistema de ecuaciones planteado a continuacion:")
# #PARA TODOS LOS FRACCIONARIOS CON DENOMINADOR MAYOR A 10000 DARA UN RESULTADO DE 0
# a,b = imprimir_ecuaciones(A, B)
# print(a)
# print(b)

# print("Se determinaran los valores aproximados de X mediante Gauss-Seidan partiendo de:")
# print("Xt = ", Xt)
#
# print(calcular(A, B)[0][2])




