import numpy as np
import matplotlib.pyplot as plt
import sympy

def proceso(data):
    Resultado = ""
    error = ""
    lista=[]
    medios=""
    try:
        fx = lambda x: eval(data[0])
        a = eval(data[1])
        b = eval(data[2])
        n = eval(data[3])
        h = (b - a) / (n)

        if n % 2 == 0:
            if n == 2:
                t = 3
            else:
                t = 6
            lista = [a]
            medios = []
            aux = a + h
            sumaMed = 0
            for i in range(n):
                lista.append(aux)
                aux = aux + h
                medios.append((lista[i] + lista[i + 1]) / 2)

                if n != 2:
                    if i < n:
                        sumaMed += fx(medios[i])
                        plt.plot(medios[i], 0, 'ro')

            j = 1
            sumaAux = 0
            # fmax = fx(lista[0])
            while j < n:
                sumaAux += (fx(lista[j]))
                j += 1

            med = (b - a) / 2
            der = (fx(a) - (4 * fx(med)) + (6 * fx((a + med) / 2)) - (4 * fx((a + med) / 2)) + fx(b)) / (h ** 4)

            if n == 2:
                suma = fx(lista[0]) + 4 * fx((a + b) / 2) + fx(lista[n])

                error = abs((-(h ** 5) / 90) * abs(der))

            else:
                suma = fx(lista[0]) + 4 * sumaMed + 2 * sumaAux + fx(lista[n])
                error = abs((-(3 * (h ** 5)) / 80) * abs(der))

            Resultado = abs((h / t) * suma)
            # print('Resultado: ', Resultado)
            # print('El error es de: ', error)
            plt.axvline(0, color='k')
            plt.axhline(0, 0, color='k')
            x = np.linspace(eval(data[4]), eval(data[5]), 100)
            fi = fx(x)
            plt.plot(x, fi, 'c')

            for i in range(n):
                x_trap_i = [lista[i], lista[i + 1]]
                y_trap_i = [fx(lista[i]), fx(lista[i + 1])]
                plt.fill_between(x_trap_i, y_trap_i, color='b', alpha=0.5)

        else:
            Resultado = "Error, la cantidad de debe ser par"
            plt.axvline(0, color='k')
            plt.axhline(0, 0, color='k')
        if str(Resultado) == str(np.nan):
            Resultado = "Error, verifique que la información ingresada sea correcta, de ser así\nel método diverge"
            error = "∞"
            lista = []
    except:
        Resultado = "Error, verifique que la información ingresada sea correcta, de ser así\nel método diverge"
        error = "∞"
        lista = []
        medios = []
    # plt.show()
    return Resultado, error, lista, medios
# data = ["np.sin(x)", "-2", "5", "1", "-2", "10"]
# b, c, d, e = proceso(data)
# print(b)
# print(c)