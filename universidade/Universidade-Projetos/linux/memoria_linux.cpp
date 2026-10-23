// ============================================================================
//  Camada 2 - MEMORIA (versao Linux / WSL / MinGW)
//  Emula a EEPROM usando um arquivo binario. Inspecione com:
//        hexdump -C PARTICAO.BIN | less
// ============================================================================
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "memoria.h"

#ifndef PARTICAO_ARQUIVO
#define PARTICAO_ARQUIVO "PARTICAO.BIN"
#endif

// Descomente (ou compile com -DMEM_DEBUG) para ver cada acesso a memoria
// #define MEM_DEBUG

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

    // Garante o tamanho do "chip". Uma EEPROM nova vem com todos os bytes em 0xFF.
    fseek(f, 0, SEEK_END);
    long atual = ftell(f);
    if (atual < (long)MEM_TAMANHO) {
        unsigned char ff[256];
        memset(ff, 0xFF, sizeof(ff));
        long falta = (long)MEM_TAMANHO - atual;
        while (falta > 0) {
            size_t n = falta > (long)sizeof(ff) ? sizeof(ff) : (size_t)falta;
            fwrite(ff, 1, n, f);
            falta -= (long)n;
        }
        fflush(f);
    }
}

void memoria_fwrite(const void *buffer, uint16_t posicao, uint16_t tam)
{
    if ((unsigned long)posicao + tam > MEM_TAMANHO) {
        printf("ERRO: escrita fora da memoria (pos=%u tam=%u)\n", posicao, tam);
        return;
    }
#ifdef MEM_DEBUG
    printf("[mem] write pos=%u tam=%u\n", posicao, tam);
#endif
    fseek(f, posicao, SEEK_SET);
    fwrite(buffer, 1, tam, f);
    fflush(f);                  // assim o hexdump ja enxerga a alteracao
}

void memoria_fread(void *buffer, uint16_t posicao, uint16_t tam)
{
    if ((unsigned long)posicao + tam > MEM_TAMANHO) {
        printf("ERRO: leitura fora da memoria (pos=%u tam=%u)\n", posicao, tam);
        memset(buffer, 0xFF, tam);
        return;
    }
#ifdef MEM_DEBUG
    printf("[mem] read  pos=%u tam=%u\n", posicao, tam);
#endif
    fseek(f, posicao, SEEK_SET);
    size_t lidos = fread(buffer, 1, tam, f);
    if (lidos < tam) memset((uint8_t *)buffer + lidos, 0xFF, tam - lidos);
}
