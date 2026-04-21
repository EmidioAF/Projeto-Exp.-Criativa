from database import (
    criar_usuario,
    autenticar_usuario,
    listar_usuarios,
    listar_jogos,
    criar_review,
    listar_reviews_por_jogo,
    adicionar_ou_atualizar_lista,
    listar_lista_usuario
)

# Criar usuário
usuario_id = criar_usuario("Emidio", "emidio@email.com", "senha123")
print("Usuário criado com ID:", usuario_id)

# Testar login
usuario = autenticar_usuario("emidio@email.com", "senha123")
print("Login:", usuario)

# Listar usuários
print("\nUsuários cadastrados:")
print(listar_usuarios())

# Listar jogos
print("\nJogos:")
print(listar_jogos())

# Criar review
review_id = criar_review(usuario_id, 4, 5, "Jogo excelente")
print("\nReview criada:", review_id)

# Listar reviews do jogo 4
print("\nReviews do jogo:")
print(listar_reviews_por_jogo(4))

# Adicionar à lista do usuário
adicionar_ou_atualizar_lista(usuario_id, 4, "zerado")
adicionar_ou_atualizar_lista(usuario_id, 7, "jogando")

print("\nLista do usuário:")
print(listar_lista_usuario(usuario_id))
