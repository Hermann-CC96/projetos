// ============================================================================
//  Testes automaticos do sistema de arquivos (versao Linux, memoria em arquivo)
//
//  Compilar e rodar:   make testes
//  (usa AddressSanitizer + UBSan; para MinGW/Windows:  make testes SAN=)
//
//  Cada CHECK imprime [OK] ou [FALHA]. O programa retorna 0 se tudo passou.
// ============================================================================
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "sa_api.h"
#include "sa.h"          // so para os testes olharem a lista de blocos livres

static int total_checks = 0;
static int falhas = 0;

#define CHECK(cond, descricao)                                              \
    do {                                                                    \
        total_checks++;                                                     \
        if (cond) {                                                         \
            printf("  [OK]     %s\n", descricao);                           \
        } else {                                                            \
            falhas++;                                                       \
            printf("  [FALHA]  %s   (linha %d)\n", descricao, __LINE__);    \
        }                                                                   \
    } while (0)

static void titulo(const char *t) { printf("\n== %s ==\n", t); }

// Padrao de bytes reproduzivel para comparar o que foi escrito com o que foi lido
static void preenche(uint8_t *b, int n, int semente)
{
    for (int i = 0; i < n; i++) b[i] = (uint8_t)((i * 7 + semente) & 0xFF);
}

static int livres(void) { return sa_conta_livres(); }

// Escreve n bytes de padrao em um arquivo novo (modo "w"), em pedacos de "passo" bytes
static int cria_arquivo(const char *nome, int n, int semente, int passo)
{
    uint8_t buf[600];
    preenche(buf, n, semente);
    ARQUIVO *f = meu_fopen(nome, "w");
    if (f == NULL) return -1;
    int total = 0;
    for (int off = 0; off < n; off += passo) {
        int q = (n - off < passo) ? (n - off) : passo;
        total += meu_fwrite(f, buf + off, (uint16_t)q);
    }
    meu_fclose(f);
    return total;
}

// Le o arquivo inteiro e compara com o padrao esperado
static bool confere_arquivo(const char *nome, int n, int semente)
{
    uint8_t esperado[600], lido[600];
    preenche(esperado, n, semente);
    memset(lido, 0, sizeof(lido));
    ARQUIVO *f = meu_fopen(nome, "r");
    if (f == NULL) return false;
    int r = meu_fread(f, lido, (uint16_t)n);
    meu_fclose(f);
    return r == n && memcmp(esperado, lido, n) == 0;
}

// ---------------------------------------------------------------------------
static void teste_formatacao(void)
{
    titulo("1. Formatacao e constantes do layout");
    CHECK(sizeof(Inodo) == 45, "Inodo tem 45 bytes");
    CHECK(SA_TAM_MAX_ARQUIVO == 544, "tamanho maximo de arquivo = 544");
    CHECK(livres() == (int)SA_NUM_BLOCOS, "apos formatar, todos os blocos estao livres");
    CHECK(SA_END_DADOS + SA_NUM_BLOCOS * SA_TAM_BLOCO <= MEM_TAMANHO,
          "a regiao de dados cabe na memoria");
}

static void teste_exemplo_enunciado(void)
{
    titulo("2. Exemplo do enunciado (UFSC / Fabio)");
    char buffer[70];
    ARQUIVO *A, *B, *C;

    A = meu_fopen("UFSC", "w");
    strcpy(buffer, "Oi mundo, teste de mensagemXXX");
    CHECK(meu_fwrite(A, (uint8_t *)buffer, strlen(buffer)) == 30, "UFSC: escreveu 30 bytes");
    meu_fclose(A);

    B = meu_fopen("Fabio", "w");
    strcpy(buffer, "Oi mundo, teste de mensagemXXX");
    meu_fwrite(B, (uint8_t *)buffer, strlen(buffer));
    strcpy(buffer, " Prof: FABIO");
    meu_fwrite(B, (uint8_t *)buffer, strlen(buffer));
    strcpy(buffer, " de la Rocha UFSC Ararangua");
    meu_fwrite(B, (uint8_t *)buffer, strlen(buffer));
    CHECK(meu_ftell(B) == 69, "Fabio: ftell = 69 depois das 3 escritas");
    meu_fclose(B);

    C = meu_fopen("Fabio", "r");
    CHECK(meu_fseek(C, 19, SEEK_SET) == 0, "fseek(19, SEEK_SET) ok");
    CHECK(meu_fread(C, (uint8_t *)buffer, 8) == 8, "fread de 8 bytes");
    buffer[8] = 0;
    CHECK(strcmp(buffer, "mensagem") == 0, "leu \"mensagem\"");
    meu_fclose(C);

    CHECK(livres() == (int)SA_NUM_BLOCOS - 3, "Fabio ocupa 3 blocos (1 indireto + 2 de dados); UFSC 0");
}

static void teste_posicao_eof_seek(void)
{
    titulo("3. ftell / feof / fseek");
    ARQUIVO *f = meu_fopen("Fabio", "r");
    CHECK(meu_ftell(f) == 0, "ftell inicial = 0");
    CHECK(meu_feof(f) == 0, "feof falso no inicio");
    CHECK(meu_fseek(f, 0, SEEK_END) == 0, "fseek(0, SEEK_END)");
    CHECK(meu_ftell(f) == 69, "ftell = tamanho");
    CHECK(meu_feof(f) != 0, "feof verdadeiro no fim");
    CHECK(meu_fseek(f, -9, SEEK_CUR) == 0, "fseek(-9, SEEK_CUR)");
    CHECK(meu_ftell(f) == 60, "ftell = 60");
    CHECK(meu_fseek(f, 70, SEEK_SET) == -1, "fseek alem do fim e rejeitado");
    CHECK(meu_ftell(f) == 60, "posicao nao muda apos fseek invalido");
    CHECK(meu_fseek(f, -1, SEEK_SET) == -1, "fseek para posicao negativa e rejeitado");
    CHECK(meu_fseek(f, 0, 99) == -1, "whence invalido e rejeitado");

    uint8_t buf[100];
    meu_fseek(f, 60, SEEK_SET);
    CHECK(meu_fread(f, buf, 50) == 9, "fread alem do fim devolve so o que resta (9)");
    CHECK(meu_feof(f) != 0, "feof verdadeiro depois de ler tudo");
    CHECK(meu_fread(f, buf, 10) == 0, "fread no fim devolve 0");
    meu_fclose(f);

    // limpa os arquivos do exemplo para os proximos testes comecarem com 12 inodos livres
    CHECK(meu_remove("UFSC") == 0 && meu_remove("Fabio") == 0, "remove UFSC e Fabio");
    CHECK(livres() == (int)SA_NUM_BLOCOS, "todos os blocos voltaram para a lista de livres");
}

static void teste_limite_544(void)
{
    titulo("4. Arquivo de tamanho maximo (544 bytes)");
    int antes = livres();
    CHECK(cria_arquivo("MAX", 544, 5, 50) == 544, "escreveu 544 bytes em pedacos de 50");
    CHECK(confere_arquivo("MAX", 544, 5), "conteudo de 544 bytes confere byte a byte");
    CHECK(antes - livres() == 17, "arquivo cheio usa 17 blocos (1 indireto + 16 de dados)");

    ARQUIVO *f = meu_fopen("MAX", "r+");
    meu_fseek(f, 0, SEEK_END);
    uint8_t x = 0x42;
    CHECK(meu_fwrite(f, &x, 1) == 0, "nao grava o byte 545");
    meu_fclose(f);
    CHECK(confere_arquivo("MAX", 544, 5), "arquivo continua intacto depois da tentativa");

    uint8_t grande[600];
    preenche(grande, 600, 9);
    f = meu_fopen("GRANDE", "w");
    CHECK(meu_fwrite(f, grande, 600) == 544, "fwrite de 600 bytes grava apenas 544");
    CHECK(meu_ftell(f) == 544, "posicao fica em 544");
    meu_fclose(f);
    CHECK(confere_arquivo("GRANDE", 544, 9), "conteudo dos 544 bytes confere");

    meu_remove("MAX");
    meu_remove("GRANDE");
}

static void teste_fronteiras_de_bloco(void)
{
    titulo("5. Fronteiras entre area direta, indireta e blocos");
    // tamanhos nas bordas: 32 (so direto), 33 (1o byte indireto), 64, 65, 543
    int tamanhos[] = {1, 31, 32, 33, 64, 65, 96, 543};
    char nome[16];
    for (unsigned i = 0; i < sizeof(tamanhos) / sizeof(tamanhos[0]); i++) {
        int n = tamanhos[i];
        int antes = livres();
        snprintf(nome, sizeof(nome), "T%d", n);
        int esperado_blocos = (n <= 32) ? 0 : 1 + (n - 32 + 31) / 32;
        char msg[80];
        snprintf(msg, sizeof(msg), "%d bytes: grava e le de volta igual", n);
        CHECK(cria_arquivo(nome, n, n, 7) == n && confere_arquivo(nome, n, n), msg);
        snprintf(msg, sizeof(msg), "%d bytes: usa %d bloco(s)", n, esperado_blocos);
        CHECK(antes - livres() == esperado_blocos, msg);
        meu_remove(nome);
        snprintf(msg, sizeof(msg), "%d bytes: remover devolve todos os blocos", n);
        CHECK(livres() == antes, msg);
    }
}

static void teste_modos(void)
{
    titulo("6. Modos de abertura e permissoes");
    uint8_t b[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    uint8_t l[8];

    CHECK(meu_fopen("NAOEXISTE", "r") == NULL, "\"r\" em arquivo inexistente -> NULL");
    CHECK(meu_fopen("NAOEXISTE", "r+") == NULL, "\"r+\" em arquivo inexistente -> NULL");
    CHECK(meu_fopen("X", "a") == NULL, "modo invalido -> NULL");
    CHECK(meu_fopen(NULL, "w") == NULL, "nome NULL -> NULL");
    CHECK(meu_fopen("A", NULL) == NULL, "modo NULL -> NULL");

    ARQUIVO *f = meu_fopen("MODOS", "w");
    CHECK(f != NULL, "\"w\" cria arquivo");
    CHECK(meu_fread(f, l, 8) == 0, "\"w\" nao permite leitura");
    CHECK(meu_fwrite(f, b, 8) == 8, "\"w\" permite escrita");
    meu_fclose(f);

    f = meu_fopen("MODOS", "r");
    CHECK(meu_fwrite(f, b, 8) == 0, "\"r\" nao permite escrita");
    CHECK(meu_fread(f, l, 8) == 8 && memcmp(b, l, 8) == 0, "\"r\" permite leitura");
    meu_fclose(f);

    f = meu_fopen("MODOS", "w");
    meu_fclose(f);
    f = meu_fopen("MODOS", "r");
    CHECK(meu_fread(f, l, 8) == 0 && meu_feof(f) != 0, "\"w\" em arquivo existente zera o conteudo");
    meu_fclose(f);

    CHECK(meu_ftell(NULL) == -1, "ftell(NULL) = -1");
    CHECK(meu_fread(NULL, l, 8) == 0, "fread(NULL) = 0");
    CHECK(meu_fwrite(NULL, b, 8) == 0, "fwrite(NULL) = 0");
    CHECK(meu_fclose(NULL) == -1, "fclose(NULL) = -1");

    meu_remove("MODOS");
}

static void teste_nomes(void)
{
    titulo("7. Nomes");
    CHECK(meu_fopen("", "w") == NULL, "nome vazio e rejeitado");
    CHECK(meu_fopen("123456789", "w") == NULL, "nome com 9 caracteres e rejeitado");

    ARQUIVO *f = meu_fopen("12345678", "w");
    CHECK(f != NULL, "nome com 8 caracteres (sem terminador no disco) e aceito");
    uint8_t x = 1;
    meu_fwrite(f, &x, 1);
    meu_fclose(f);
    f = meu_fopen("12345678", "r");
    CHECK(f != NULL, "nome de 8 caracteres e encontrado de novo");
    meu_fclose(f);

    cria_arquivo("AB", 10, 1, 10);
    cria_arquivo("ABC", 20, 2, 20);
    CHECK(confere_arquivo("AB", 10, 1), "\"AB\" nao se confunde com \"ABC\"");
    CHECK(confere_arquivo("ABC", 20, 2), "\"ABC\" nao se confunde com \"AB\"");
    CHECK(meu_fopen("ab", "r") == NULL, "nomes diferenciam maiusculas de minusculas");

    meu_remove("12345678");
    meu_remove("AB");
    meu_remove("ABC");
}

static void teste_r_mais(void)
{
    titulo("8. Modo r+ (sobrescrever e estender)");
    uint8_t esperado[200], lido[200], patch[20];
    CHECK(cria_arquivo("RMAIS", 100, 3, 100) == 100, "cria arquivo de 100 bytes");
    preenche(esperado, 100, 3);

    ARQUIVO *f = meu_fopen("RMAIS", "r+");
    CHECK(meu_ftell(f) == 0, "r+ comeca na posicao 0");
    memset(patch, 0xAA, sizeof(patch));
    meu_fseek(f, 40, SEEK_SET);
    CHECK(meu_fwrite(f, patch, 20) == 20, "sobrescreve 20 bytes no meio (cruza direto/indireto)");
    memcpy(esperado + 40, patch, 20);
    meu_fseek(f, 0, SEEK_SET);
    memset(lido, 0, sizeof(lido));
    CHECK(meu_fread(f, lido, 100) == 100 && memcmp(lido, esperado, 100) == 0,
          "conteudo bate e o tamanho continua 100");

    meu_fseek(f, 0, SEEK_END);
    memset(patch, 0xBB, 10);
    CHECK(meu_fwrite(f, patch, 10) == 10, "estende o arquivo no fim");
    memcpy(esperado + 100, patch, 10);
    meu_fseek(f, 0, SEEK_SET);
    memset(lido, 0, sizeof(lido));
    CHECK(meu_fread(f, lido, 200) == 110 && memcmp(lido, esperado, 110) == 0,
          "tamanho passou a 110 e o conteudo confere");
    meu_fclose(f);
    meu_remove("RMAIS");
}

static void teste_remocao_e_inodos(void)
{
    titulo("9. Remocao e limite de 12 inodos");
    int antes = livres();
    char nome[16];
    ARQUIVO *f;

    for (int i = 0; i < SA_NUM_INODOS; i++) {
        snprintf(nome, sizeof(nome), "F%02d", i);
        if (cria_arquivo(nome, 40, i, 40) != 40) {
            CHECK(false, "criou os 12 arquivos");
            for (int j = 0; j < i; j++) {
                snprintf(nome, sizeof(nome), "F%02d", j);
                meu_remove(nome);
            }
            return;
        }
    }
    CHECK(true, "criou os 12 arquivos");
    CHECK(meu_fopen("EXTRA", "w") == NULL, "o 13o arquivo e recusado (sem inodo livre)");
    CHECK(meu_remove("NAOEXISTE") == -1, "remover arquivo inexistente -> -1");

    CHECK(meu_remove("F05") == 0, "remove F05");
    CHECK(meu_fopen("F05", "r") == NULL, "F05 nao existe mais");
    f = meu_fopen("EXTRA", "w");
    CHECK(f != NULL, "o inodo liberado pode ser reaproveitado");
    meu_fclose(f);

    for (int i = 0; i < SA_NUM_INODOS; i++) {
        snprintf(nome, sizeof(nome), "F%02d", i);
        meu_remove(nome);
    }
    meu_remove("EXTRA");
    CHECK(livres() == antes, "depois de remover tudo, a lista de livres volta ao estado inicial");
}

static void teste_handles(void)
{
    titulo("10. Limite de arquivos abertos e dois handles no mesmo arquivo");
    ARQUIVO *h[9];
    char nome[16];
    int ok = 0;
    for (int i = 0; i < 8; i++) {
        snprintf(nome, sizeof(nome), "H%d", i);
        h[i] = meu_fopen(nome, "w");
        if (h[i] != NULL) ok++;
    }
    CHECK(ok == 8, "abre 8 arquivos ao mesmo tempo");
    h[8] = meu_fopen("H8", "w");
    CHECK(h[8] == NULL, "o 9o arquivo aberto e recusado");
    for (int i = 0; i < 8; i++) meu_fclose(h[i]);
    h[8] = meu_fopen("H8", "w");
    CHECK(h[8] != NULL, "depois de fechar, o slot e reaproveitado");
    meu_fclose(h[8]);
    for (int i = 0; i < 9; i++) {
        snprintf(nome, sizeof(nome), "H%d", i);
        meu_remove(nome);
    }

    // escritor e leitor no mesmo arquivo
    uint8_t a[10], b[10], l[10];
    preenche(a, 10, 1);
    preenche(b, 10, 2);
    ARQUIVO *W = meu_fopen("DUP", "w");
    ARQUIVO *R;
    meu_fwrite(W, a, 10);
    R = meu_fopen("DUP", "r");
    CHECK(meu_fread(R, l, 10) == 10 && memcmp(l, a, 10) == 0, "leitor enxerga o que o escritor gravou");
    CHECK(meu_feof(R) != 0, "leitor esta no fim");
    meu_fwrite(W, b, 10);
    CHECK(meu_feof(R) == 0, "depois de nova escrita o leitor ja nao esta no fim (inodo e relido)");
    CHECK(meu_fread(R, l, 10) == 10 && memcmp(l, b, 10) == 0, "leitor le os bytes novos");
    meu_fclose(W);
    meu_fclose(R);
    meu_remove("DUP");
}

static void teste_persistencia(void)
{
    titulo("11. Persistencia (reinicializar sem formatar)");
    CHECK(cria_arquivo("PERSIST", 200, 11, 33) == 200, "grava arquivo de 200 bytes");
    int antes = livres();
    inicializa_SA();                        // simula um novo boot: nao apaga nada
    CHECK(livres() == antes, "lista de blocos livres sobrevive a reinicializacao");
    CHECK(confere_arquivo("PERSIST", 200, 11), "arquivo sobrevive a reinicializacao");
    meu_remove("PERSIST");
}

static void teste_memoria_cheia(void)
{
    titulo("12. Memoria cheia");
    // Com so 12 inodos de 544 bytes o SA nunca encheria sozinho: ocupamos os blocos "na mao".
    int n = 0;
    while (sa_aloca_bloco() != SA_NIL) n++;
    CHECK(n == (int)SA_NUM_BLOCOS, "alocou exatamente SA_NUM_BLOCOS blocos");
    CHECK(sa_aloca_bloco() == SA_NIL, "sem blocos livres, aloca devolve SA_NIL");

    uint8_t buf[100];
    preenche(buf, 100, 4);
    ARQUIVO *f = meu_fopen("CHEIO", "w");
    CHECK(f != NULL, "ainda e possivel criar o inodo");
    int r = meu_fwrite(f, buf, 100);
    CHECK(r == 32, "so os 32 bytes da area direta foram gravados (sem blocos para o resto)");
    CHECK(meu_ftell(f) == 32, "posicao = 32");
    meu_fclose(f);
    f = meu_fopen("CHEIO", "r");
    uint8_t lido[100];
    CHECK(meu_fread(f, lido, 100) == 32 && memcmp(lido, buf, 32) == 0,
          "arquivo continua consistente: 32 bytes legiveis e corretos");
    meu_fclose(f);

    formata_SA();                           // devolve tudo
    CHECK(livres() == (int)SA_NUM_BLOCOS, "apos formatar de novo, todos os blocos voltam");
}

static void teste_integridade_lista(void)
{
    titulo("13. Integridade da lista encadeada apos varias operacoes");
    char nome[16];
    for (int rodada = 0; rodada < 5; rodada++) {
        for (int i = 0; i < 6; i++) {
            snprintf(nome, sizeof(nome), "R%d", i);
            cria_arquivo(nome, 30 + 90 * i, rodada + i, 17);
        }
        for (int i = 0; i < 6; i += 2) {
            snprintf(nome, sizeof(nome), "R%d", i);
            meu_remove(nome);
        }
        for (int i = 1; i < 6; i += 2) {
            snprintf(nome, sizeof(nome), "R%d", i);
            meu_remove(nome);
        }
    }
    CHECK(livres() == (int)SA_NUM_BLOCOS, "criar/remover em ciclos nao perde nem duplica blocos");
}

// ---------------------------------------------------------------------------
int main(void)
{
    printf("Testes do sistema de arquivos  (MEM_TAMANHO=%lu, blocos=%lu)\n",
           (unsigned long)MEM_TAMANHO, (unsigned long)SA_NUM_BLOCOS);

    inicializa_SA();
    formata_SA();

    teste_formatacao();
    teste_exemplo_enunciado();
    teste_posicao_eof_seek();
    teste_limite_544();
    teste_fronteiras_de_bloco();
    teste_modos();
    teste_nomes();
    teste_r_mais();
    teste_remocao_e_inodos();
    teste_handles();
    teste_persistencia();
    teste_memoria_cheia();
    teste_integridade_lista();

    printf("\n==============================\n");
    printf("%d verificacoes, %d falha(s)\n", total_checks, falhas);
    printf("%s\n", falhas == 0 ? "TUDO OK" : "HA FALHAS");
    return falhas == 0 ? 0 : 1;
}
