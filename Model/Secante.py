# Método Secante

import numpy as np
import matplotlib.pyplot as plt

# INGRESO

def proceso(data):
    try:
        fx = lambda x: eval(data[0])
        # fx  = lambda x: x**3 + 2*(x**2) + 10*x - 20
        x = np.linspace(eval(data[3]), eval(data[4]), 1000)
        # x0 = 6
        # x1 = 5
        error = 0.001

        # PROCEDIMIENTO
        tabla = []
        deltax = 0.002
        xi = eval(data[2])
        xi1 = eval(data[1])
        fi = fx(x)
        plt.axvline(0, color='k')
        plt.axhline(0, 0, color='k')
        plt.plot(x, fi, 'c')
        i=0
        while error < deltax:

            xnuevo = xi - (fx(xi) * (xi - xi1)) / (fx(xi) - fx(xi1))
            deltax = abs(xnuevo - xi)
            tabla.append([i, round(xi, 4), round(xnuevo, 4), round(deltax, 4)])
            plt.plot(xi, fx(xi), 'go')
            plt.plot(xi1, fx(xi1), 'go')

            plt.plot(np.linspace(xi, xi1, 2), np.linspace(fx(xi), fx(xi1), 2), 'g')

            xi1 = xi
            xi = xnuevo
            i += 1
            # print('Deltax', deltax)

        # convierte la lista a un arreglo.
        tabla = np.array(tabla)
        # n = len(tabla)

        # SALIDA
        # print(['xi', 'xnuevo', 'deltax'])
        np.set_printoptions(precision=4)
        f = fx(xi)
        # print(tabla)
        # print('raiz en: ', xi)
        # print('con error de: ', deltax)
        if xi != np.nan:
            plt.axvline(xi)

        plt.plot(xi, 0, 'ro')
        if (round(fx(xi), 1) != 0):
            xi = "Error, El método diverge"
    except:
        i=0
        tabla=[]
        deltax= "∞"
        xi="Error, verifique que la información ingresada sea correcta, de ser así el método diverge"
    # plt.show()
    return deltax, xi, tabla, i

# data = ["x**3 + 2*(x**2) + 10*x - 20", "-5", "5","-15", "15"]
# b, c, d=proceso(data)
# print(b)
# print(c)
# print(d)