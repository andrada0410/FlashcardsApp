let cards = [];
let index = 0;

window.onload = function () {
  cards = JSON.parse(localStorage.getItem("flashcards")) || [];
  renderCard();
};

function updateProgressBar(){
  const progressBar = document.getElementById("progressBar");

  if (!progressBar || cards.length === 0)
    return;

  const percentage = Math.round(((index + 1) / cards.length) * 100);

  progressBar.value = percentage;
}

function renderCard() {
  const container = document.getElementById("app");

  if (cards.length === 0) {
    container.innerHTML = "<h2>No flashcards found</h2>";
    updateProgressBar();
    return;
  }

  const card = cards[index];

  container.innerHTML = `
    <div class="study-wrapper">
      <div class="card" onclick="toggleFlip()">
        <div class="inner">
          <div class="front">
            <h2>Question</h2>
            <p id="card-question"></p>
          </div>

          <div class="back">
            <h2>Answer</h2>
            <p id="card-answer"></p>
          </div>
        </div>
      </div>

      <div class="controls">
        <button onclick="prevCard()" ${index === 0 ? "disabled" : ""}>Prev</button>
        <span>${index + 1} / ${cards.length}</span>
        <button onclick="nextCard()" ${index === cards.length - 1 ? "disabled" : ""}>Next</button>
      </div>

    </div>
  `;
  document.getElementById("card-question").textContent = card.question;
  document.getElementById("card-answer").textContent = card.answer;

  updateProgressBar();
}

function nextCard() {
  if (index < cards.length - 1) {
    index++;
    renderCard();
  }
}

function prevCard() {
  if (index > 0) {
    index--;
    renderCard();
  }
}

function shuffleCards() {
  if (cards.length <= 1) 
    return;

  for (let i = cards.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [cards[i], cards[j]] = [cards[j], cards[i]];
  }

  index = 0;
  renderCard();
}

function toggleTheme() {
  document.body.classList.toggle("dark");

  const btn = document.querySelector(".theme-toggle");

  if (document.body.classList.contains("dark")) {
    btn.innerHTML = "☀️";
    localStorage.setItem("theme", "dark");
  } else {
    btn.innerHTML = "🌙";
    localStorage.setItem("theme", "light");
  }
}

// load saved theme
window.addEventListener("load", () => {
  const theme = localStorage.getItem("theme");

  if (theme === "dark") {
    document.body.classList.add("dark");

    const btn = document.querySelector(".theme-toggle");
    if (btn) btn.innerHTML = "☀️";
  }
});

function toggleFlip(){
  const cardElement = document.querySelector(".card");
  if (cardElement){
    cardElement.classList.toggle("flipped");
  }
}

window.addEventListener("keydown", (event) => {
  switch (event.key) {
    case "ArrowRight":
    case " ":
      event.preventDefault();
      nextCard();
      break;

    case "ArrowLeft":
      event.preventDefault();
      prevCard();
      break;

    case "ArrowUp":
    case "ArrowDown":
    case "Enter":
      event.preventDefault();
      toggleFlip();
      break;

    case "s":
    case "S":
      event.preventDefault();
      shuffleCards();
      break;
  }
});