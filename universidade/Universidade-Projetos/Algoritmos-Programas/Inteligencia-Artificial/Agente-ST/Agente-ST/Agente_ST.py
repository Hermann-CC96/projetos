import openai

class AgenteIndustrialLLM:
    def __init__(self):

        self.client = openai.OpenAI(
            base_url="http://localhost:11434/v1/",
            api_key="ollama" 
        )
        self.contexto_manutencao = """
        Você é um Agente Inteligente Industrial. 
        Seu foco é manutenção preventiva. 
        Dados do Ativo no CMDB: ID TRB-402, Local: Setor A.
        Base de Conhecimento: 
        - Aquecimento > 80°C: Reduzir carga.
        - Vibração > 5mm/s: Lubrificar eixos.
        - Ruído > 70dB: Verificar rolamentos.
        - Histórico: Última manutenção em 2024-05-01, sem falhas reportadas.
        - Diagnóstico de status: Temperatura atual 85°C, Vibração 6mm/s, Ruído 75dB.
        - Recomendações: Agendar manutenção imediata, priorizar verificação de rolamentos e lubrificação.
        - se a pressão for maior que 10bar, verificar válvulas de segurança e possíveis vazamentos.
        """
        self.historico = [{"role": "system", "content": self.contexto_manutencao}]

    def responder(self, entrada_usuario):
        if not entrada_usuario.strip():
            return "Erro: Entrada vazia."

        self.historico.append({"role": "user", "content": entrada_usuario})

        try:
            response = self.client.chat.completions.create(
                model="gemma:2b",
                messages=self.historico
            )
            resposta = response.choices[0].message.content
            self.historico.append({"role": "assistant", "content": resposta})
            return resposta
        except Exception as e:
            return f"Erro ao conectar com o Ollama local: {e}"

# --- Simulação de Uso ---
def simular_chat():
    meu_agente = AgenteIndustrialLLM()
    print("=== Sistema Industrial (MODO LOCAL: OLLAMA) ===")
    while True:
        user_input = input("\nOperador (ou sensor): ")
        if user_input.lower() in ["sair", "exit"]:
            break
        resposta = meu_agente.responder(user_input)
        print(f"Agente: {resposta}")

if __name__ == "__main__":
    simular_chat()