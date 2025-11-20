#include <stdio.h>
#include <string.h>
#include <ctype.h>

int validarFila(char *fila)
{
    int count = 0;
    for (int i = 0; fila[i]; i++)
    {
        if (isdigit(fila[i]))
            count += fila[i] - '0';
        else if (strchr("rnbqkpRNBQKP", fila[i]))
            count++;
        else
            return 0;
    }
    return count == 8;
}

int validarFEN(const char *fen)
{
    char copia[128];
    strcpy(copia, fen);

    char *campos[6];
    int i = 0;
    char *token = strtok(copia, " ");
    while (token && i < 6)
    {
        campos[i++] = token;
        token = strtok(NULL, " ");
    }
    if (i != 6)
        return 0;

    char tablero[128];
    strcpy(tablero, campos[0]);
    char *fila = strtok(tablero, "/");
    int filas = 0;
    while (fila)
    {
        if (!validarFila(fila))
            return 0;
        filas++;
        fila = strtok(NULL, "/");
    }
    return filas == 8;
}

int main()
{
    char fen[128];
    printf("Ingrese la cadena FEN: ");
    fgets(fen, sizeof(fen), stdin);
    fen[strcspn(fen, "\n")] = 0;

    if (validarFEN(fen))
        printf(" La cadena está en notación FEN valida.\n");
    else
        printf(" Cadena FEN es invalida.\n");

    return 0;
}