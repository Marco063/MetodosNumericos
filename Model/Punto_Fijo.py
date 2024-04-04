#Librerias

import numpy as np
import matplotlib.pyplot as plt

#Funciones

def puntofijo(gx, a, tolera, iteramax):#Unicio de la función

    i = 1
    b = gx(a)
    tramo = abs(a - b)
    tabla = []
    while (tramo >= tolera and i <= iteramax):
        a = b
        b = gx(a)
        tramo = abs(b - a)
        tabla.append([i, round(a, 4), "  " + str(round(b, 4))])
        i = i + 1

    respuesta = b  # Retorno de la función

    # Validar respuesta

    if (i >= iteramax):
        respuesta = np.nan
    return respuesta, tramo, tabla, i

#Fin de la función

#Entadas
def proceso(data):
    i=0
    try:
        # fx = lambda x: 2*(x**2) - x - 5
        fx = lambda x: eval(data[0])
        # gx = lambda x: np.sqrt((x+5)/2)
        gx = lambda x: eval(data[1])
        x0 = eval(data[2])

        # Grafica
        a = eval(data[3])
        b = eval(data[4])

        tolera = 0.0001
        iteramax = 15  # máximo de iteraciones
        muestras = 100  # grafico
        # tramos = 50
        #
        # Procedimiento
        tabl = []
        respuesta, error, tabla, i = puntofijo(gx, x0, tolera, iteramax)

        # Salidas
        xi = np.linspace(a, b, muestras)
        fi = fx(xi)
        if (str(respuesta) != str(np.nan)) and (round(fx(respuesta), 1) == 0):

            gi = gx(xi)
            yi = xi
            plt.plot(xi, gi, label='g(x)')
            plt.plot(xi, yi, label='(y=x)')
            plt.axvline(respuesta)  # Linea vertical donde cruzan la funcion

            plt.plot(respuesta, 0, 'ro', label='raíz')
            plt.title('Punto Fijo')
            plt.legend()
            tabl = np.array(tabla)
        else:
            respuesta = "Error, verifique que la información ingresada sea correcta, de ser así el método diverge"
        plt.plot(xi, fi, label='f(x)')
        plt.axvline(0, color='k')
        plt.axhline(0, 0, color='k')
    except:
        error = ""
        respuesta = "Error, verifique que la información ingresada sea correcta, de ser así el método diverge"
        tabl = []
    # plt.show()
    return respuesta, error, tabl, i
# data = ['((4*(x**2))-8)/4', '(x**2)-2', '-2', '-5', '5']
# b = proceso(data)
# print(b)
