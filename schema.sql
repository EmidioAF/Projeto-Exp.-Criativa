-- ==============================================
-- THE KEEP - Schema SQL Inicial
-- Testado com MySQL 8+. Adaptável ao SQLite.
-- ==============================================

CREATE DATABASE IF NOT EXISTS the_keep CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE the_keep;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    foto_url VARCHAR(255) DEFAULT '/static/img/avatar_default.png',
    is_admin BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jogos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    desenvolvedora VARCHAR(100),
    data_lancamento DATE,
    descricao TEXT,
    lore TEXT,
    genero VARCHAR(80),
    capa_url VARCHAR(255) DEFAULT '/static/img/game_default.png',
    media_reviews DECIMAL(3,2) DEFAULT 0.00,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    jogo_id INT NOT NULL,
    nota TINYINT NOT NULL,
    comentario TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE,
    UNIQUE KEY unico_review (usuario_id, jogo_id)
);

CREATE TABLE IF NOT EXISTS favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    jogo_id INT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE,
    UNIQUE KEY unico_fav (usuario_id, jogo_id)
);

CREATE TABLE IF NOT EXISTS status_jogo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    jogo_id INT NOT NULL,
    status ENUM('jogando', 'jogado', 'quero_jogar') NOT NULL DEFAULT 'quero_jogar',
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE,
    UNIQUE KEY unico_status (usuario_id, jogo_id)
);

-- Admin padrão — senha: admin123
-- TODO: Troque o hash antes de usar em produção!
INSERT INTO usuarios (username, email, senha_hash, is_admin) VALUES
('admin', 'admin@thekeep.com', '$2b$12$EIXPsGbfqv0z6S3mzQ5TIu5KhKlEn8e5G7OjkAx2Z1mR4yPq3t2Wy', TRUE);

INSERT INTO jogos (nome, desenvolvedora, data_lancamento, descricao, lore, genero) VALUES
('The Witcher 3', 'CD Projekt Red', '2015-05-19', 'RPG de mundo aberto em dark fantasy.', 'Geralt busca Ciri enquanto a Wild Hunt a persegue.', 'RPG'),
('Dark Souls', 'FromSoftware', '2011-09-22', 'Action RPG desafiador com exploração interconectada.', 'Um morto-vivo busca o destino dos Chosen Undead.', 'Action RPG'),
('Hollow Knight', 'Team Cherry', '2017-02-24', 'Metroidvania atmosférico com world-building profundo.', 'Um cavaleiro silencioso explora as ruínas de Hallownest.', 'Metroidvania');
