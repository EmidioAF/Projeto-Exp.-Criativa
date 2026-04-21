from database import criar_usuario, autenticar_usuario

usuario_id = criar_usuario("Emidio", "emidio@email.com", "senha123")
print("Usuário criado com ID:", usuario_id)

login_ok = autenticar_usuario("emidio@email.com", "senha123")
print("Login correto:", login_ok)

login_erro = autenticar_usuario("emidio@email.com", "senha_errada")
print("Login incorreto:", login_erro)
