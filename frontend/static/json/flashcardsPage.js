let cards = [];
let index = 0;

window.onload = function () {
  cards = JSON.parse(localStorage.getItem("flashcards")) || [];
  renderCard();
};

function renderCard() {
  const container = document.getElementById("app");

  if (cards.length === 0) {
    container.innerHTML = "<h2>No flashcards found</h2>";
    return;
  }

  const card = cards[index];

  container.innerHTML = `
    <div class="study-wrapper">

      <div class="card">
        <div class="inner">
          <div class="front">
            <h2>Question</h2>
            <p>${card.question}</p>
          </div>

          <div class="back">
            <h2>Answer</h2>
            <p>${card.answer}</p>
          </div>
        </div>
      </div>

      <div class="controls">
        <button onclick="prevCard()">Previous</button>
        <span>${index + 1} / ${cards.length}</span>
        <button onclick="nextCard()">Next</button>
      </div>

    </div>
  `;
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