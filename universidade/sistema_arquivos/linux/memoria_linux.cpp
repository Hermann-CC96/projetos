//  Camada 2 - MEMORIA (versao Linux / WSL / MinGW)
//  Emula a EEPROM usando um arquivo binario.
#include <stdio.h>
#include <stdlib.h>
#include "memoria.h"

#ifndef PARTICAO_ARQUIVO
#define PARTICAO_ARQUIVO "PARTICAO.BIN"
#endif

static FILE *f = NULL;

void memoria_init(void)
{
    if (f != NULL) return;

    // "b" = modo binario (importante no Windows: sem ele o \n vira \r\n e corrompe os dados)
    f = fopen(PARTICAO_ARQUIVO, "r+b");
    if (f == NULL) {
        f = fopen(PARTICAO_ARQUIVO, "w+b");
        if (f == NULL) {
            printf("Impossivel criar arquivo de particao\n");
            exit(1);
        }
    }
}

void memoria_fwrite(const void *buffer, uint16_t posicao, uint16_t tam)
{
    if ((unsigned long)posicao + tam > MEM_TAMANHO) {
        printf("ERRO: escrita fora da memoria (pos=%u tam=%u)\n", posicao, tam);
        return;
    }
    fseek(f, posicao, SEEK_SET);
    fwrite(buffer, 1, tam, f);
    fflush(f);                  // assim o hexdump ja enxerga a alteracao
}

void memoria_fread(void *buffer, uint16_t posicao, uint16_t tam)
{
    if ((unsigned long)posicao + tam > MEM_TAMANHO) {
        printf("ERRO: leitura fora da memoria (pos=%u tam=%u)\n", posicao, tam);
        return;
    }
    fseek(f, posicao, SEEK_SET);
    if (fread(buffer, 1, tam, f) != tam)
        printf("ERRO: leitura incompleta (pos=%u tam=%u)\n", posicao, tam);
}