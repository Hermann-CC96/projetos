// ============================================================================
//  Camada 2 - MEMORIA
//  Interface unica usada pelo sistema de arquivos para acessar "o chip".
//  Existem DUAS implementacoes com exatamente estes nomes:
//     linux/memoria_linux.cpp       -> emula a memoria usando um arquivo (PARTICAO.BIN)
//     esp32/main/memoria_esp32.cpp  -> acessa a EEPROM I2C (AT24C512 / AT24C256)
// ============================================================================
#ifndef MEMORIA_H
#define MEMORIA_H

#include <stdint.h>

// Tamanho total do chip em bytes.
//   AT24C512 = 65536   (padrao)
//   AT24C256 = 32768   (compile com -DMEM_TAMANHO=32768UL)
#ifndef MEM_TAMANHO
#define MEM_TAMANHO 32768UL
#endif

// Prepara a memoria (abre o arquivo no Linux / configura o I2C no ESP32).
void memoria_init(void);

// Escreve 'tam' bytes de 'buffer' a partir do endereco 'posicao' da memoria.
void memoria_fwrite(const void *buffer, uint16_t posicao, uint16_t tam);

// Le 'tam' bytes a partir do endereco 'posicao' para dentro de 'buffer'.
void memoria_fread(void *buffer, uint16_t posicao, uint16_t tam);

#endif
