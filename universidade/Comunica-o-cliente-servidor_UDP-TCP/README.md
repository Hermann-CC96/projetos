# Projeto "Ping Pong" UDP e TCP em Python
Este repositório contém a implementação de um programa "Ping Pong" baseado em cliente-servidor, inicialementea
a criação de scriputilizando o protocolo UDP e, posteriormente, adaptando para o protocolo TCP. O projeto tem como objetivo
demostrar a comunicação de socket em python. O calculo do tempo de viagem ida e volta (RTT) e o tratamento 
do pacote perdido em UDP. Ele serve como atividade para Rede de Computadores na Universidade Federal de Santa Catarina (UFSC).

Descrição

Nesse projecto o foco foi criar um sistema cliente - servidor com protocolo UDP e TCP que permite a comunicação 
entre dois host distinto, porém na mesmo rede. 

A solução baseada na conexão UDP, foi devidida em dois grande parte:

   1 - Código do Servidor UDP (server.py)
   
          Este código Python implementa o lado do servidor do programa "ping" baseado em UDP. Ele aguarda por
          
          mensagens "ping" do cliente e responde com mensagens "pong".
          
   2 - Código do Cliente UDP (client.py)
   
          Este código Python implementa o lado do cliente do programa "ping" baseado em UDP. Ele envia 10 mensagens "ping"
          
          ao servidor, mede o RTT e lida com pacotes perdidos.
          
Em seguida, emplementação de modificaçoes para TCP, o mesmo em duas maquinas diferentes.
    

Odoncol-amigável
