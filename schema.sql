CREATE DATABASE IF NOT EXISTS thekeep_db;
USE thekeep_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jogos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    genero VARCHAR(100),
    plataforma VARCHAR(100),
    imagem_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    jogo_id INT NOT NULL,
    nota INT NOT NULL,
    comentario TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_nota CHECK (nota BETWEEN 1 AND 5),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS lista_jogos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    jogo_id INT NOT NULL,
    status ENUM('quero_jogar', 'jogando', 'zerado') NOT NULL,
    UNIQUE KEY unique_usuario_jogo (usuario_id, jogo_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE
);

INSERT INTO jogos (titulo, genero, plataforma, imagem_url) VALUES
('The Legend of Zelda: Breath of the Wild', 'Aventura/Open World', 'Nintendo Switch', 'BOTW.png'),
('Cyberpunk 2077', 'RPG/Open World', 'PC/PS5/Xbox', 'Cy2077.jpg'),
('Deathloop', 'FPS/Action', 'PC/PS5', 'DELI.jpg'),
('Elden Ring', 'RPG/Souls-like', 'PC/PS5/Xbox', 'ElRin.jpg'),
('God of War Ragnarok', 'Aventura/Acao', 'PS5', 'GOWrag.jpg'),
('Horizon Forbidden West', 'Aventura/Open World', 'PS5', 'Hor.jpg'),
('Red Dead Redemption 2', 'Aventura/Open World', 'PC/PS4/Xbox', 'RDR2.png'),
('The Witcher 3: Wild Hunt', 'RPG/Open World', 'PC/PS5/Xbox', 'TW3.jpg');

-- Cadastro de usuário (senha armazenada como hash bcrypt em produção)
INSERT INTO usuarios (nome, email, senha) VALUES
('XxRogerinMitoxX', 'teste1@gmail.com', 'teste123');
