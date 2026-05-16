-- ==============================================
-- THE KEEP - Schema SQL Completo v3
-- Execute no MySQL Workbench: File > Open SQL Script > Execute
-- Após executar: python gerar_admin.py
-- Capas: Steam CDN (cdn.cloudflare.steamstatic.com)
-- ==============================================

CREATE DATABASE IF NOT EXISTS the_keep CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE the_keep;

DROP TABLE IF EXISTS status_jogo;
DROP TABLE IF EXISTS favoritos;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS jogos;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    foto_url VARCHAR(255) DEFAULT '/static/img/avatar_default.png',
    is_admin BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE jogos (
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

CREATE TABLE reviews (
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

CREATE TABLE favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    jogo_id INT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE,
    UNIQUE KEY unico_fav (usuario_id, jogo_id)
);

CREATE TABLE status_jogo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    jogo_id INT NOT NULL,
    status ENUM('jogando', 'jogado', 'quero_jogar') NOT NULL DEFAULT 'quero_jogar',
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE,
    UNIQUE KEY unico_status (usuario_id, jogo_id)
);

-- ==============================================
-- 33 JOGOS — capas via Steam CDN
-- Formato: https://cdn.cloudflare.steamstatic.com/steam/apps/{APP_ID}/header.jpg
-- ==============================================
INSERT INTO jogos (nome, desenvolvedora, data_lancamento, descricao, lore, genero, capa_url) VALUES

-- ---- JOGOS ORIGINAIS (18) ----

('The Witcher 3: Wild Hunt', 'CD Projekt Red', '2015-05-19',
 'RPG de mundo aberto épico com escolhas morais profundas e narrativa premiada.',
 'Geralt de Rivia busca sua filha adotiva Ciri enquanto a ameaça sobrenatural da Wild Hunt a persegue pelos confins do Continente.',
 'RPG',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/292030/header.jpg'),

('Dark Souls', 'FromSoftware', '2011-09-22',
 'Action RPG desafiador com exploração interconectada e narrativa ambiental densa.',
 'Um morto-vivo amaldiçoado parte em jornada para descobrir o destino dos Chosen Undead e a verdade sobre o ciclo de fogo e treva.',
 'Action RPG',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/211420/header.jpg'),

('Hollow Knight', 'Team Cherry', '2017-02-24',
 'Metroidvania atmosférico com arte handmade e world-building profundíssimo.',
 'Um cavaleiro sem nome desce às ruínas do reino de insetos Hallownest, consumido por uma infecção que corrompeu seus habitantes.',
 'Metroidvania',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/367520/header.jpg'),

('Red Dead Redemption 2', 'Rockstar Games', '2019-12-05',
 'Épico open-world western sobre lealdade, honra e o fim de uma era.',
 'Arthur Morgan, membro do bando de Dutch van der Linde, enfrenta dilemas morais enquanto o velho oeste dá lugar à modernidade.',
 'Open World',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1174180/header.jpg'),

('Elden Ring', 'FromSoftware', '2022-02-25',
 'Action RPG de mundo aberto criado em parceria com George R. R. Martin.',
 'Os Tarnished são chamados de volta às Terras Intermédias para restaurar o Elden Ring e se tornar o Elden Lord.',
 'Action RPG',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1245620/header.jpg'),

('God of War', 'Santa Monica Studio', '2022-01-14',
 'Kratos e seu filho Atreus enfrentam a mitologia nórdica em uma jornada visceral de pai e filho.',
 'Após deixar a Grécia, Kratos vive no mundo nórdico. Com a morte da esposa, ele e Atreus partem para espalhar suas cinzas no pico mais alto dos nove reinos.',
 'Action Adventure',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1593500/header.jpg'),

('Cyberpunk 2077', 'CD Projekt Red', '2020-12-10',
 'RPG de ficção científica em mundo aberto na megalópole futurista Night City.',
 'V, um mercenário, implanta um chip com a consciência do lendário Johnny Silverhand, desencadeando uma corrida contra o tempo para sobreviver.',
 'RPG',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1091500/header.jpg'),

('Minecraft', 'Mojang Studios', '2011-11-18',
 'Jogo sandbox de construção e sobrevivência que definiu uma geração inteira.',
 'Em um mundo de blocos infinitamente gerado, jogadores exploram, coletam recursos, constroem estruturas e enfrentam criaturas noturnas.',
 'Sandbox',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1672970/header.jpg'),

('Grand Theft Auto V', 'Rockstar Games', '2015-04-14',
 'Crime de mundo aberto com três protagonistas jogáveis e o massivo GTA Online.',
 'Três criminosos — Michael, Trevor e Franklin — unem forças em Los Santos para executar heists enquanto fogem do governo e de rivais.',
 'Open World',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/271590/header.jpg'),

('The Legend of Zelda: Breath of the Wild', 'Nintendo', '2017-03-03',
 'Open-world que redefiniu o gênero, com física sandbox e exploração sem limites.',
 'Link acorda sem memórias após 100 anos de sono e deve encontrar força para enfrentar Calamity Ganon antes que destrua Hyrule.',
 'Action Adventure',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/2432740/header.jpg'),

('Sekiro: Shadows Die Twice', 'FromSoftware', '2019-03-22',
 'Action stealth ambientado no Japão feudal com sistema de combate único e preciso.',
 'Wolf, um shinobi, busca resgatar seu jovem senhor e vingar a desonra sofrida, enfrentando imortais e demônios no Japão do século XVI.',
 'Action',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/814380/header.jpg'),

('Hades', 'Supergiant Games', '2020-09-17',
 'Rogue-like de ação com narrativa excepcional integrada ao gameplay e arte deslumbrante.',
 'Zagreus, filho do deus Hades, tenta escapar do submundo enfrentando seus guardiões com poderes concedidos pelos deuses do Olimpo.',
 'Roguelike',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1145360/header.jpg'),

('Disco Elysium', 'ZA/UM', '2019-10-15',
 'RPG de detetive sem combate com o sistema de habilidades mais original já criado.',
 'Um detetive sem memórias deve resolver um assassinato em uma cidade falida enquanto reconstrói sua identidade e ideologia do zero.',
 'RPG',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/632470/header.jpg'),

('Bloodborne', 'FromSoftware', '2015-03-24',
 'Action RPG gótico de horror cósmico ambientado na cidade vitoriana de Yharnam.',
 'Um caçador desperta em Yharnam durante a noite da caçada, descobrindo os segredos sombrios por trás da praga que transformou seus habitantes em bestas.',
 'Action RPG',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/2229580/header.jpg'),

('Stardew Valley', 'ConcernedApe', '2016-02-26',
 'Simulador de fazenda indie que conquistou o mundo com charme e profundidade surpreendente.',
 'Você herda a fazenda do seu avô em Stardew Valley e decide trocar a vida corporativa pelo campo, descobrindo uma comunidade cheia de segredos.',
 'Simulation',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/413150/header.jpg'),

('Portal 2', 'Valve', '2011-04-19',
 'Puzzle em primeira pessoa com narrativa humorística e design de fases genial.',
 'Chell acorda novamente em Aperture Science e deve escapar das instalações com o auxílio de uma IA rebelde enquanto enfrenta a manipuladora GLaDOS.',
 'Puzzle',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/620/header.jpg'),

('Resident Evil 4 Remake', 'Capcom', '2023-03-24',
 'Remake do clássico survival horror com gráficos de geração atual e gameplay refinado.',
 'Leon S. Kennedy é enviado a uma aldeia rural europeia para resgatar a filha do presidente dos EUA, descobrindo um culto sinistro e uma nova ameaça biológica.',
 'Survival Horror',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/2050650/header.jpg'),

('Baldur''s Gate 3', 'Larian Studios', '2023-08-03',
 'RPG baseado em D&D 5e com liberdade narrativa e consequências sem precedentes.',
 'Infectados com um parasita Mind Flayer, um grupo de aventureiros percorre Faerûn em busca de uma cura e acaba no centro de uma conspiração divina.',
 'RPG',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1086940/header.jpg'),

-- ---- 15 JOGOS NOVOS ----

('Counter-Strike 2', 'Valve', '2023-09-27',
 'O FPS tático mais jogado do mundo, completamente reconstruído na engine Source 2.',
 'Dois times se enfrentam em mapas icônicos: terroristas plantam bombas enquanto contra-terroristas tentam neutralizá-las em rounds de alta tensão.',
 'FPS',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg'),

('Dota 2', 'Valve', '2013-07-09',
 'MOBA de estratégia profunda com mais de 120 heróis e competição de nível mundial.',
 'Dois times de cinco heróis batalham para destruir o Ancient inimigo em Ancient, no epicentro de uma guerra entre forças da luz e da escuridão.',
 'MOBA',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/570/header.jpg'),

('Among Us', 'Innersloth', '2018-11-16',
 'Jogo de dedução social em que tripulantes tentam identificar impostores a bordo.',
 'A bordo de uma nave espacial, crewmates completam tarefas enquanto um ou mais impostores sabotam a missão e eliminam a tripulação silenciosamente.',
 'Social Deduction',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/945360/header.jpg'),

('Terraria', 'Re-Logic', '2011-05-16',
 'Aventura 2D de ação e construção com conteúdo praticamente infinito.',
 'Em um mundo 2D procedural, jogadores escavam, constroem e combatem centenas de inimigos e chefes em uma jornada que vai do subsolo ao espaço.',
 'Sandbox',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/105600/header.jpg'),

('Rust', 'Facepunch Studios', '2018-02-08',
 'Survival multiplayer brutal onde a principal ameaça são outros jogadores.',
 'Você acorda nu em uma ilha hostil sem nada. Cada escolha — com quem confiar, o que construir, quando atacar — determina se vai sobreviver ou morrer.',
 'Survival',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/252490/header.jpg'),

('Celeste', 'Maddy Makes Games', '2018-01-25',
 'Plataformer preciso e emocionante sobre superar os próprios limites.',
 'Madeline sobe a montanha Celeste para encarar seus demônios internos literais e figurativos, em uma metáfora poderosa sobre saúde mental.',
 'Platformer',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/504230/header.jpg'),

('Ori and the Will of the Wisps', 'Moon Studios', '2020-03-11',
 'Metroidvania visual e emocionalmente deslumbrante com trilha sonora premiada.',
 'Ori parte em uma nova jornada para descobrir seu destino e salvar uma floresta corrompida, enfrentando criaturas e segredos antigos.',
 'Metroidvania',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1057090/header.jpg'),

('Death Stranding', 'Kojima Productions', '2020-07-14',
 'Jogo de entrega pós-apocalíptico e meditativo de Hideo Kojima.',
 'Sam Porter Bridges atravessa os Estados Unidos devastados por uma catástrofe sobrenatural para reconectar a sociedade, carregando encomendas e bebês em cápsulas.',
 'Action',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1190460/header.jpg'),

('Divinity: Original Sin 2', 'Larian Studios', '2017-09-14',
 'RPG tático com co-op de até quatro jogadores e liberdade criativa total.',
 'Sourcerers perseguidos pelo Divine Order buscam se tornar divindades em Rivellon, enquanto uma entidade consumidora de almas ameaça destruir tudo.',
 'RPG',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/435150/header.jpg'),

('Monster Hunter: World', 'Capcom', '2018-08-09',
 'Action RPG de caça cooperativa com ecossistemas vivos e crafting profundo.',
 'Caçadores exploram o Novo Mundo rastreando e combatendo criaturas colossais para coletar materiais e forjar equipamentos cada vez mais poderosos.',
 'Action RPG',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/582010/header.jpg'),

('Persona 5 Royal', 'Atlus', '2022-10-21',
 'JRPG estilizado sobre rebeldia, identidade e transformação social.',
 'Ren Amamiya, acusado injustamente de um crime, forma os Phantom Thieves para invadir os Palaces da mente de adultos corruptos e mudar seus corações.',
 'JRPG',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1687950/header.jpg'),

('Lies of P', 'Round8 Studio', '2023-09-19',
 'Soulslike baseado em Pinóquio ambientado em uma Belle Époque sombria.',
 'P, um puppet que ganhou vida, percorre a cidade de Krat mergulhada em caos para encontrar seu criador Geppetto enquanto enfrenta outros puppets enlouquecidos.',
 'Soulslike',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1627720/header.jpg'),

('Palworld', 'Pocketpair', '2024-01-19',
 'Jogo de sobrevivência e crafting com criaturas colecionáveis em mundo aberto.',
 'Em um mundo selvagem, jogadores capturam e treinam Pals — criaturas misteriosas — para trabalhar, lutar e ajudar na construção de bases em um ambiente perigoso.',
 'Survival',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1623730/header.jpg'),

('Hogwarts Legacy', 'Avalanche Software', '2023-02-10',
 'RPG de ação no universo de Harry Potter ambientado no século XIX.',
 'Um estudante com poderes incomuns chega a Hogwarts e descobre estar no centro de uma conspiração envolvendo magia antiga e uma rebelião goblin.',
 'Action RPG',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/990080/header.jpg'),

('Hades II', 'Supergiant Games', '2024-05-06',
 'Sequência do aclamado rogue-like com a princesa Melinoë como protagonista.',
 'Melinoë, irmã de Zagreus, foi criada pela feiticeira Hecate para derrotar Cronos, o Titã do Tempo, que aprisionou seu pai Hades no submundo.',
 'Roguelike',
 'https://cdn.cloudflare.steamstatic.com/steam/apps/1145350/header.jpg');
