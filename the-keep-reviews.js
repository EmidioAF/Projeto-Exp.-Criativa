const reviews = [
  {
    title: "Disco Elysium",
    className: "disco-elysium",
    rating: 5.0,
    text: "Diálogo afiado e escolhas profundas. Um dos melhores RPGs narrativos da última década.",
    tags: "RPG • Narrativa • Investigação",
  },
  {
    title: "God of War Ragnarök",
    className: "gow-ragnarok",
    rating: 4.8,
    text: "Combate excelente, história emocionante e personagens marcantes.",
    tags: "Ação • História",
  },
  {
    title: "Zelda: Breath of the Wild",
    className: "botw",
    rating: 4.9,
    text: "Liberdade absurda de exploração e gameplay inovador.",
    tags: "Aventura • Mundo Aberto",
  },
  {
    title: "The Witcher 3",
    className: "witcher3",
    rating: 4.7,
    text: "Grande história e personagens inesquecíveis num mundo rico.",
    tags: "RPG • Fantasia",
  },
  {
    title: "Cyberpunk 2077",
    className: "cyberpunk-2077",
    rating: 4.2,
    text: "Night City ainda é um dos mundos mais ambiciosos do gaming.",
    tags: "RPG • Futuro",
  },
];

const reviewsList = document.getElementById("reviewsList");
const reviewSearchInput = document.getElementById("reviewSearchInput");

/* GERAR ESTRELAS */
function generateStars(rating) {
  const maxStars = 5;
  const fullStars = Math.round(rating);
  let starsHTML = "";

  for (let i = 1; i <= maxStars; i++) {
    starsHTML += `<span class="star ${i <= fullStars ? "filled" : ""}">★</span>`;
  }

  return starsHTML;
}

/* RENDER */
function renderReviews(search = "") {
  reviewsList.innerHTML = "";
  const query = search.toLowerCase();

  const filtered = reviews.filter((review) => {
    return [review.title, review.text, review.tags]
      .some(v => v.toLowerCase().includes(query));
  });

  if (!filtered.length) {
    reviewsList.innerHTML = "<p>Nenhuma review encontrada.</p>";
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
          <div class="rating-container">
            <span class="rating">${review.rating}</span>
            <div class="stars">${generateStars(review.rating)}</div>
          </div>
        </div>
        <p>${review.text}</p>
        <div class="review-tags">${review.tags}</div>
      </div>
    `;

    reviewsList.appendChild(card);
  });
}

/* SEARCH */
reviewSearchInput.addEventListener("input", (e) => {
  renderReviews(e.target.value);
});

/* INIT */
renderReviews();
