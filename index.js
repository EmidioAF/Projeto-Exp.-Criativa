const mostPlayedGames = [
  { title: "The Witcher 3", image: "TW3.jpg", rating: "4.9", players: "279h" },
  { title: "Elden Ring", image: "ElRin.jpg", rating: "4.8", players: "322h" },
  { title: "Horizon Forbidden West", image: "Hor.jpg", rating: "4.6", players: "214h" },
  { title: "Cyberpunk 2077", image: "Cy2077.jpg", rating: "4.2", players: "198h" },
  { title: "Disco Elysium", image: "DELI.jpg", rating: "5.0", players: "147h" },
];

const highestRatedGames = [
  { title: "Disco Elysium", image: "DELI.jpg", rating: "5.0", highlight: "RPG narrativo" },
  { title: "Zelda: Breath of the Wild", image: "BOTW.png", rating: "4.9", highlight: "Exploração aberta" },
  { title: "God of War Ragnarök", image: "GOWrag.jpg", rating: "4.8", highlight: "Ação cinematográfica" },
  { title: "The Witcher 3", image: "TW3.jpg", rating: "4.7", highlight: "História épica" },
  { title: "Horizon Forbidden West", image: "Hor.jpg", rating: "4.6", highlight: "Visual impressionante" },
];

const topReviews = [
  { title: "Disco Elysium", image: "DELI.jpg", rating: "5.0", text: "Narrativa brutalmente honesta e um sistema de escolhas inesquecível." , tags: "RPG • Mistério"},
  { title: "Zelda: Breath of the Wild", image: "BOTW.png", rating: "4.9", text: "Liberdade total em um mundo aberto lindo e cheio de descobertas.", tags: "Aventura • Mundo Aberto"},
  { title: "God of War Ragnarök", image: "GOWrag.jpg", rating: "4.8", text: "Emocionante, brutal e com uma jornada que prende do começo ao fim.", tags: "Ação • Mitologia"},
  { title: "The Witcher 3", image: "TW3.jpg", rating: "4.7", text: "Um RPG que define qualidade de história e ambientação.", tags: "RPG • Fantasia"},
];

const mostPlayedList = document.getElementById("mostPlayedList");
const topRatedGamesList = document.getElementById("topRatedGamesList");
const topReviewsList = document.getElementById("topReviewsList");
const landingSearch = document.getElementById("landingSearch");

function createGameCard(game) {
  const card = document.createElement("article");
  card.className = "card";
  card.innerHTML = `
    <img src="${game.image}" alt="${game.title}" />
    <h3>${game.title}</h3>
    <p>${game.highlight || "Mais jogado atualmente"}</p>
    <span class="rating">⭐ ${game.rating} • ${game.players || "-"}</span>
  `;
  return card;
}

function createReviewCard(review) {
  const card = document.createElement("article");
  card.className = "review-card";
  card.innerHTML = `
    <img src="${review.image}" alt="${review.title}" />
    <h3>${review.title}</h3>
    <p>${review.text}</p>
    <span class="rating">⭐ ${review.rating}</span>
    <div class="review-tags">${review.tags}</div>
  `;
  return card;
}

function renderCards(list, container, factory, filterText = "") {
  container.innerHTML = "";
  const query = filterText.trim().toLowerCase();
  list
    .filter((item) => {
      if (!query) return true;
      return [item.title, item.highlight, item.tags, item.text]
        .filter(Boolean)
        .some((value) => value.toLowerCase().includes(query));
    })
    .forEach((item) => container.appendChild(factory(item)));

  if (!container.children.length) {
    container.innerHTML = `<p class="empty-state">Nenhum resultado encontrado.</p>`;
  }
}

function updateLanding() {
  const query = landingSearch.value;
  renderCards(mostPlayedGames, mostPlayedList, createGameCard, query);
  renderCards(highestRatedGames, topRatedGamesList, createGameCard, query);
  renderCards(topReviews, topReviewsList, createReviewCard, query);
}

landingSearch.addEventListener("input", updateLanding);
updateLanding();
