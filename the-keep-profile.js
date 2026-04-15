const favoritesData = [
  { name: "The Witcher 3: Wild Hunt",                className: "witcher3" },
  { name: "Red Dead Redemption 2",                   className: "rdr2" },
  { name: "The Legend of Zelda: Breath of the Wild", className: "botw" },
  { name: "Cyberpunk 2077",                          className: "cyberpunk-2077" },
];

const reviewsData = [
  {
    title:  "Disco Elysium",
    className: "disco-elysium",
    rating: "5.0",
    text:   "Diálogo afiado e escolhas profundas. Um dos melhores RPGs narrativos da última década.",
    tags:   "RPG • Narrativa • Investigação",
  },
  {
    title:  "God of War Ragnarök",
    className: "gow-ragnarok",
    rating: "4.8",
    text:   "Uma sequência épica que supera o original em escala e profundidade emocional.",
    tags:   "Ação • Aventura • Mitologia",
  },
  {
    title:  "The Legend of Zelda: Breath of the Wild",
    className: "botw",
    rating: "5.0",
    text:   "Liberdade absoluta num mundo aberto magistralmente construído.",
    tags:   "Aventura • Open World • Puzzle",
  },
  {
    title:  "Cyberpunk 2077",
    className: "cyberpunk-2077",
    rating: "4.2",
    text:   "Apesar do lançamento conturbado, Night City é um dos mundos mais ricos do gaming.",
    tags:   "RPG • FPS • Futuro",
  },
];

let state = {
  name:        document.getElementById("profileNameDisplay").textContent,
  email:       "",
  avatarUrl:   document.getElementById("profileAvatarDisplay").src,
  favorites:   JSON.parse(JSON.stringify(favoritesData)),
  currentGame: {
    name: document.getElementById("currentGameName").textContent,
    img:  document.getElementById("currentGameImg").src,
  },
  lastGame: {
    name: document.getElementById("lastGameName").textContent,
    img:  document.getElementById("lastGameImg").src,
  },
  featuredReviewIndex: 0,
};

const openBtn        = document.getElementById("openEditModal");
const closeBtn       = document.getElementById("closeEditModal");
const cancelBtn      = document.getElementById("cancelEdit");
const saveBtn        = document.getElementById("saveEdit");
const modal          = document.getElementById("editModal");
const tabBtns        = document.querySelectorAll(".tab-btn");
const tabContents    = document.querySelectorAll(".tab-content");
const avatarUrlInput = document.getElementById("avatarUrlInput");
const avatarPreview  = document.getElementById("avatarPreview");
const usernameInput  = document.getElementById("usernameInput");
const currentGameNameInput = document.getElementById("currentGameNameInput");
const currentGameImgInput  = document.getElementById("currentGameImgInput");
const currentGamePreview   = document.getElementById("currentGamePreview");
const lastGameNameInput = document.getElementById("lastGameNameInput");
const lastGameImgInput  = document.getElementById("lastGameImgInput");
const lastGamePreview   = document.getElementById("lastGamePreview");

function openModal() {
  populateModal();
  modal.classList.add("open");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  modal.classList.remove("open");
  document.body.style.overflow = "";
}

openBtn.addEventListener("click", openModal);
closeBtn.addEventListener("click", closeModal);
cancelBtn.addEventListener("click", closeModal);
modal.addEventListener("click", (e) => {
  if (e.target === modal) closeModal();
});

tabBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    tabBtns.forEach((b) => b.classList.remove("active"));
    tabContents.forEach((c) => c.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.tab).classList.add("active");
  });
});

function populateModal() {
  avatarUrlInput.value  = state.avatarUrl;
  avatarPreview.src     = state.avatarUrl;
  usernameInput.value   = state.name;
  document.getElementById("emailInput").value           = state.email;
  document.getElementById("currentPasswordInput").value = "";
  document.getElementById("newPasswordInput").value     = "";
  document.getElementById("confirmPasswordInput").value = "";
  document.getElementById("passwordError").textContent  = "";

  buildFavoritesEditor();

  currentGameNameInput.value = state.currentGame.name;
  currentGameImgInput.value  = state.currentGame.img;
  currentGamePreview.src     = state.currentGame.img;

  lastGameNameInput.value    = state.lastGame.name;
  lastGameImgInput.value     = state.lastGame.img;
  lastGamePreview.src        = state.lastGame.img;

  buildReviewSelector();
}

function buildFavoritesEditor() {
  const list = document.getElementById("favoritesEditList");
  list.innerHTML = "";

  state.favorites.forEach((fav, i) => {
    const item = document.createElement("div");
    item.className = "favorite-edit-item";
    item.innerHTML = `
      <div class="favorite-edit-preview ${fav.className}" id="favPreview${i}"></div>
      <div class="favorite-edit-inputs">
        <input type="text" class="edit-input fav-name-input" data-index="${i}"
               placeholder="Nome do jogo" value="${fav.name}">
        <input type="text" class="edit-input fav-img-input" data-index="${i}"
               placeholder="URL da capa" value="">
      </div>
    `;
    list.appendChild(item);

    item.querySelector(".fav-img-input").addEventListener("input", (e) => {
      const preview = document.getElementById(`favPreview${i}`);
      preview.style.backgroundImage = e.target.value ? `url('${e.target.value}')` : "";
    });
  });
}

function buildReviewSelector() {
  const list = document.getElementById("reviewsSelectList");
  list.innerHTML = "";

  reviewsData.forEach((review, i) => {
    const opt = document.createElement("div");
    opt.className = "review-option" + (i === state.featuredReviewIndex ? " active" : "");
    opt.dataset.reviewId = i;
    opt.innerHTML = `
      <div class="review-option-img ${review.className}"></div>
      <div class="review-option-info">
        <span class="review-option-title">${review.title}</span>
        <span class="review-option-rating">⭐ ${review.rating}</span>
        <span class="review-option-tags">${review.tags}</span>
      </div>
      <div class="review-selected-badge">Em Destaque</div>
    `;
    opt.addEventListener("click", () => {
      list.querySelectorAll(".review-option").forEach((o) => o.classList.remove("active"));
      opt.classList.add("active");
      state.featuredReviewIndex = i;
    });
    list.appendChild(opt);
  });
}

avatarUrlInput.addEventListener("input", (e) => {
  avatarPreview.src = e.target.value;
});

currentGameImgInput.addEventListener("input", (e) => {
  currentGamePreview.src = e.target.value;
});

lastGameImgInput.addEventListener("input", (e) => {
  lastGamePreview.src = e.target.value;
});

saveBtn.addEventListener("click", () => {
  const newPassword     = document.getElementById("newPasswordInput").value;
  const confirmPassword = document.getElementById("confirmPasswordInput").value;
  const passwordError   = document.getElementById("passwordError");

  if (newPassword && newPassword !== confirmPassword) {
    passwordError.textContent = "As senhas não coincidem.";
    document.querySelector('[data-tab="tab-identity"]').click();
    return;
  }
  passwordError.textContent = "";

  state.name      = usernameInput.value.trim() || state.name;
  state.avatarUrl = avatarUrlInput.value.trim() || state.avatarUrl;
  state.email     = document.getElementById("emailInput").value.trim();

  document.querySelectorAll(".fav-name-input").forEach((inp) => {
    state.favorites[inp.dataset.index].name = inp.value;
  });
  document.querySelectorAll(".fav-img-input").forEach((inp) => {
    state.favorites[inp.dataset.index].img = inp.value;
  });

  state.currentGame.name = currentGameNameInput.value.trim();
  state.currentGame.img  = currentGameImgInput.value.trim();

  state.lastGame.name = lastGameNameInput.value.trim();
  state.lastGame.img  = lastGameImgInput.value.trim();

  applyStateToPage();
  closeModal();
  showToast("Perfil atualizado com sucesso!");
});

function applyStateToPage() {
  document.getElementById("profileNameDisplay").textContent = state.name;
  document.getElementById("profileAvatarDisplay").src       = state.avatarUrl;

  const grid = document.getElementById("favoritesGrid");
  const items = grid.querySelectorAll(".game-item");
  state.favorites.forEach((fav, i) => {
    const img = items[i].querySelector("img");
    img.src = fav.img;
    img.alt = fav.name;
  });

  document.getElementById("currentGameImg").src          = state.currentGame.img;
  document.getElementById("currentGameName").textContent = state.currentGame.name;
  document.getElementById("currentGameImg").alt          = state.currentGame.name;

  document.getElementById("lastGameImg").src          = state.lastGame.img;
  document.getElementById("lastGameName").textContent = state.lastGame.name;
  document.getElementById("lastGameImg").alt          = state.lastGame.name;

  const review = reviewsData[state.featuredReviewIndex];
  const featuredReviewCover = document.getElementById("featuredReviewCover");
  featuredReviewCover.className = `review-cover featured-review ${review.className}`;
  featuredReviewCover.setAttribute("aria-label", review.title);
  document.getElementById("featuredReviewTitle").textContent   = review.title;
  document.getElementById("featuredReviewRating").textContent  = review.rating;
  document.getElementById("featuredReviewText").textContent    = review.text;
  document.getElementById("featuredReviewTags").textContent    = review.tags;
}

function showToast(msg) {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3000);
}
