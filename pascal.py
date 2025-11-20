import time
import math


def generar_coeficientes(n):
    """Genera coeficientes usando el triángulo de Pascal"""
    coeficientes = [1]  # (x+1)^0 = 1

    for i in range(1, n + 1):
        nuevo_coeficiente = [1]  # Primer coeficiente siempre es 1
        # Calcular coeficientes intermedios
        for j in range(1, i):
            nuevo_coeficiente.append(coeficientes[j - 1] + coeficientes[j])
        nuevo_coeficiente.append(1)  # Último coeficiente siempre es 1
        coeficientes = nuevo_coeficiente

    return coeficientes


def mostrar_polinomio(coeficientes, n):
    """Muestra el polinomio formateado"""
    print(f"(x+1)^{n} = ", end="")
    terminos = []

    for i in range(n, -1, -1):
        coef = coeficientes[i]
        if coef != 0:
            if i == n:
                terminos.append(f"{coef}")
            else:
                terminos.append(f"{coef}")

            if i > 1:
                terminos[-1] += f"x^{i}"
            elif i == 1:
                terminos[-1] += "x"

    print(" + ".join(terminos))


def calcular_polinomio(coeficientes, n, x):
    """Calcula f(x) paso a paso según el polinomio generado"""
    resultado = 0.0

    print(f"Calculando f({x}) = ", end="")
    expresion = []
    for i in range(n, -1, -1):
        expresion.append(f"{coeficientes[i]}*{x}^{i}")

    print(" + ".join(expresion))

    print("Paso a paso:")
    for i in range(n, -1, -1):
        potencia_x = math.pow(x, i)
        termino = coeficientes[i] * potencia_x
        resultado += termino
        print(
            f"Termino {n - i + 1}: {coeficientes[i]}*{x}^{i} = {coeficientes[i]}*{potencia_x:.6f} = {termino:.6f}"
        )

    return resultado


def main():
    try:
        n = int(input("Ingrese el valor de n: "))

        if n < 0:
            print("n debe ser no negativo")
            return

        # Medir tiempo de generación de coeficientes
        inicio = time.time()
        coeficientes = generar_coeficientes(n)
        fin = time.time()
        tiempo_ms = (fin - inicio) * 1000

        # a) Mostrar coeficientes y polinomio
        print("\n--- PARTE a) ---")
        print("Coeficientes:", " ".join(map(str, coeficientes))) 

        if n <= 10:
            mostrar_polinomio(coeficientes, n)
        else:
            print("(Polinomio muy grande para mostrar)")

        # b) Calcular para x dado
        print("\n--- PARTE b) ---")
        x = float(input("Ingrese el valor de x: "))

        resultado = calcular_polinomio(coeficientes, n, x)
        print(f"Resultado final: f({x}) = {resultado:.6f}")

        # Verificación
        verificacion = math.pow(x + 1, n)
        print(f"Verificación: ({x}+1)^{n} = {verificacion:.6f}")

        # Guardar resultados para n=100 en archivo
        if n == 100:
            with open("resultado_python.txt", "w") as archivo:
                archivo.write("Coeficientes para (x+1)^100:\n")
                for i, coef in enumerate(coeficientes):
                    archivo.write(f"{coef} ")
                    if (i + 1) % 10 == 0:
                        archivo.write("\n")
                archivo.write(
                    f"\n\nTiempo de ejecución: {tiempo_ms:.4f} milisegundos\n"
                )
            print("\nResultados guardados en 'resultado_python.txt'")

        print(f"Tiempo de generación de coeficientes: {tiempo_ms:.4f} milisegundos")

    except ValueError:
        print("Error: Ingrese valores numéricos válidos")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
