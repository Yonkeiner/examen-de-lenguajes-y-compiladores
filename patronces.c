// Dado una cadena C, valide si C se encuentra en notación FEN 

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

// Función para verificar si es una dirección IP válida
bool esIPValida(const char *ip)
{
    int numeros[4];
    int puntos = 0;
    char temp[20];

    // Copiar la cadena para no modificar la original
    strcpy(temp, ip);

    char *token = strtok(temp, ".");
    while (token != NULL)
    {
        puntos++;
        if (puntos > 4)
            return false; // Máximo 4 números

        // Verificar que sea un número
        for (int i = 0; token[i] != '\0'; i++)
        {
            if (!isdigit(token[i]))
                return false;
        }

        int num = atoi(token);
        if (num < 0 || num > 255)
            return false;

        numeros[puntos - 1] = num;
        token = strtok(NULL, ".");
    }

    return (puntos == 4); // Debe tener exactamente 4 números
}

// Función para verificar si es un correo electrónico válido
bool esCorreoValido(const char *correo)
{
    int arroba = -1;
    int punto = -1;
    int longitud = strlen(correo);

    // Buscar la posición del @ y del último punto
    for (int i = 0; i < longitud; i++)
    {
        if (correo[i] == '@')
        {
            if (arroba != -1)
                return false; // Solo un @ permitido
            arroba = i;
        }
        else if (correo[i] == '.')
        {
            punto = i;
        }
    }

    // Validaciones básicas
    if (arroba == -1)
        return false; // Debe tener @
    if (punto == -1)
        return false; // Debe tener al menos un punto
    if (arroba == 0)
        return false; // No puede empezar con @
    if (punto <= arroba + 1)
        return false; // El punto debe estar después del @
    if (punto == longitud - 1)
        return false; // No puede terminar con punto

    // Verificar caracteres válidos en la parte local (antes del @)
    for (int i = 0; i < arroba; i++)
    {
        char c = correo[i];
        if (!isalnum(c) && c != '.' && c != '_' && c != '-')
        {
            return false;
        }
    }

    // Verificar caracteres válidos en el dominio (después del @)
    for (int i = arroba + 1; i < longitud; i++)
    {
        char c = correo[i];
        if (!isalnum(c) && c != '.' && c != '-')
        {
            return false;
        }
    }

    return true;
}

// Función para verificar si es notación científica válida
bool esNotacionCientifica(const char *cadena)
{
    int longitud = strlen(cadena);
    bool tienePunto = false;
    bool tieneE = false;
    bool tieneSigno = false;
    bool tieneDigitosAntes = false;
    bool tieneDigitosDespues = false;
    int posicionE = -1;

    // Verificar formato básico
    for (int i = 0; i < longitud; i++)
    {
        char c = cadena[i];

        if (i == 0)
        {
            // Primer carácter puede ser signo, dígito o punto
            if (c == '+' || c == '-')
            {
                tieneSigno = true;
            }
            else if (isdigit(c))
            {
                tieneDigitosAntes = true;
            }
            else if (c == '.')
            {
                tienePunto = true;
            }
            else
            {
                return false;
            }
        }
        else
        {
            if (c == 'e' || c == 'E')
            {
                if (tieneE)
                    return false; // Solo una E permitida
                tieneE = true;
                posicionE = i;
            }
            else if (c == '.')
            {
                if (tienePunto || tieneE)
                    return false; // Solo un punto antes de E
                tienePunto = true;
            }
            else if (c == '+' || c == '-')
            {
                // Signo solo permitido después de E
                if (i != posicionE + 1)
                    return false;
            }
            else if (!isdigit(c))
            {
                return false;
            }
        }
    }

    // Validaciones adicionales
    if (!tieneE)
        return false; // Debe tener E
    if (posicionE == 0)
        return false; // No puede empezar con E
    if (posicionE == longitud - 1)
        return false; // No puede terminar con E

    // Verificar que hay dígitos antes de E
    for (int i = (tieneSigno ? 1 : 0); i < posicionE; i++)
    {
        if (isdigit(cadena[i]))
        {
            tieneDigitosAntes = true;
            break;
        }
    }

    if (!tieneDigitosAntes)
        return false;

    // Verificar que hay dígitos después de E
    int inicioExponente = posicionE + 1;
    if (cadena[inicioExponente] == '+' || cadena[inicioExponente] == '-')
    {
        inicioExponente++;
    }

    for (int i = inicioExponente; i < longitud; i++)
    {
        if (isdigit(cadena[i]))
        {
            tieneDigitosDespues = true;
            break;
        }
    }

    return tieneDigitosDespues;
}

// Función para mostrar el menú
void mostrarMenu()
{
    printf("\n=== RECONOCIMIENTO DE CADENAS ===\n");
    printf("1. Validar Notación Científica\n");
    printf("2. Validar Dirección IP\n");
    printf("3. Validar Correo Electrónico\n");
    printf("4. Validar Todos\n");
    printf("5. Salir\n");
    printf("Seleccione una opción: ");
}

// Función para probar todos los formatos
void probarTodos(const char *cadena)
{
    printf("\nCadena: \"%s\"\n", cadena);
    printf("--------------------------------\n");

    if (esNotacionCientifica(cadena))
    {
        printf("✓ NOTACIÓN CIENTÍFICA VÁLIDA\n");
    }
    else
    {
        printf("✗ No es notación científica válida\n");
    }

    if (esIPValida(cadena))
    {
        printf("✓ DIRECCIÓN IP VÁLIDA\n");
    }
    else
    {
        printf("✗ No es dirección IP válida\n");
    }

    if (esCorreoValido(cadena))
    {
        printf("✓ CORREO ELECTRÓNICO VÁLIDO\n");
    }
    else
    {
        printf("✗ No es correo electrónico válido\n");
    }
}

int main()
{
    int opcion;
    char cadena[100];

    printf("=== SISTEMA DE RECONOCIMIENTO DE CADENAS ===\n");

    while (1)
    {
        mostrarMenu();
        scanf("%d", &opcion);
        getchar(); // Limpiar buffer

        switch (opcion)
        {
        case 1:
            printf("\nIngrese cadena para validar notación científica: ");
            fgets(cadena, sizeof(cadena), stdin);
            cadena[strcspn(cadena, "\n")] = 0; // Eliminar salto de línea

            if (esNotacionCientifica(cadena))
            {
                printf("✓ '%s' es NOTACIÓN CIENTÍFICA VÁLIDA\n", cadena);
                printf("   Formato: número[.número]E[+-]número\n");
            }
            else
            {
                printf("✗ '%s' NO es notación científica válida\n", cadena);
                printf("   Ejemplos válidos: 1.23E-4, -5.67e+8, 2E10\n");
            }
            break;

        case 2:
            printf("\nIngrese cadena para validar dirección IP: ");
            fgets(cadena, sizeof(cadena), stdin);
            cadena[strcspn(cadena, "\n")] = 0;

            if (esIPValida(cadena))
            {
                printf("✓ '%s' es DIRECCIÓN IP VÁLIDA\n", cadena);
            }
            else
            {
                printf("✗ '%s' NO es dirección IP válida\n", cadena);
                printf("   Formato: xxx.xxx.xxx.xxx (0-255 cada octeto)\n");
            }
            break;

        case 3:
            printf("\nIngrese cadena para validar correo electrónico: ");
            fgets(cadena, sizeof(cadena), stdin);
            cadena[strcspn(cadena, "\n")] = 0;

            if (esCorreoValido(cadena))
            {
                printf("✓ '%s' es CORREO ELECTRÓNICO VÁLIDO\n", cadena);
            }
            else
            {
                printf("✗ '%s' NO es correo electrónico válido\n", cadena);
                printf("   Formato: usuario@dominio.extensión\n");
            }
            break;

        case 4:
            printf("\nIngrese cadena para validar todos los formatos: ");
            fgets(cadena, sizeof(cadena), stdin);
            cadena[strcspn(cadena, "\n")] = 0;
            probarTodos(cadena);
            break;

        case 5:
            printf("¡Hasta luego!\n");
            return 0;

        default:
            printf("Opción no válida. Intente nuevamente.\n");
        }

        printf("\nPresione Enter para continuar...");
        getchar();
    }

    return 0;
}