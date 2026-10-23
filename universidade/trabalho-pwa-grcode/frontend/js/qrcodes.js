document.addEventListener("DOMContentLoaded", () => {
    carregarLista();
    
    // Gatilho de segurança: ativa o push se o usuário carregar direto a tela de listagem
    if (typeof inicializarPushNotification === "function") {
        inicializarPushNotification();
    }
});

async function carregarLista(){
    const lista = document.getElementById("listaQRCodes");
    lista.innerHTML = "";

    const codigos = await listarQRCodes();
    if(codigos.length === 0){
        lista.innerHTML = `
        <li class="list-group-item text-center">
            Nenhum QR Code cadastrado.
        </li>`;
        return;
    }

    codigos.forEach(codigo => {
        const item = document.createElement("li");
        item.className = "list-group-item";
        item.textContent = codigo;
        lista.appendChild(item);
    });
}

document
.getElementById("btnAtualizar")
.addEventListener("click", carregarLista);