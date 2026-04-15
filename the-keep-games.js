const finishedGames = [
  { title: "Disco Elysium", image: "DELI.jpg", rating: "★★★★½", info: "RPG narrativo" },
  { title: "God of War Ragnarök", image: "GOWrag.jpg", rating: "★★★★☆", info: "Ação cinematográfica" },
  { title: "Zelda: Breath of the Wild", image: "BOTW.png", rating: "★★★★☆", info: "Exploração aberta" },
  { title: "The Witcher 3", image: "TW3.jpg", rating: "★★★★☆", info: "História épica" },
  { title: "Horizon Forbidden West", image: "Hor.jpg", rating: "★★★★☆", info: "Gráficos impressionantes" },
];

const gamesGrid = document.getElementById("gamesFinishedGrid");
const gameSearchInput = document.getElementById("gameSearchInput");

function renderGames(search = "") {
  gamesGrid.innerHTML = "";
  const query = search.trim().toLowerCase();
  const filtered = finishedGames.filter((game) => {
    if (!query) return true;
    return [game.title, game.info].some((value) => value.toLowerCase().includes(query));
  });

  if (!filtered.length) {
    gamesGrid.innerHTML = '<p class="empty-state">Nenhum jogo encontrado.</p>';
    return;
  }

  filtered.forEach((game) => {
    const card = document.createElement("div");
    card.className = "finished-game";
    card.innerHTML = `
      <div class="poster-wrapper">
        <img src="${game.image}" alt="${game.title}" class="game-cover">
      </div>
      <div class="game-rating">
        <span class="stars">${game.rating}</span>
      </div>
    `;
    gamesGrid.appendChild(card);
  });
}

gameSearchInput.addEventListener("input", (event) => {
  renderGames(event.target.value);
});

renderGames();
