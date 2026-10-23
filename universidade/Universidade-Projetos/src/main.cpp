// ============================================================================
//  Camada 5 - APLICACAO (teste do sistema de arquivos)
//  E o exemplo do enunciado. O mesmo arquivo compila no Linux (main) e no
//  ESP32 (app_main): a macro ESP_PLATFORM e definida automaticamente pelo IDF.
// ============================================================================
#include <stdio.h>
#include <string.h>
#include "sa_api.h"

#ifdef ESP_PLATFORM
  #include "freertos/FreeRTOS.h"
  #include "freertos/task.h"
#endif

static int principal(void)
{
    char buffer[70];
    int a;
    ARQUIVO *A, *B, *C;

    printf("Tecle [ENTER] para iniciar\n");
    while (1) {
        a = getchar();
        if (a == 13 || a == 10) break;          // aceita CR (monitor serial) e LF (terminal Linux)
        if (a == EOF) {
#ifdef ESP_PLATFORM
            vTaskDelay(pdMS_TO_TICKS(20));      // na serial do ESP32 getchar() nao bloqueia: espera um pouco
#else
            break;                              // Linux: entrada fechada/redirecionada, nao ha ENTER a esperar
#endif
        }
    }
    printf("OK\n");

    inicializa_SA();
    formata_SA();           // realizado apenas 1 vez

    A = meu_fopen("UFSC", "w");
    strcpy(buffer, "Oi mundo, teste de mensagemXXX");
    meu_fwrite(A, (uint8_t *)buffer, strlen(buffer));
    meu_fclose(A);

    B = meu_fopen("Fabio", "w");
    strcpy(buffer, "Oi mundo, teste de mensagemXXX");
    meu_fwrite(B, (uint8_t *)buffer, strlen(buffer));

    strcpy(buffer, " Prof: FABIO");
    meu_fwrite(B, (uint8_t *)buffer, strlen(buffer));

    strcpy(buffer, " de la Rocha UFSC Ararangua");
    meu_fwrite(B, (uint8_t *)buffer, strlen(buffer));
    meu_fclose(B);

    C = meu_fopen("Fabio", "r");
    meu_fseek(C, 19, SEEK_SET);
    meu_fread(C, (uint8_t *)buffer, 8);
    buffer[8] = 0;
    printf("Lido=%s\n", buffer);
    meu_fclose(C);

    lista_todos();
    mostra_bytes_arquivo("Fabio");      // extra: dump hexadecimal para conferir o conteudo

    return 0;
}

#ifdef ESP_PLATFORM
extern "C" void app_main(void)
{
    principal();
    while (1) vTaskDelay(pdMS_TO_TICKS(1000));  // evita o watchdog e nao reinicia a placa
}
#else
int main(void)
{
    return principal();
}
#endif
