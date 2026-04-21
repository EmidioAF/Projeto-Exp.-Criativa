from database import criar_usuario, autenticar_usuario

usuario_id = criar_usuario("XxRogerinMitoxX", "teste1@gmail.com", "teste123")
print("Usuário criado com ID:", usuario_id)

login_ok = autenticar_usuario("teste1@gmail.com", "teste123")
print("Login correto:", login_ok)
