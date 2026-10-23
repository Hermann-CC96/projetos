const usuario = localStorage.getItem("usuario");

if(usuario){
    document.getElementById("nomeUsuario").innerHTML = `
        Bem-vindo,<br>
        <strong>${usuario}</strong>
    `;

    // Gatilho automático: se o arquivo push-client.js estiver carregado, 
    // ele tenta registrar o dispositivo no banco assim que a Home abre.
    if (typeof inicializarPushNotification === "function") {
        inicializarPushNotification();
    }
}

function logout(){
    // Garante que o token de autenticação e os dados sejam limpos no logout
    localStorage.removeItem("usuario");
    localStorage.removeItem("token"); 

    window.location.href="index.html";
}