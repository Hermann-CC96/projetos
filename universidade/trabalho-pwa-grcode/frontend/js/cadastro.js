document
.getElementById("cadastroForm")
.addEventListener("submit", async function(event){

    event.preventDefault();

    const nome = document.getElementById("nome").value;
    const cpf = document.getElementById("cpf").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    localStorage.setItem("nomeUsuario", nome);
    localStorage.setItem("cpfUsuario", cpf);
    localStorage.setItem("emailUsuario", email);
    localStorage.setItem("senhaUsuario", senha);

    const resposta = await cadastrar(nome, email, senha, cpf);

    if(resposta.sucesso){
        document.getElementById("mensagemCadastro").innerHTML = `
        <div class="alert alert-success">
            Cadastro realizado com sucesso!
        </div>`;

        setTimeout(()=>{
            window.location.href="index.html";
        }, 1500);
    } else {
        // Exibe o erro real vindo do back-end (ex: CPF ou E-mail já cadastrados)
        document.getElementById("mensagemCadastro").innerHTML = `
        <div class="alert alert-danger">
            ${resposta.mensagem}
        </div>`;
    }
});