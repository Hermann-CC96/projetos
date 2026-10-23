// ============================================================================
//  Camada 2 - MEMORIA (versao ESP32 + EEPROM I2C AT24C512 / AT24C256)
//
//  Baseada no codigo de aula (Memoria_I2C/teste/main/teste.c), usando o driver
//  novo do IDF (driver/i2c_master.h).
//
//  Ligacao:   EEPROM pino 5 (SDA) -> GPIO 23       EEPROM pino 6 (SCL) -> GPIO 22
//             A0, A1, A2, WP e GND -> GND   (endereco I2C = 0x50)
//             VCC -> 3,3 V
//             Pull-up: resistores de ~4,7k em SDA e SCL para 3,3 V. Se nao tiver,
//             o codigo habilita os pull-ups internos do ESP32 (funciona em fio curto).
// ============================================================================
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "driver/i2c_master.h"
#include "esp_err.h"
#include "memoria.h"

#define PINO_SDA        GPIO_NUM_23
#define PINO_SCL        GPIO_NUM_22
#define ENDERECO_I2C    0x50
#define VELOCIDADE_I2C  100000        // 100 kHz

// Uma escrita em "pagina" nao pode cruzar o limite da pagina da EEPROM; se cruzar,
// o endereco da a volta e sobrescreve o INICIO da mesma pagina.
//   AT24C512: pagina de 128 B     AT24C256: pagina de 64 B
// Usamos 64 para funcionar nos dois chips.
#define TAM_PAGINA      64

#define TAM_MAX_LEITURA 64

static i2c_master_bus_handle_t bus;
static i2c_master_dev_handle_t dev;
static bool iniciado = false;

// Depois de uma escrita a EEPROM fica ocupada (ate 5 ms) e nao responde ao seu
// endereco (NACK). Fazemos "ACK polling": tentamos ate ela responder.
static void aguarda_fim_da_escrita(void)
{
    for (int tentativa = 0; tentativa < 500; tentativa++) {
        if (i2c_master_probe(bus, ENDERECO_I2C, 10) == ESP_OK) return;
        usleep(100);
    }
    printf("AVISO: EEPROM nao respondeu (confira fios e pull-ups)\n");
}

void memoria_init(void)
{
    if (iniciado) return;

    i2c_master_bus_config_t cfg_bus = {};
    cfg_bus.i2c_port = I2C_NUM_0;
    cfg_bus.sda_io_num = PINO_SDA;
    cfg_bus.scl_io_num = PINO_SCL;
    cfg_bus.clk_source = I2C_CLK_SRC_DEFAULT;
    cfg_bus.glitch_ignore_cnt = 7;
    cfg_bus.flags.enable_internal_pullup = true;
    ESP_ERROR_CHECK(i2c_new_master_bus(&cfg_bus, &bus));

    i2c_device_config_t cfg_dev = {};
    cfg_dev.dev_addr_length = I2C_ADDR_BIT_LEN_7;
    cfg_dev.device_address = ENDERECO_I2C;
    cfg_dev.scl_speed_hz = VELOCIDADE_I2C;
    ESP_ERROR_CHECK(i2c_master_bus_add_device(bus, &cfg_dev, &dev));

    iniciado = true;

    if (i2c_master_probe(bus, ENDERECO_I2C, 100) != ESP_OK)
        printf("AVISO: EEPROM nao encontrada no endereco 0x%02X\n", ENDERECO_I2C);
}

void memoria_fwrite(const void *buffer, uint16_t posicao, uint16_t tam)
{
    const uint8_t *p = (const uint8_t *)buffer;
    uint32_t end = posicao;

    while (tam > 0) {
        // quantos bytes cabem ate o fim da pagina atual
        uint16_t espaco = TAM_PAGINA - (end % TAM_PAGINA);
        uint16_t n = (tam < espaco) ? tam : espaco;

        uint8_t pacote[2 + TAM_PAGINA];
        pacote[0] = (uint8_t)(end >> 8);        // endereco de 16 bits, byte alto primeiro
        pacote[1] = (uint8_t)(end & 0xFF);
        memcpy(pacote + 2, p, n);

        ESP_ERROR_CHECK(i2c_master_transmit(dev, pacote, n + 2, 100));
        aguarda_fim_da_escrita();               // so segue quando o chip terminar de gravar

        p += n;
        end += n;
        tam -= n;
    }
}

void memoria_fread(void *buffer, uint16_t posicao, uint16_t tam)
{
    uint8_t *p = (uint8_t *)buffer;
    uint32_t end = posicao;

    while (tam > 0) {
        uint16_t n = (tam < TAM_MAX_LEITURA) ? tam : TAM_MAX_LEITURA;

        uint8_t endereco[2] = { (uint8_t)(end >> 8), (uint8_t)(end & 0xFF) };
        // "random read": envia o endereco e le n bytes em sequencia (o chip incrementa sozinho)
        ESP_ERROR_CHECK(i2c_master_transmit_receive(dev, endereco, 2, p, n, 100));

        p += n;
        end += n;
        tam -= n;
    }
}
