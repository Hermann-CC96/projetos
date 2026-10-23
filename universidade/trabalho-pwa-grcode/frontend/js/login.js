document
.getElementById("loginForm")
.addEventListener("submit", async function(event){

    event.preventDefault();

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    // Executa a função do api.js que faz o POST e salva Token/Usuário no localStorage
    const resposta = await login(email, senha);

    if(resposta.sucesso){
        // Redireciona direto para a Home, pois o api.js já guardou tudo o que precisamos
        window.location.href = "home.html";
    } else {
        // Exibe a mensagem de erro real retornada pelo servidor back-end
        document.getElementById("mensagemLogin").innerHTML = `
        <div class="alert alert-danger">
            ${resposta.mensagem}
        </div>`;
    }
});