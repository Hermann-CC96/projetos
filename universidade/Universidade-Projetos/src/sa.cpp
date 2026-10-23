#include <string.h>
#include "sa.h"

// ----------------------------------------------------------------- enderecos
uint16_t sa_end_inodo(int i)             { return (uint16_t)(SA_END_INODOS + i * sizeof(Inodo)); }
static uint16_t end_ponteiro(uint16_t b) { return (uint16_t)(SA_END_PONTEIROS + 2 * b); }
uint16_t sa_end_dados(uint16_t b)        { return (uint16_t)(SA_END_DADOS + SA_TAM_BLOCO * b); }

// ------------------------------------------------- cabecalho / ponteiros (2 B)
static uint16_t le_primeiro_livre(void)
{
    uint16_t v;
    memoria_fread(&v, SA_END_CABECALHO, sizeof(v));
    return v;
}
static void escreve_primeiro_livre(uint16_t v)
{
    memoria_fwrite(&v, SA_END_CABECALHO, sizeof(v));
}
static uint16_t le_ponteiro(uint16_t b)
{
    uint16_t v;
    memoria_fread(&v, end_ponteiro(b), sizeof(v));
    return v;
}
static void escreve_ponteiro(uint16_t b, uint16_t v)
{
    memoria_fwrite(&v, end_ponteiro(b), sizeof(v));
}

// --------------------------------------------------------------- ciclo de vida
void sa_init(void)
{
    memoria_init();
}

void sa_formata(void)
{
    // 1) cabecalho: o primeiro bloco livre e o bloco 0
    escreve_primeiro_livre(0);

    // 2) inodos: tudo zero => status 0 (livre)
    uint8_t zeros[64];
    memset(zeros, 0, sizeof(zeros));
    uint16_t end = SA_END_INODOS;
    int restante = SA_NUM_INODOS * sizeof(Inodo);
    while (restante > 0) {
        int n = restante < (int)sizeof(zeros) ? restante : (int)sizeof(zeros);
        memoria_fwrite(zeros, end, n);
        end += n;
        restante -= n;
    }

    // 3) blocos de ponteiros: lista encadeada 0 -> 1 -> 2 -> ... -> N-1 -> NIL
    //    (escreve em lotes de 32 ponteiros para ser rapido na EEPROM)
    uint16_t lote[32];
    for (uint16_t b = 0; b < SA_NUM_BLOCOS; b += 32) {
        int n = SA_NUM_BLOCOS - b;
        if (n > 32) n = 32;
        for (int j = 0; j < n; j++) {
            uint16_t prox = (uint16_t)(b + j + 1);
            lote[j] = (prox < SA_NUM_BLOCOS) ? prox : SA_NIL;
        }
        memoria_fwrite(lote, end_ponteiro(b), 2 * n);
    }
}

// -------------------------------------------------------------------- alocacao
uint16_t sa_aloca_bloco(void)
{
    uint16_t b = le_primeiro_livre();
    if (b == SA_NIL || b >= SA_NUM_BLOCOS) return SA_NIL;     // memoria cheia (ou SA nao formatado)

    uint16_t proximo = le_ponteiro(b);        // o proximo da lista passa a ser o primeiro livre
    escreve_primeiro_livre(proximo);
    escreve_ponteiro(b, SA_NIL);              // bloco agora esta em uso
    return b;
}

void sa_libera_bloco(uint16_t b)
{
    if (b >= SA_NUM_BLOCOS) return;
    escreve_ponteiro(b, le_primeiro_livre()); // aponta para o antigo primeiro livre
    escreve_primeiro_livre(b);                // e vira o novo primeiro livre
}

uint16_t sa_conta_livres(void)
{
    uint16_t cont = 0;
    uint16_t b = le_primeiro_livre();
    while (b != SA_NIL && b < SA_NUM_BLOCOS && cont <= SA_NUM_BLOCOS) {
        cont++;
        b = le_ponteiro(b);
    }
    return cont;
}

// ---------------------------------------------------------------------- inodos
void sa_le_inodo(int i, Inodo *ino)
{
    memoria_fread(ino, sa_end_inodo(i), sizeof(Inodo));
}

void sa_escreve_inodo(int i, const Inodo *ino)
{
    memoria_fwrite(ino, sa_end_inodo(i), sizeof(Inodo));
}

int sa_busca_inodo(const char *nome)
{
    Inodo ino;
    for (int i = 0; i < SA_NUM_INODOS; i++) {
        sa_le_inodo(i, &ino);
        if (ino.status == SA_INODO_OCUPADO && strncmp(ino.nome, nome, SA_TAM_NOME) == 0)
            return i;
    }
    return -1;
}

int sa_cria_inodo(const char *nome)
{
    Inodo ino;
    for (int i = 0; i < SA_NUM_INODOS; i++) {
        sa_le_inodo(i, &ino);
        if (ino.status == SA_INODO_LIVRE) {
            memset(&ino, 0, sizeof(ino));
            ino.status = SA_INODO_OCUPADO;
            memcpy(ino.nome, nome, strlen(nome));     // o resto do campo ja esta zerado ('\0')
            ino.tam = 0;
            ino.indireto = SA_NIL;
            sa_escreve_inodo(i, &ino);
            return i;
        }
    }
    return -1;
}

void sa_libera_arquivo(int i)
{
    Inodo ino;
    sa_le_inodo(i, &ino);

    if (ino.indireto != SA_NIL) {
        uint16_t tabela[SA_PTRS_POR_BLOCO];
        sa_le_tabela(ino.indireto, tabela);
        for (int k = 0; k < SA_PTRS_POR_BLOCO; k++)
            if (tabela[k] != SA_NIL) sa_libera_bloco(tabela[k]);   // blocos de dados
        sa_libera_bloco(ino.indireto);                              // o proprio bloco indireto
    }
    ino.indireto = SA_NIL;
    ino.tam = 0;
    sa_escreve_inodo(i, &ino);
}

void sa_remove_inodo(int i)
{
    sa_libera_arquivo(i);
    Inodo ino;
    sa_le_inodo(i, &ino);
    ino.status = SA_INODO_LIVRE;
    sa_escreve_inodo(i, &ino);
}

// -------------------------------------------------------------- bloco indireto
void sa_le_tabela(uint16_t bi, uint16_t tabela[SA_PTRS_POR_BLOCO])
{
    memoria_fread(tabela, sa_end_dados(bi), SA_TAM_BLOCO);
}

void sa_escreve_tabela(uint16_t bi, const uint16_t tabela[SA_PTRS_POR_BLOCO])
{
    memoria_fwrite(tabela, sa_end_dados(bi), SA_TAM_BLOCO);
}
