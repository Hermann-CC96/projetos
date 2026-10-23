# Sistema de Arquivos Embarcado baseado em Inode

Este projeto consiste no desenvolvimento de um **Sistema de Arquivos inspirado em Inodes** para dispositivos embarcados, utilizando memória EEPROM I2C (como a AT24C512) como suporte físico de armazenamento. O sistema foi estruturado de forma modular para desacoplar a lógica de alto nível da persistência física e facilitar a validação em ambiente de desenvolvimento.

---

## 1. Visão Geral e Arquitetura em Camadas

O projeto foi desacoplado em camadas lógicas distintas para isolar a aplicação final das regras de gerenciamento de blocos e persistência física:

* **Camada 3 - Aplicação (`main.cpp`):** Responsável pelos testes de rotina do usuário, englobando cenários de formatação, listagem, escrita, leitura e movimentação de ponteiros.
* **Camada 4 - Sistema de Arquivos de Alto Nível (`sa_api.cpp`, `sa_api.h`):** Fornece a interface com o programador através de chamadas inspiradas na biblioteca padrão de arquivos (`meu_fopen`, `meu_fwrite`, `meu_fread`, `meu_fseek`, `meu_fclose`, etc.).
* **Camada 5 - Sistema de Arquivos de Baixo Nível (`sa.cpp`, `sa.h`):** Gerencia a lógica interna do sistema, controle de alocação de blocos e resolução de ponteiros na memória.
* **Camada 2 - Memória (`memoria.cpp`, `memoria.h`):** Camada de abstração de hardware responsável pela configuração de barramento e operações sequenciais de leitura/escrita de bytes.

---

## 2. Layout da Memória e Estrutura de Inodos

O particionamento lógico da memória foi desenhado para otimizar o espaço reduzido de EEPROMs I2C (como a AT24C512):

* **Cabeçalho da Partição (2 Bytes):** Armazena o endereço do primeiro bloco de dados livre disponível para alocação.
* **Tabela de Inodos (Entradas de Arquivos):**
  * Total de **12 entradas** estáticas para gerenciamento de arquivos.
  * **Status (1 byte):** Indica se o inodo está livre (`0`) ou ocupado (`1`).
  * **Nome (8 bytes):** Identificador textual do arquivo (strings de até 8 caracteres).
  * **Tamanho (2 bytes):** Comprimento atual do arquivo em bytes.
  * **Ponteiro Direto (2 bytes):** Referência ao primeiro bloco de dados alocado.
  * **Ponteiro Indireto (2 bytes):** Endereço de um bloco encadeado que aponta para expansões de dados subsequentes.

---

## 3. Especificação da API (`sa_api.cpp`)

### Gerenciamento e Estrutura Inicial
* `inicializa_SA()` / `formata_SA()`: Inicializam os descritores internos e preenchem a partição com os valores padrão de fábrica.
* `lista_todos()`: Varre a tabela de inodos imprimindo no console o nome, status e tamanho dos arquivos presentes.

### Manipulação de Arquivos
* `meu_fopen(nome, modo)`: Abre ou cria arquivos de acordo com o modo especificado (`r`, `w`, etc.), buscando entradas livres na tabela de inodos.
* `meu_fwrite(A, buffer, tam)` / `meu_fread(C, buffer, tam)`: Realizam a transferência em lote de blocos de dados, otimizando o desempenho de I/O.
* `meu_fseek(C, deslocamento, origem)`: Reposiciona o cursor lógico de leitura/escrita dentro do arquivo ativo.
* `meu_fclose(A)`: Sincroniza os metadados pendentes e libera o descritor na tabela de arquivos abertos.

---

## 4. Estratégia de Emulação e Validação no Ambiente Linux

Para acelerar o ciclo de depuração e evitar gravações excessivas desnecessárias na memória física durante a fase de testes, o subsistema de memória foi adaptado para operar em cima de um arquivo binário local simulando a partição (`PARTICAO.BIN`):

* `memoria_init()`: Cria ou carrega o arquivo no diretório de trabalho do host (`PARTICAO.BIN`).
* `memoria_fwrite()` / `memoria_fread()`: Traduzem as chamadas de barramento para funções padrão de manipulação de arquivos em C (`fseek`, `fread`, `fwrite`).
* **Inspeção de Binários:** O conteúdo estruturado da partição simulada pode ser inspecionado diretamente a qualquer momento através de utilitários como o `hexdump`.
