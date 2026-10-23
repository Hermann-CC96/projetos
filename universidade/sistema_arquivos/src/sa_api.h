// ============================================================================
//  Camada 4 - SISTEMA DE ARQUIVOS DE ALTO NIVEL (API do usuario)
//  Funcoes parecidas com as da <stdio.h>, mas operando sobre o nosso SA.
// ============================================================================
#ifndef SA_API_H
#define SA_API_H

#include <stdio.h>      // SEEK_SET, SEEK_CUR, SEEK_END
#include <stdint.h>

// Tipo opaco: a estrutura real fica escondida em sa_api.cpp
typedef struct ARQUIVO ARQUIVO;

// ----------------------------------------------------------------- sistema
void inicializa_SA(void);   // prepara a memoria (NAO apaga os dados)
void formata_SA(void);      // apaga tudo e recria o SA (fazer so 1 vez)

// ---------------------------------------------------------------- arquivos
// Modos aceitos:
//   "w"   cria o arquivo (ou zera, se ja existir). So escrita.
//   "r+"  arquivo precisa existir. Leitura e escrita, comeca na posicao 0.
//   "r"   (extra) arquivo precisa existir. Somente leitura.  O main do enunciado usa este modo.
// Nome: 1 a 8 caracteres. Devolve NULL em caso de erro (nome invalido, nao existe,
// sem inodo livre ou muitos arquivos abertos).
ARQUIVO *meu_fopen(const char *nome, const char *modo);

// Devolve 0 em caso de sucesso.
int meu_fclose(ARQUIVO *f);

// Le/escreve VARIOS bytes de uma vez (nao usa fgetc/fputc).
// ATENCAO: diferente do stdio, devolvem o numero de BYTES transferidos (nao de itens).
// O arquivo cresce ate no maximo 544 bytes; o que passar disso nao e gravado.
int meu_fread (ARQUIVO *f, uint8_t *buffer, uint16_t tam);
int meu_fwrite(ARQUIVO *f, const uint8_t *buffer, uint16_t tam);

// Posicao atual (em bytes, a partir do inicio).
long meu_ftell(ARQUIVO *f);

// Devolve diferente de zero quando a posicao atual esta no fim do arquivo.
int meu_feof(ARQUIVO *f);

// (usada no main do enunciado) Move a posicao. whence = SEEK_SET / SEEK_CUR / SEEK_END.
// Devolve 0 se ok, -1 se a nova posicao ficaria fora de [0, tamanho].
int meu_fseek(ARQUIVO *f, long deslocamento, int whence);

// (extra) Remove um arquivo, devolvendo seus blocos para a lista de livres. 0 = ok, -1 = nao existe.
int meu_remove(const char *nome);

// ------------------------------------------------- utilitarios para a aplicacao
void lista_todos(void);                      // tabela com nome, tamanho e blocos de cada arquivo
void mostra_bytes_arquivo(const char *nome); // dump hexadecimal do conteudo
void mostra_estrutura(void);                 // debug: inodos e a cadeia de blocos de cada arquivo

#endif
