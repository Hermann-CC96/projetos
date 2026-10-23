async function sucesso(decodedText) {
    // 1. Preenche o input correto com o texto do QR Code
    document.getElementById("resultado").value = decodedText;

    // Opcional: Para o scanner para não ler várias vezes seguidas o mesmo código
    try {
        await html5QrCode.stop();
        console.log("Scanner parado para processamento.");
    } catch (err) {
        console.warn("Erro ao parar o scanner:", err);
    }

    // 2. Envia para o banco de dados
    const resultado = await salvarQRCode(decodedText);

    if (resultado.sucesso) {
        document.getElementById("mensagem").innerHTML = `
        <div class="alert alert-success mt-3">
             QR Code salvo com sucesso!
        </div>`;
    } else {
        document.getElementById("mensagem").innerHTML = `
        <div class="alert alert-danger mt-3">
             Erro ao escanear: ${resultado.mensagem}
        </div>`;
    }
}

function erro(error) {
    // Ignorar erros de leitura automática do scanner
}

// Inicialização do leitor
const html5QrCode = new Html5Qrcode("reader");

// Substitua o bloco html5QrCode.start por este:
html5QrCode.start(
  { facingMode: "environment" }, 
  {
    fps: 10, 
    qrbox: { width: 250, height: 250 }
  },
  // Callback de Sucesso Direto:
  async (decodedText) => {
      console.log("QR Code detectado pelo scanner:", decodedText);
      
      // Força o preenchimento do input na tela
      const inputResultado = document.getElementById("resultado");
      if (inputResultado) {
          inputResultado.value = decodedText;
      }
      
      // Executa a sua função sucesso para salvar no banco
      await sucesso(decodedText);
  },
  (errorMessage) => {
      // Ignora erros normais de busca por frame
  }
).catch((err) => {
    console.error("Erro ao iniciar a câmera: ", err);
});

document.getElementById("salvarBtn").addEventListener("click", async () => {
    const textoDoInput = document.getElementById("resultado").value;
    
    if (!textoDoInput) {
        alert("Por favor, insira ou escaneie um código primeiro!");
        return;
    }

    const resultado = await salvarQRCode(textoDoInput);

    if (resultado.sucesso) {
        document.getElementById("mensagem").innerHTML = `
            <div class="alert alert-success mt-3">
                 QR Code salvo com sucesso!
            </div>`;
    } else {
        document.getElementById("mensagem").innerHTML = `
            <div class="alert alert-danger mt-3">
                 Erro ao salvar: ${resultado.mensagem}
            </div>`;
    }
});