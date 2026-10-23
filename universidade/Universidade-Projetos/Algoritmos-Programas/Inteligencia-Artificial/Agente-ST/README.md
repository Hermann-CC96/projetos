**Agente Inteligente de Manutenção Industrial (Agente-ST)**

## 📝 Descrição do Projeto
Este projeto consiste no desenvolvimento de um Agente Inteligente voltado para o setor industrial,
focado em manutenção preventiva. O objetivo é simular uma interface homem-máquina onde o agente 
recebe dados de sensores ou relatos de operadores e utiliza um Modelo de Linguagem de Grande Escala (LLM)
para fornecer soluções instantâneas e gerenciar o status de ativos industriais. 
    O projeto aplica conceitos fundamentais de Processamento de Linguagem Natural (PLN), especificamente a 
análise semântica (atribuição de significado à estrutura das frases) e pragmática (ajuste do significado ao 
contexto industrial específico).

## ⚙️ Funcionalidades Mínimas
**Entrada de Texto:** Interface para o usuário reportar estados de máquinas ou dúvidas técnicas.

**Processamento LLM:** Utilização de inteligência artificial para interpretar a necessidade do 
usuário com base em uma base de conhecimento.

**Manutenção de Contexto:** O agente é capaz de manter a memória da conversa, permitindo um diálogo 
fluido sobre o estado do ativo.

**Modos de Operação:** Simulação dos modos manual, semi-automatizado e automatizado conforme planejado
na arquitetura do sistema.
    
## 🛠️ Tecnologias Utilizadas
**Python:** Linguagem principal para a lógica do agente e integração.

**LLM (OpenAI API / Ollama):** Para o processamento e geração de respostas em linguagem natural.

**Lógica de Gramática:** Inspirado em gramáticas de cláusulas definidas para estruturação de dados.


## 🚀 Instruções de Execução
1. Clone este repositório.

2. Instale as dependências necessárias: pip install openai.

3. Configure sua chave de API no script principal.

4. Execute o comando: python Agente-ST.py

## 📚 Fundamentação Teórica (PLN)
De acordo com Silvio do Lago Pereira, o PLN envolve diferentes níveis de análise que este agente 
busca mimetizar:
Morfologia: Reconhecimento das unidades primitivas das palavras técnicas.
Sintaxe: Estruturação correta das frases para comandos do operador.
Semântica e Pragmática: Essenciais para que o chatbot entenda que "aquecimento excessivo" no contexto 
predador-presa seria irrelevante, mas no contexto industrial significa uma falha crítica.


## 🚀 Link do video
Link: https://www.loom.com/looms/videosR

