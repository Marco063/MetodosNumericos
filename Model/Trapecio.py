
import numpy as np
import matplotlib.pyplot as plt

def proceso(data):
    try:
        fx = lambda x: eval(data[0])
        a = eval(data[1])
        b = eval(data[2])
        n = eval(data[3])
        h = (b - a) / n
        lista = [a]
        aux = a + h

        for i in range(n):
            lista.append(aux)
            aux = aux + h

        j = 1
        sumaAux = 0
        # fmax = fx(lista[0])
        while j < n:
            sumaAux += (fx(lista[j]))
            j += 1
        suma = fx(lista[0]) + 2 * sumaAux + fx(lista[n])
        Resultado = abs((h / 2) * suma)
        # print('Resultado: ', Resultado)
        med = (b - a) / 2
        der = (fx(a) - (2 * fx(med)) + fx(b)) / (h ** 2)
        error = abs((((b - a) ** 3) / (12 * (n ** 2))) * abs(der))
        # print('El error es de:', error)

        plt.axvline(0, color='k')
        plt.axhline(0, 0, color='k')
        x = np.linspace(eval(data[4]), eval(data[5]), 100)
        fi = fx(x)
        plt.plot(x, fi, 'c')

        for i in range(n):
            x_trap_i = [lista[i], lista[i + 1]]
            y_trap_i = [fx(lista[i]), fx(lista[i + 1])]
            plt.fill_between(x_trap_i, y_trap_i, color='b', alpha=0.5)
        if str(Resultado) == str(np.nan):
            Resultado = "Error, verifique que la información ingresada sea correcta, de ser así\nel método diverge"
            error = "∞"
            lista = []
    except:
        Resultado= "Error, verifique que la información ingresada sea correcta, de ser así\nel método diverge"
        error = "∞"
        lista = []
    # plt.show()
    return Resultado, error, lista
# data = ["np.sin(x)", "-2", "5", "1000", "-2", "10"]
# # b, c, d=proceso(data)
# print(b)
# print(c)
# print(d)