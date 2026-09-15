let isUploading = false;

async function upload_file() {
  if (isUploading) 
    return;

  const fileInput = document.getElementById("fileInput");
  const cardCountSelect = document.getElementById("cardCount");
  const button = document.querySelector(".upload-box > button");

  if (!fileInput.files.length) {
    alert("Please select a file");
    return;
  }

  const selectedFile = fileInput.files[0];
  
  isUploading = true;
  button.disabled = true;
  fileInput.disabled = true;
  cardCountSelect.disabled = true;
  button.innerText = "Generating...";

  try {
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("cardCount", cardCountSelect.value);

    const res = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.error || "Something went wrong");
      return;
    }

    localStorage.setItem("flashcards", JSON.stringify(data));
    localStorage.setItem("fileName", selectedFile.name);
    window.location.href = "flashcardsPage.html";

  } catch (err) {
    alert("Server error");
    console.error(err);
  } finally {
    isUploading = false;
    button.disabled = false;
    fileInput.disabled = false;
    cardCountSelect.disabled = false;
    button.innerText = "Generate";
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