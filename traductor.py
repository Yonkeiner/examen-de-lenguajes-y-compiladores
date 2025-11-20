import re
import sys
import os
from typing import List, Tuple, Dict


class AnalizadorC:
    def __init__(self):
        # Diccionario de palabras reservadas de C y sus traducciones
        self.palabras_reservadas = {
            "auto": "automático",
            "break": "romper",
            "case": "caso",
            "char": "carácter",
            "const": "constante",
            "continue": "continuar",
            "default": "por_defecto",
            "do": "hacer",
            "double": "doble",
            "else": "si_no",
            "enum": "enumeración",
            "extern": "externo",
            "float": "flotante",
            "for": "para",
            "goto": "ir_a",
            "if": "si",
            "int": "entero",
            "long": "largo",
            "register": "registro",
            "return": "retornar",
            "short": "corto",
            "signed": "con_signo",
            "sizeof": "tamaño_de",
            "static": "estático",
            "struct": "estructura",
            "switch": "interruptor",
            "typedef": "definir_tipo",
            "union": "unión",
            "unsigned": "sin_signo",
            "void": "vacío",
            "volatile": "volátil",
            "while": "mientras",
            "include": "incluir",
            "define": "definir",
            "ifdef": "si_definido",
            "ifndef": "si_no_definido",
            "endif": "fin_si",
            "pragma": "pragma",
        }

        # Patrones regex para identificar diferentes elementos del código
        self.patron_palabra_reservada = re.compile(
            r"\b("
            + "|".join(re.escape(p) for p in self.palabras_reservadas.keys())
            + r")\b"
        )
        self.patron_comentario_linea = re.compile(r"//.*$")
        self.patron_comentario_bloque = re.compile(r"/\*.*?\*/", re.DOTALL)
        self.patron_cadena = re.compile(r"\"(?:\\.|[^\"])*\"")
        self.patron_caracter = re.compile(r"\'(?:\\.|[^\'])*\'")
        self.patron_directiva = re.compile(r"^\s*#\s*(\w+)")

    def cargar_archivo_c(self, ruta_archivo: str) -> str:
        """Carga un archivo C en memoria"""
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
            return contenido
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {ruta_archivo}")
            return ""
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return ""

    def proteger_cadenas_comentarios(self, codigo: str) -> Tuple[str, Dict[str, str]]:
        """Protege cadenas y comentarios reemplazándolos por marcadores"""
        marcadores = {}
        contador = 0

        # Proteger cadenas de texto
        def proteger_cadena(match):
            nonlocal contador
            marcador = f"__CADENA_{contador}__"
            marcadores[marcador] = match.group(0)
            contador += 1
            return marcador

        # Aplicar protección en orden específico
        codigo_protegido = self.patron_cadena.sub(proteger_cadena, codigo)
        codigo_protegido = self.patron_caracter.sub(proteger_cadena, codigo_protegido)
        codigo_protegido = self.patron_comentario_bloque.sub(
            proteger_cadena, codigo_protegido
        )
        codigo_protegido = self.patron_comentario_linea.sub(
            proteger_cadena, codigo_protegido
        )

        return codigo_protegido, marcadores

    def restaurar_cadenas_comentarios(
        self, codigo: str, marcadores: Dict[str, str]
    ) -> str:
        """Restaura las cadenas y comentarios protegidos"""
        for marcador, contenido_original in marcadores.items():
            codigo = codigo.replace(marcador, contenido_original)
        return codigo

    def traducir_palabra_reservada(self, match) -> str:
        """Traduce una palabra reservada encontrada"""
        palabra = match.group(0)
        return self.palabras_reservadas.get(palabra, palabra)

    def analizar_y_traducir(
        self, codigo_c: str
    ) -> Tuple[str, List[Tuple[str, str, int]]]:
        """Analiza el código C y traduce palabras reservadas"""
        if not codigo_c:
            return "", []

        # Proteger cadenas y comentarios
        codigo_protegido, marcadores = self.proteger_cadenas_comentarios(codigo_c)

        # Encontrar y traducir palabras reservadas
        lineas_originales = codigo_c.split("\n")
        traducciones = []
        lineas_traducidas = []

        for num_linea, linea in enumerate(lineas_originales, 1):
            linea_protegida, marcadores_linea = self.proteger_cadenas_comentarios(linea)

            # Buscar palabras reservadas en esta línea
            palabras_encontradas = []
            posiciones = []

            for match in self.patron_palabra_reservada.finditer(linea_protegida):
                palabra = match.group(0)
                if palabra in self.palabras_reservadas:
                    palabras_encontradas.append(palabra)
                    posiciones.append(match.start())

            # Traducir la línea protegida
            linea_traducida_protegida = self.patron_palabra_reservada.sub(
                self.traducir_palabra_reservada, linea_protegida
            )

            # Restaurar cadenas y comentarios
            linea_traducida = self.restaurar_cadenas_comentarios(
                linea_traducida_protegida, marcadores_linea
            )

            lineas_traducidas.append(linea_traducida)

            # Registrar traducciones
            for palabra in palabras_encontradas:
                traducciones.append(
                    (palabra, self.palabras_reservadas[palabra], num_linea)
                )

        codigo_traducido = "\n".join(lineas_traducidas)

        return codigo_traducido, traducciones

    def generar_reporte(
        self, traducciones: List[Tuple[str, str, int]], archivo_original: str
    ) -> str:
        """Genera un reporte detallado de las traducciones"""
        if not traducciones:
            return "No se encontraron palabras reservadas para traducir."

        reporte = f"REPORTE DE ANÁLISIS - {archivo_original}\n"
        reporte += "=" * 60 + "\n"
        reporte += f"Total de palabras reservadas encontradas: {len(traducciones)}\n\n"
        reporte += "DETALLE DE TRADUCCIONES:\n"
        reporte += "-" * 60 + "\n"

        # Agrupar por línea para mejor presentación
        traducciones_por_linea = {}
        for original, traducida, linea in traducciones:
            if linea not in traducciones_por_linea:
                traducciones_por_linea[linea] = []
            traducciones_por_linea[linea].append((original, traducida))

        for linea in sorted(traducciones_por_linea.keys()):
            reporte += f"Línea {linea}:\n"
            for original, traducida in traducciones_por_linea[linea]:
                reporte += f"  {original} -> {traducida}\n"

        return reporte

    def analizar_archivo(self, ruta_archivo_c: str, guardar_salida: bool = False):
        """Analiza un archivo C completo"""
        if not os.path.exists(ruta_archivo_c):
            print(f"Error: El archivo {ruta_archivo_c} no existe.")
            return

        print(f"Analizando archivo: {ruta_archivo_c}")
        print("-" * 50)

        # Cargar y analizar el archivo
        codigo_original = self.cargar_archivo_c(ruta_archivo_c)
        if not codigo_original:
            return

        codigo_traducido, traducciones = self.analizar_y_traducir(codigo_original)

        # Mostrar resultados
        print(f"Archivo analizado: {ruta_archivo_c}")
        print(f"Tamaño del archivo: {len(codigo_original)} caracteres")
        print(f"Palabras reservadas encontradas: {len(traducciones)}")
        print("\n" + "=" * 50)

        # Mostrar reporte
        reporte = self.generar_reporte(traducciones, ruta_archivo_c)
        print(reporte)

        # Mostrar código traducido (primeras 20 líneas)
        print("\nVISTA PREVIA DEL CÓDIGO TRADUCIDO (primeras 20 líneas):")
        print("-" * 50)
        lineas_traducidas = codigo_traducido.split("\n")[:20]
        for i, linea in enumerate(lineas_traducidas, 1):
            print(f"{i:3}: {linea}")

        if len(codigo_traducido.split("\n")) > 20:
            print("... (archivo demasiado largo para mostrar completo)")

        # Guardar archivo traducido si se solicita
        if guardar_salida:
            nombre_base = os.path.splitext(ruta_archivo_c)[0]
            ruta_salida = f"{nombre_base}_traducido.c"

            try:
                with open(ruta_salida, "w", encoding="utf-8") as archivo:
                    archivo.write(codigo_traducido)
                print(f"\nArchivo traducido guardado como: {ruta_salida}")
            except Exception as e:
                print(f"Error al guardar archivo traducido: {e}")


def main():
    """Función principal del programa"""
    analizador = AnalizadorC()

    print("ANALIZADOR DE CÓDIGO C - TRADUCTOR DE PALABRAS RESERVADAS")
    print("=" * 60)

    while True:
        print("\nOpciones:")
        print("1. Analizar archivo C")
        print("2. Mostrar diccionario de palabras reservadas")
        print("3. Salir")

        opcion = input("\nSeleccione una opción (1-3): ").strip()

        if opcion == "1":
            ruta_archivo = input("Ingrese la ruta del archivo C a analizar: ").strip()
            guardar = (
                input("¿Guardar archivo traducido? (s/n): ").strip().lower() == "s"
            )
            analizador.analizar_archivo(ruta_archivo, guardar)

        elif opcion == "2":
            print("\nDICCIONARIO DE PALABRAS RESERVADAS:")
            print("-" * 40)
            for ingles, espanol in analizador.palabras_reservadas.items():
                print(f"{ingles:15} -> {espanol}")

        elif opcion == "3":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


# Ejemplo de uso directo
if __name__ == "__main__":
    # Crear un archivo C de ejemplo para probar
    codigo_ejemplo = """
#include <stdio.h>
#include <stdlib.h>

int main() {
    int numero = 10;
    float resultado = 0.0;
    
    printf("Calculando factorial...\\n");
    
    for(int i = 1; i <= numero; i++) {
        if(i == 1) {
            resultado = 1;
        } else {
            resultado *= i;
        }
    }
    
    printf("Factorial de %d es: %.2f\\n", numero, resultado);
    return 0;
}
"""

    # Guardar archivo de ejemplo
    with open("ejemplo.c", "w", encoding="utf-8") as f:
        f.write(codigo_ejemplo)

    print("Archivo de ejemplo creado: ejemplo.c")

    # Ejecutar el programa principal
    main()
