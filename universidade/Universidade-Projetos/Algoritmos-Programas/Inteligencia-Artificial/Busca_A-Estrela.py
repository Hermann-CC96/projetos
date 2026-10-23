import math

# Classe que representa cada ponto (cidade/ponto de conexão) no mapa
class Node:
    def __init__(self, nome, h):
        self.nome = nome
        self.h = h  
        self.g = float('inf')  
        self.f = float('inf')  
        self.parent = None   

    def __repr__(self):
        return self.nome

def A_Estrela_Com_Log(inicio, meta, grafo, nós):
    abrirList = [inicio]
    fecharList = []

    # Configurações do nó de partida
    inicio.g = 0
    inicio.f = inicio.h

    print(f"--- Iniciando busca de {inicio.nome} para {meta.nome} ---")

    while abrirList:
        # Sempre escolhe o nó com o MENOR valor de 'f'
        no_atual = min(abrirList, key=lambda n: n.f)
        
        print(f"\n[Analisando]:\n {no_atual.nome} (f: {no_atual.f:.1f}, g: {no_atual.g}, h: {no_atual.h})")

        # Verifica se o nó atual é o objetivo final
        if no_atual.nome == meta.nome:
            print(f"Meta atingida!")
            return reconstruir_path(no_atual)

        # Move o nó da lista de espera (aberta) para a de concluídos (fechada)
        abrirList.remove(no_atual)
        fecharList.append(no_atual)

        # Verifica todos os vizinhos conectados ao nó atual no grafo
        for nome_vizinho, custo_aresta in grafo[no_atual.nome].items():
            vizinho = nós[nome_vizinho]

            # Se o vizinho já foi analisado, ignoramos
            if vizinho in fecharList:
                continue

            # Calcula o custo 'g' provisório: custo do nó atual + peso da aresta (estrada)
            tentative_g = no_atual.g + custo_aresta

            # Se o vizinho é novo ou se encontramos um caminho mais curto até ele
            if vizinho not in abrirList:
                abrirList.append(vizinho)
                print(f"  -> Novo nó descoberto: {vizinho.nome}")
            elif tentative_g >= vizinho.g:
                continue

            # ESTA É A PARTE ONDE O ALGORITMO APRENDE:
            # Registra o 'pai' para saber de onde veio e atualiza os custos matemáticos
            vizinho.parent = no_atual
            vizinho.g = tentative_g
            vizinho.f = vizinho.g + vizinho.h
        print(f"     Calculando: f({vizinho.nome}) = g({vizinho.g}) + h({vizinho.h}) = {vizinho.f}")

    return "Caminho não encontrado"

def reconstruir_path(no_atual):
    # Segue o rastro dos 'parents' do destino até a origem
    caminho = []
    while no_atual:
        caminho.append(no_atual.nome)
        no_atual = no_atual.parent
    return " -> ".join(caminho[::-1]) # Inverte a lista para mostrar Início -> Fim

#CONFIGURAÇÃO DO CENÁRIO 
#O "palpite" de distância de cada ponto até Floripa (Heurística)
h_valores = {
    'Araranguá': 213, 'A': 90, 'B': 100, 'C': 80, 'D': 90, 
    'E': 50, 'F': 50, 'G': 60, 'Floripa': 0
}

# Criamos os objetos Node para cada localidade
nós = {nome: Node(nome, h) for nome, h in h_valores.items()}

# grafo: Representa o mapa real com as distâncias das estradas (Custo g)
grafo = {
    'Araranguá': {'A': 90, 'B': 150, 'C': 80},
    'A': {'D': 95, 'Araranguá': 90, 'B': 150, 'C': 80},
    'B': {'A': 150, 'C': 77, 'F': 100, 'Araranguá': 150},
    'C': {'A': 80, 'B': 77, 'D': 70, 'E': 112, 'Araranguá': 80},
    'D': {'A': 95, 'C': 70, 'E': 120},
    'E': {'C': 112, 'D': 120, 'F': 50, 'G': 50, 'Floripa': 105},
    'F': {'B': 100, 'E': 50},
    'G': {'E': 50, 'Floripa': 105},
    'Floripa': {}
}

# Execução do Algoritmo
resultado = A_Estrela_Com_Log(nós['Araranguá'], nós['Floripa'], grafo, nós)
print(f"\n RESULTADO FINAL (A ROTA MAIS OTIMIZADA):")
print(resultado)