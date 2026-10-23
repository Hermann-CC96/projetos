import random

#CONSTANTES DO JOGO
VAZIO = ' '
TABULEIRO = [VAZIO] * 16
CONDICOES_VITORIA = [
    [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15],  #Linhas
    [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15],  #Colunas
    [0, 5, 10, 15], [3, 6, 9, 12]  #Diagonais
]

Dificuldades = { 
    'Fácil': 1,
    'Médio': 3,
    'Difícil': 5
}

#FUNÇÃO PARA EXIBIR O TABULEIRO
def exibir_tabuleiro():
    print("\n")
    for i in range(0, 16, 4):
        print(f" {TABULEIRO[i]} | {TABULEIRO[i+1]} | {TABULEIRO[i+2]} | {TABULEIRO[i+3]}")
        if i < 12: 
            print("---+---+---+---")
    print("\n")

#Função para escolher os jogadores
def Jogadores():
    global HUMANO, COMPUTADOR
    escolha = input("Escolha seu símbolo (X/O): ").upper()
    while escolha not in ['X', 'O']:
        print("Símbolo inválido. Tente novamente.")
        escolha = input("Escolha seu símbolo (X/O): ").upper()
    if escolha == 'X':
        HUMANO = 'X'
        COMPUTADOR = 'O'
    else:
        HUMANO = 'O'
        COMPUTADOR = 'X'

#Acão:  retona o conjunto de jogadas possíveis para o jogador atual
def Acao(tabuleiro):
    acoes = []
    for i in range(len(tabuleiro)):
        if tabuleiro[i] == VAZIO:
            acoes.append(i)
    return acoes
    
#Resultado: retorna o estado do tabuleiro após a execução de uma jogada
def resultado(tabuleiro, acao, jogador):
    novo_tabuleiro = tabuleiro.copy() 
    novo_tabuleiro[acao] = jogador
    return novo_tabuleiro

#Teste de término: verifica se o jogo terminou (vitória ou empate)
def Teste__termino():
    return verificar_vitoria(TABULEIRO, HUMANO) or verificar_vitoria(TABULEIRO, COMPUTADOR) or verificar_empate(TABULEIRO)

#Utlidade: função para calcular a utilidade do estado do jogo
def Utilidade(tabuleiro):
    if verificar_vitoria(tabuleiro, COMPUTADOR):
        return 10
    elif verificar_vitoria(tabuleiro, HUMANO):
        return -10
    else:
        return 0

#Minimax: avalia as melhores jogadas possíveis para o computador, considerando as jogadas
#futuras e suas consequências para o computador, maximizando suas chances de vitória e minimizando
#as chances do jogador humano vencer.
def Minimax(tabuleiro, profundidade, maximizando, limite_profundidade):
    
    if verificar_vitoria(tabuleiro, COMPUTADOR):
        return 10 - profundidade 
    if verificar_vitoria(tabuleiro, HUMANO):
        return profundidade - 10
    if verificar_empate(tabuleiro) or profundidade >= limite_profundidade:
        return Utilidade(tabuleiro) 

    if maximizando:
        melhor_valor = float('-inf')
        for acao in Acao(tabuleiro):
            valor = Minimax(resultado(tabuleiro, acao, COMPUTADOR), profundidade + 1, False, limite_profundidade)
            if valor is not None:
                melhor_valor = max(melhor_valor, valor) # 
        return melhor_valor
    else:
        melhor_valor = float('inf')
        for acao in Acao(tabuleiro):
            valor = Minimax(resultado(tabuleiro, acao, HUMANO), profundidade + 1, True, limite_profundidade) # Chamada recursiva para avaliar a jogada do jogador humano
            if valor is not None:
                melhor_valor = min(melhor_valor, valor) #
        return melhor_valor

#FUNÇÃO PARA AÇÃO DO COMPUTADOR
def jogada_computador(dificuldade):
    melhor_valor = float('-inf')
    melhor_acao = None
    for acao in Acao(TABULEIRO):
        valor = Minimax(resultado(TABULEIRO, acao, COMPUTADOR), 0, False, Dificuldades[dificuldade]) #Chamada para avaliar a jogada do computador, considerando a dificuldade escolhida
        if valor > melhor_valor:
            melhor_valor = valor
            melhor_acao = acao
    if melhor_acao is not None:
        TABULEIRO[melhor_acao] = COMPUTADOR

#FUNÇÃO PARA AÇÃO DO JOGADOR HUMANO
def jogada_humana():
    while True:
        try:
            posicao = int(input("Escolha uma posição (1-16): ")) - 1
            if posicao < 0 or posicao > 15:
                print("Posição inválida. Tente novamente.")
            elif TABULEIRO[posicao] != VAZIO:
                print("Posição já ocupada. Tente novamente.")
            else:
                TABULEIRO[posicao] = HUMANO
                break
        except ValueError:
            print("Entrada inválida. Digite um número entre 1 e 16.")

#FUNÇÃO PARA VERIFICAR VITÓRIA
def verificar_vitoria(tabuleiro_checar, jogador):
    for condicao in CONDICOES_VITORIA:
        if all(tabuleiro_checar[i] == jogador for i in condicao):
            return True
    return False

#FUNÇÃO PARA VERIFICAR EMPATE
def verificar_empate(tabuleiro_checar):
    return all(celula != VAZIO for celula in tabuleiro_checar)


#FUNÇÃO PRINCIPAL DO JOGO
def main():
    Jogadores()
    dificuldade = input("Escolha a dificuldade (Fácil, Médio, Difícil): ")
    while dificuldade not in Dificuldades:
        print("Dificuldade inválida. Tente novamente.")
        dificuldade = input("Escolha a dificuldade (Fácil, Médio, Difícil): ")

    while not Teste__termino():
        exibir_tabuleiro()
        jogada_humana()
        if Teste__termino():
            break
        jogada_computador(dificuldade)

    exibir_tabuleiro()
    if verificar_vitoria(TABULEIRO, HUMANO):
        print("Parabéns! Você venceu!")
    elif verificar_vitoria(TABULEIRO, COMPUTADOR):
        print("O computador venceu! Tente novamente.")
    else:
        print("Empate! Ninguém venceu.")

if __name__ == "__main__":
    main()