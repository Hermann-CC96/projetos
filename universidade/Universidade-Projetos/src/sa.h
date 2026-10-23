// ============================================================================
//  Camada 3 - SISTEMA DE ARQUIVOS DE BAIXO NIVEL
//
//  Layout da memoria (ver Figura 1 do enunciado):
//
//   +------------------------------+ endereco 0
//   | primeiro bloco livre (2 B)   |
//   +------------------------------+ endereco 2
//   | 12 inodos de 45 bytes        |   status(1) nome(8) tam(2) direto(32) indireto(2)
//   +------------------------------+ endereco 542
//   | N blocos de ponteiros (2 B)  |   lista encadeada de blocos livres
//   +------------------------------+ endereco 542 + 2N
//   | N blocos de dados (32 B)     |   bloco de ponteiro i  <->  bloco de dados i
//   +------------------------------+
//
//  Um arquivo guarda os primeiros 32 bytes DENTRO do inodo (campo "direto").
//  Os demais bytes ficam em blocos de dados, apontados por um "bloco indireto"
//  (um bloco de dados de 32 B que contem 16 ponteiros de 2 B).
//  Tamanho maximo de um arquivo = 32 + 16*32 = 544 bytes.
// ============================================================================
#ifndef SA_H
#define SA_H

#include <stdint.h>
#include <stddef.h>
#include "memoria.h"

#define SA_NUM_INODOS      12
#define SA_TAM_BLOCO       32
#define SA_TAM_NOME        8
#define SA_PTRS_POR_BLOCO  (SA_TAM_BLOCO / 2)                                   // 16
#define SA_NIL             0xFFFF   // "sem bloco" (o bloco 0 e valido, entao nao da pra usar 0)
#define SA_TAM_MAX_ARQUIVO (SA_TAM_BLOCO + SA_PTRS_POR_BLOCO * SA_TAM_BLOCO)    // 544

#define SA_INODO_LIVRE     0
#define SA_INODO_OCUPADO   1

// "packed" evita que o compilador insira bytes de alinhamento: sem isso o
// struct teria 46 bytes e o layout em disco ficaria errado.
typedef struct __attribute__((packed)) {
    uint8_t  status;                 // 0 = livre, 1 = ocupado
    char     nome[SA_TAM_NOME];      // 8 letras, preenchido com '\0' (sem terminador se tiver 8)
    uint16_t tam;                    // tamanho do arquivo em bytes
    uint8_t  direto[SA_TAM_BLOCO];   // primeiros 32 bytes do arquivo
    uint16_t indireto;               // numero do bloco indireto (SA_NIL se nao existe)
} Inodo;

static_assert(sizeof(Inodo) == 45, "Inodo precisa ter 45 bytes");

// Enderecos fixos do layout
#define SA_END_CABECALHO   0
#define SA_END_INODOS      2
#define SA_END_PONTEIROS   (SA_END_INODOS + SA_NUM_INODOS * sizeof(Inodo))              // 542
#define SA_NUM_BLOCOS      ((MEM_TAMANHO - SA_END_PONTEIROS) / (2 + SA_TAM_BLOCO))      // 1911 (512K) / 947 (256K)
#define SA_END_DADOS       (SA_END_PONTEIROS + 2 * SA_NUM_BLOCOS)

static_assert(SA_NUM_BLOCOS < SA_NIL, "numero de blocos nao cabe em 16 bits");

// ---------------------------------------------------------------- enderecos
uint16_t sa_end_inodo(int i);
uint16_t sa_end_dados(uint16_t bloco);

// ------------------------------------------------------------ ciclo de vida
void sa_init(void);          // inicializa a memoria (nao apaga nada)
void sa_formata(void);       // cria o SA do zero: inodos livres + lista de blocos livres

// ------------------------------------------------- alocacao (lista encadeada)
uint16_t sa_aloca_bloco(void);                 // devolve o bloco ou SA_NIL se nao ha livre
void     sa_libera_bloco(uint16_t bloco);      // devolve o bloco para o inicio da lista
uint16_t sa_conta_livres(void);                // percorre a lista (util para testes)

// ------------------------------------------------------------------- inodos
void sa_le_inodo(int i, Inodo *ino);
void sa_escreve_inodo(int i, const Inodo *ino);
int  sa_busca_inodo(const char *nome);         // indice do inodo ocupado com esse nome, ou -1
int  sa_cria_inodo(const char *nome);          // reserva um inodo livre (status=1), ou -1 se cheio
void sa_libera_arquivo(int i);                 // libera todos os blocos e zera o tamanho (inodo continua ocupado)
void sa_remove_inodo(int i);                   // libera os blocos E marca o inodo como livre

// ------------------------------------------------------ bloco indireto (16 ptrs)
void sa_le_tabela(uint16_t bloco_indireto, uint16_t tabela[SA_PTRS_POR_BLOCO]);
void sa_escreve_tabela(uint16_t bloco_indireto, const uint16_t tabela[SA_PTRS_POR_BLOCO]);

#endif
