## Relatório Técnico – Estudo Inicial de Viabilidade para Rastreamento de Bovinos a Pasto com IoT
## Grupo: Leão de Berut
## Disciplina: Projeto Integrador / Estudo de Caso em IoT
## Tema: Monitoramento e Rastreamento de Bovinos a Pasto

## 1. Introdução
    O rastreamento e monitoramento de bovinos a pasto se tornou uma área estratégica no setor agropecuário, visando melhorar a gestão do rebanho, 
otimizar a alimentação, detectar doenças e reduzir perdas econômicas. Com o avanço da Internet das Coisas (IoT), é possível desenvolver soluções eficientes,
de baixo custo e adaptáveis às necessidades do campo.

    Este relatório apresenta uma análise inicial de documentos, tecnologias e tipos de monitoramento, com o objetivo de embasar a escolha de ferramentas e 
sensores para o projeto de uma plataforma IoT focada em bovinos a pasto.

## 2. Documentos e Estudos Relevantes sobre Rastreamento de Bovinos
Foram consultadas pesquisas acadêmicas, artigos técnicos e relatórios de casos reais de implementação de IoT no campo. Destacam-se:

  ## Estudo da Embrapa sobre uso de colares com sensores GPS para rastreamento de bovinos no Cerrado.
  ## Artigos do IEEE e Scielo sobre monitoramento remoto de rebanhos usando tecnologias LPWAN (LoRa e Sigfox).
  ## Projetos-piloto em fazendas no Brasil e Austrália, que usam sensores para detectar temperatura corporal, movimento e padrão de alimentação.

Esses documentos ressaltam a importância de integrar diferentes sensores com conectividade de longo alcance e baixo consumo,
principalmente em áreas onde não há infraestrutura de internet tradicional.

## 3. Tipos de Monitoramento e Rastreamento em Animais Selvagens e Bovinos
A abordagem usada em animais selvagens inspira parte das soluções aplicadas em bovinos. Veja as principais técnicas:

Animal / Contexto	Tecnologia Utilizada	Objetivo
Cervos e javalis (vida selvagem)	Coleiras GPS + rádio VHF	Entendimento de movimentação e habitat
Gado em fazendas	GPS + LoRa + sensores de movimento	Rastreamento, detecção de doenças e quedas
Antílopes em parques	Etiquetas RFID + drones	Rastreamento remoto e não intrusivo
Pasto inteligente (Smart Pasture)	Sensores no solo + coleiras	Otimização da pastagem e bem-estar animal
As tecnologias de rastreamento adaptadas para gado devem considerar: durabilidade, autonomia de bateria, resistência climática e integração com rede de dados.

## 4. Tecnologias de Viabilidade para IoT em Rastreamento Animal
Abaixo, apresentamos os principais elementos tecnológicos analisados para o sistema:

🟩 Microcontroladores e Módulos
ESP32 LoRa: Ideal por seu custo, Wi-Fi/LoRa integrado e suporte a sensores diversos.
Arduino + Shield LoRa: Alternativa modular com ampla documentação.

🟩 Sensores
Temperatura Corporal (MLX90614) – sem contato, ideal para coleiras.
Acelerômetro (MPU6050) – detecção de movimento, quedas e repouso.
Sensor de Solo (capacitivo) – análise da umidade do pasto.
Módulo GPS (NEO-6M) – rastreamento de localização em tempo real.

🟩 Conectividade
LoRa: Comunicação de longo alcance (~2-10 km), ideal para áreas rurais.
Gateways LoRaWAN: Conectam os sensores à nuvem ou servidor.
Plataformas de dados: Firebase, Node-RED, Grafana, AWS IoT.

## 5. Considerações Finais
A aplicação da IoT no rastreamento de bovinos oferece ganhos consideráveis em produtividade, bem-estar animal e prevenção de perdas. Com o uso de sensores apropriados e comunicação eficiente via LoRa, é possível desenvolver uma plataforma robusta e de baixo custo.

As tecnologias estudadas são viáveis tanto tecnicamente quanto economicamente para um projeto universitário, com espaço para expansão e aplicação no mundo real. O próximo passo será prototipar os sensores selecionados e testar a conectividade em campo.

## Referencias
    https://www.embrapa.br/busca-de-noticias/-/noticia/63903853/internet-das-coisas-monitora-produtividade-e-bem-estar-animal-em-sistemas-de-ilpf
    https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1108706/1/5050.pdf


