const reviews = [
  {
    title: "Disco Elysium",
    className: "disco-elysium",
    rating: "5.0",
    text: "Diálogo afiado e escolhas profundas. Um dos melhores RPGs narrativos da última década.",
    tags: "RPG • Narrativa • Investigação",
  },
  {
    title: "God of War Ragnarök",
    className: "gow-ragnarok",
    rating: "4.8",
    text: "Combate excelente, história emocionante e personagens marcantes.",
    tags: "Ação • História",
  },
  {
    title: "Zelda: Breath of the Wild",
    className: "botw",
    rating: "4.9",
    text: "Liberdade absurda de exploração e gameplay inovador.",
    tags: "Aventura • Mundo Aberto",
  },
  {
    title: "The Witcher 3",
    className: "witcher3",
    rating: "4.7",
    text: "Grande história e personagens inesquecíveis num mundo rico.",
    tags: "RPG • Fantasia",
  },
  {
    title: "Cyberpunk 2077",
    className: "cyberpunk-2077",
    rating: "4.2",
    text: "Night City ainda é um dos mundos mais ambiciosos do gaming.",
    tags: "RPG • Futuro",
  },
];

const reviewsList = document.getElementById("reviewsList");
const reviewSearchInput = document.getElementById("reviewSearchInput");

function renderReviews(search = "") {
  reviewsList.innerHTML = "";
  const query = search.trim().toLowerCase();
  const filtered = reviews.filter((review) => {
    if (!query) return true;
    return [review.title, review.text, review.tags]
      .some((value) => value.toLowerCase().includes(query));
  });

  if (!filtered.length) {
    reviewsList.innerHTML = '<p class="empty-state">Nenhuma review encontrada.</p>';
    return;
  }

  filtered.forEach((review) => {
    const card = document.createElement("article");
    card.className = `review-card ${review.className}`;
    card.innerHTML = `
      <div class="review-cover"></div>
      <div class="review-content">
        <div class="review-meta">
          <h3>${review.title}</h3>
          <span class="rating">${review.rating}</span>
        </div>
        <p>${review.text}</p>
        <div class="review-tags">${review.tags}</div>
      </div>
    `;
    reviewsList.appendChild(card);
  });
}

reviewSearchInput.addEventListener("input", (event) => {
  renderReviews(event.target.value);
});

renderReviews();
