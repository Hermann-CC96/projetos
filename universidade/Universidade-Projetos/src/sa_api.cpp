#include <stdio.h>
#include <string.h>
#include <stddef.h>
#include "sa_api.h"
#include "sa.h"

#define SA_MAX_ABERTOS 8     // quantos arquivos podem estar abertos ao mesmo tempo

// Estrutura de um arquivo aberto. Guarda apenas o necessario: o numero do
// inodo e a posicao atual. O inodo em si e relido da memoria a cada operacao,
// assim duas aberturas do mesmo arquivo nunca ficam com dados desatualizados.
struct ARQUIVO {
    bool     usado;
    bool     pode_ler;
    bool     pode_escrever;
    int      inodo;      // indice do inodo (0..11)
    uint16_t pos;        // posicao atual (offset em bytes)
};

static ARQUIVO abertos[SA_MAX_ABERTOS];

// Copia em RAM do bloco indireto (16 ponteiros). Funciona como um pequeno
// cache: le a tabela UMA vez por operacao em vez de uma vez por bloco.
struct TabelaInd {
    uint16_t ptr[SA_PTRS_POR_BLOCO];
    bool     carregada;
    bool     suja;       // precisa ser gravada de volta na memoria
};

// Garante que a tabela esta em RAM. Se o arquivo ainda nao tem bloco indireto
// e 'criar' for verdadeiro, aloca um (com todos os ponteiros = SA_NIL).
static bool tabela_carrega(Inodo *ino, TabelaInd *t, bool criar)
{
    if (t->carregada) return true;

    if (ino->indireto == SA_NIL) {
        if (!criar) return false;
        uint16_t b = sa_aloca_bloco();
        if (b == SA_NIL) return false;                 // memoria cheia
        ino->indireto = b;
        memset(t->ptr, 0xFF, sizeof(t->ptr));          // 0xFFFF = SA_NIL em todos
        t->suja = true;
    } else {
        sa_le_tabela(ino->indireto, t->ptr);
    }
    t->carregada = true;
    return true;
}

// ----------------------------------------------------------------- sistema
void inicializa_SA(void)
{
    memset(abertos, 0, sizeof(abertos));
    sa_init();
}

void formata_SA(void)
{
    memset(abertos, 0, sizeof(abertos));
    sa_formata();
}

// ------------------------------------------------------------------- fopen
ARQUIVO *meu_fopen(const char *nome, const char *modo)
{
    if (nome == NULL || modo == NULL) return NULL;

    size_t n = strlen(nome);
    if (n == 0 || n > SA_TAM_NOME) return NULL;

    bool modo_w = (modo[0] == 'w');
    bool modo_r = (modo[0] == 'r');
    if (!modo_w && !modo_r) return NULL;
    bool tem_mais = (strchr(modo, '+') != NULL);

    ARQUIVO *f = NULL;
    for (int i = 0; i < SA_MAX_ABERTOS; i++)
        if (!abertos[i].usado) { f = &abertos[i]; break; }
    if (f == NULL) return NULL;                         // muitos arquivos abertos

    int ino = sa_busca_inodo(nome);

    if (modo_w) {
        if (ino >= 0) sa_libera_arquivo(ino);           // "w" em arquivo existente: zera
        else          ino = sa_cria_inodo(nome);        // senao cria a entrada (status 0 -> 1)
        if (ino < 0) return NULL;                       // nao ha inodo livre
    } else {
        if (ino < 0) return NULL;                       // "r" e "r+" exigem que exista
    }

    f->usado         = true;
    f->inodo         = ino;
    f->pos           = 0;
    f->pode_ler      = modo_r || tem_mais;
    f->pode_escrever = modo_w || (modo_r && tem_mais);
    return f;
}

int meu_fclose(ARQUIVO *f)
{
    if (f == NULL || !f->usado) return -1;
    f->usado = false;       // os dados ja foram gravados a cada meu_fwrite
    return 0;
}

// ------------------------------------------------------------------ fwrite
int meu_fwrite(ARQUIVO *f, const uint8_t *buf, uint16_t tam)
{
    if (f == NULL || !f->usado || !f->pode_escrever || buf == NULL) return 0;

    Inodo ino;
    sa_le_inodo(f->inodo, &ino);

    TabelaInd t;
    t.carregada = false;
    t.suja = false;

    int pos = f->pos;
    int escrito = 0;

    while (escrito < tam && pos < SA_TAM_MAX_ARQUIVO) {
        int n;
        if (pos < SA_TAM_BLOCO) {
            // Primeiros 32 bytes: ficam dentro do proprio inodo (copia em RAM)
            n = SA_TAM_BLOCO - pos;
            if (n > tam - escrito) n = tam - escrito;
            memcpy(ino.direto + pos, buf + escrito, n);
        } else {
            // Demais bytes: blocos de dados apontados pela tabela indireta
            int q   = pos - SA_TAM_BLOCO;
            int k   = q / SA_TAM_BLOCO;                 // qual ponteiro da tabela
            int off = q % SA_TAM_BLOCO;                 // deslocamento dentro do bloco

            if (!tabela_carrega(&ino, &t, true)) break; // sem espaco
            if (t.ptr[k] == SA_NIL) {                   // bloco ainda nao existe: aloca
                uint16_t b = sa_aloca_bloco();
                if (b == SA_NIL) break;                 // sem espaco
                t.ptr[k] = b;
                t.suja = true;
            }
            n = SA_TAM_BLOCO - off;
            if (n > tam - escrito) n = tam - escrito;
            memoria_fwrite(buf + escrito, (uint16_t)(sa_end_dados(t.ptr[k]) + off), (uint16_t)n);
        }
        escrito += n;
        pos     += n;
    }

    if (t.suja) sa_escreve_tabela(ino.indireto, t.ptr);
    if (pos > ino.tam) ino.tam = (uint16_t)pos;
    sa_escreve_inodo(f->inodo, &ino);                   // grava tamanho, indireto e os 32 bytes diretos

    f->pos = (uint16_t)pos;
    return escrito;
}

// ------------------------------------------------------------------- fread
int meu_fread(ARQUIVO *f, uint8_t *buf, uint16_t tam)
{
    if (f == NULL || !f->usado || !f->pode_ler || buf == NULL) return 0;

    Inodo ino;
    sa_le_inodo(f->inodo, &ino);

    if (f->pos >= ino.tam) return 0;                    // ja no fim
    int disponivel = ino.tam - f->pos;
    if (tam > disponivel) tam = (uint16_t)disponivel;   // nao le alem do fim

    TabelaInd t;
    t.carregada = false;
    t.suja = false;

    int pos = f->pos;
    int lido = 0;

    while (lido < tam) {
        int n;
        if (pos < SA_TAM_BLOCO) {
            n = SA_TAM_BLOCO - pos;
            if (n > tam - lido) n = tam - lido;
            memcpy(buf + lido, ino.direto + pos, n);
        } else {
            int q   = pos - SA_TAM_BLOCO;
            int k   = q / SA_TAM_BLOCO;
            int off = q % SA_TAM_BLOCO;

            if (!tabela_carrega(&ino, &t, false)) break;    // inconsistencia: sem tabela
            if (t.ptr[k] == SA_NIL) break;                  // inconsistencia: sem bloco
            n = SA_TAM_BLOCO - off;
            if (n > tam - lido) n = tam - lido;
            memoria_fread(buf + lido, (uint16_t)(sa_end_dados(t.ptr[k]) + off), (uint16_t)n);
        }
        lido += n;
        pos  += n;
    }

    f->pos = (uint16_t)pos;
    return lido;
}

// ------------------------------------------------- ftell / feof / fseek
long meu_ftell(ARQUIVO *f)
{
    if (f == NULL || !f->usado) return -1;
    return f->pos;
}

int meu_feof(ARQUIVO *f)
{
    if (f == NULL || !f->usado) return 1;
    Inodo ino;
    sa_le_inodo(f->inodo, &ino);
    return f->pos >= ino.tam;
}

int meu_fseek(ARQUIVO *f, long deslocamento, int whence)
{
    if (f == NULL || !f->usado) return -1;

    Inodo ino;
    sa_le_inodo(f->inodo, &ino);

    long base;
    switch (whence) {
        case SEEK_SET: base = 0;        break;
        case SEEK_CUR: base = f->pos;   break;
        case SEEK_END: base = ino.tam;  break;
        default: return -1;
    }
    long nova = base + deslocamento;
    if (nova < 0 || nova > ino.tam) return -1;          // nao permite "buracos" no arquivo
    f->pos = (uint16_t)nova;
    return 0;
}

// ------------------------------------------------------------------ remove
int meu_remove(const char *nome)
{
    if (nome == NULL) return -1;
    int i = sa_busca_inodo(nome);
    if (i < 0) return -1;
    sa_remove_inodo(i);
    return 0;
}

// ------------------------------------------------------------- utilitarios
static int blocos_do_arquivo(const Inodo *ino)
{
    if (ino->indireto == SA_NIL) return 0;
    int dados = (ino->tam > SA_TAM_BLOCO) ? (ino->tam - SA_TAM_BLOCO + SA_TAM_BLOCO - 1) / SA_TAM_BLOCO : 0;
    return 1 + dados;                                   // 1 bloco indireto + blocos de dados
}

static void copia_nome(const Inodo *ino, char out[SA_TAM_NOME + 1])
{
    memcpy(out, ino->nome, SA_TAM_NOME);
    out[SA_TAM_NOME] = 0;                               // o nome de 8 letras nao tem terminador no disco
}

void lista_todos(void)
{
    Inodo ino;
    char nome[SA_TAM_NOME + 1];
    int total = 0;

    printf("\n=== Arquivos no sistema ===\n");
    printf(" #  Nome      Tamanho  Blocos\n");
    for (int i = 0; i < SA_NUM_INODOS; i++) {
        sa_le_inodo(i, &ino);
        if (ino.status != SA_INODO_OCUPADO) continue;
        copia_nome(&ino, nome);
        printf("%2d  %-8s  %7u  %6d\n", i, nome, (unsigned)ino.tam, blocos_do_arquivo(&ino));
        total++;
    }
    printf("Total: %d arquivo(s) | blocos livres: %u de %u\n",
           total, (unsigned)sa_conta_livres(), (unsigned)SA_NUM_BLOCOS);
}

void mostra_bytes_arquivo(const char *nome)
{
    ARQUIVO *f = meu_fopen(nome, "r");
    if (f == NULL) {
        printf("Arquivo '%s' nao encontrado\n", nome);
        return;
    }
    uint8_t linha[16];
    int n, offset = 0;
    printf("--- conteudo de '%s' ---\n", nome);
    while ((n = meu_fread(f, linha, sizeof(linha))) > 0) {
        printf("%04X: ", offset);
        for (int i = 0; i < 16; i++) {
            if (i < n) printf("%02X ", linha[i]);
            else       printf("   ");
        }
        printf(" |");
        for (int i = 0; i < n; i++) printf("%c", (linha[i] >= 32 && linha[i] < 127) ? linha[i] : '.');
        printf("|\n");
        offset += n;
    }
    meu_fclose(f);
}

void mostra_estrutura(void)
{
    Inodo ino;
    char nome[SA_TAM_NOME + 1];

    printf("\n=== Estrutura interna ===\n");
    printf("Blocos: %u | primeiro livre -> ver cabecalho | livres: %u\n",
           (unsigned)SA_NUM_BLOCOS, (unsigned)sa_conta_livres());
    for (int i = 0; i < SA_NUM_INODOS; i++) {
        sa_le_inodo(i, &ino);
        if (ino.status != SA_INODO_OCUPADO) continue;
        copia_nome(&ino, nome);
        printf("inodo %2d '%s' tam=%u", i, nome, (unsigned)ino.tam);
        if (ino.indireto == SA_NIL) {
            printf("  (so area direta)\n");
            continue;
        }
        uint16_t tab[SA_PTRS_POR_BLOCO];
        sa_le_tabela(ino.indireto, tab);
        printf("  indireto=bloco %u  dados=[", (unsigned)ino.indireto);
        bool primeiro = true;
        for (int k = 0; k < SA_PTRS_POR_BLOCO; k++) {
            if (tab[k] == SA_NIL) continue;
            printf("%s%u", primeiro ? "" : ",", (unsigned)tab[k]);
            primeiro = false;
        }
        printf("]\n");
    }
}
