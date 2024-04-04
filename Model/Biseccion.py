#Metodo Biseccion

import numpy as np
import matplotlib.pyplot as plt

#Ingreso
def proceso(data):
    try:
        # ingreso = input('Funcion:\n')
        fx = lambda x: eval(data[0])
        # fx = lambda x: -0.5*(x**2) + 2.5*x + 4.5
        x = np.linspace(eval(data[3]), eval(data[4]), 1000)

        xi = eval(data[1])
        xu = eval(data[2])
        ant = 1
        error = 0.002
        tabla = []
        iteacion = 0
        while error > 0.001 and iteacion<100:
            xr = (xi + xu) / 2
            fxi = fx(xi)
            fxr = fx(xr)
            f = fxi * fxr
            if f > 0:
                xi = xr
            if f < 0:
                xu = xr
            try:
                error = abs((xr - ant) / xr) * 100
            except:
                pass
            # print(error)
            tabla.append([round(xi, 4), round(xu, 4), round(xr, 4), round(fxi, 4), round(fxr, 4), round(f, 4)])
            ant = xr
            iteacion += 1

        tabla = np.array(tabla)

        # print('[xi, xu, xr, fxi, fxr, f]')
        # print(tabla)
        # print('Error: ', error)
        # print('Raiz en: ', xr)
        fi = fx(x)

        plt.axvline(0, color='k')
        plt.axhline(0, 0, color='k')
        plt.plot(x, fi, 'c')
        if xi != np.nan:
            plt.axvline(xi)
        plt.plot(xi, 0, 'ro')
        if (round(fx(xr), 1) != 0):
            xr = "No tiene raíz en el intervalo o el método diverge"
    except:
        xr = "Error, verifique que la información ingresada sea correcta, de ser así el método diverge"
        error = "∞"
        tabla = []
    # plt.show()
    return error, tabla, xr, iteacion
# data = ["-0.5*(x**2) + 2.5*x + 4.5", "-5", "5","-15", "15"]
# b, c, d=proceso(data)
# print(b)
# print(c)