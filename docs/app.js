const state = {
  data: null,
  categoryId: null,
  algorithmId: null,
  selectedCodeFileName: null,
  query: "",
};

const intro = document.getElementById("intro");
const introBar = document.getElementById("introBar");
const categoryList = document.getElementById("categoryList");
const algorithmList = document.getElementById("algorithmList");
const algorithmDetails = document.getElementById("algorithmDetails");
const searchInput = document.getElementById("searchInput");

const htmlEscape = (str) =>
  str
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");

function markdownToHtml(markdown) {
  const escaped = htmlEscape(markdown);
  const lines = escaped.split(/\r?\n/);
  const html = [];
  let inList = false;

  for (const line of lines) {
    if (line.startsWith("- ") || line.startsWith("* ")) {
      if (!inList) {
        html.push("<ul>");
        inList = true;
      }
      html.push(`<li>${line.slice(2)}</li>`);
      continue;
    }

    if (inList) {
      html.push("</ul>");
      inList = false;
    }

    if (line.startsWith("### ")) html.push(`<h3>${line.slice(4)}</h3>`);
    else if (line.startsWith("## ")) html.push(`<h2>${line.slice(3)}</h2>`);
    else if (line.startsWith("# ")) html.push(`<h1>${line.slice(2)}</h1>`);
    else if (line.startsWith("> ")) html.push(`<blockquote>${line.slice(2)}</blockquote>`);
    else if (line.trim() === "") html.push("<br />");
    else html.push(`<p>${line}</p>`);
  }

  if (inList) html.push("</ul>");
  return html.join("\n");
}

function getFilteredCategories() {
  if (!state.query) return state.data.categories;
  const query = state.query.toLowerCase();

  return state.data.categories
    .map((category) => {
      const filteredAlgorithms = category.algorithms.filter((algorithm) => {
        const textBlob = [
          algorithm.title,
          algorithm.path,
          algorithm.explanation,
          ...algorithm.codeFiles.map((f) => `${f.name} ${f.language}`),
        ]
          .join(" ")
          .toLowerCase();

        return textBlob.includes(query) || category.title.toLowerCase().includes(query);
      });

      if (!filteredAlgorithms.length) return null;
      return { ...category, algorithms: filteredAlgorithms, algorithmCount: filteredAlgorithms.length };
    })
    .filter(Boolean);
}

function renderCategories() {
  const categories = getFilteredCategories();
  categoryList.innerHTML = "";

  if (!categories.length) {
    categoryList.innerHTML = "<p class='panel-subtle'>No matching domain found.</p>";
    algorithmList.innerHTML = "";
    algorithmDetails.innerHTML = "<p class='panel-placeholder'>Try a different search term.</p>";
    return;
  }

  if (!categories.find((c) => c.id === state.categoryId)) {
    state.categoryId = categories[0].id;
  }

  for (const category of categories) {
    const button = document.createElement("button");
    button.className = category.id === state.categoryId ? "active" : "";
    button.innerHTML = `<strong>${category.title}</strong><p class='panel-subtle'>${category.algorithmCount} algorithms</p>`;
    button.addEventListener("click", () => {
      state.categoryId = category.id;
      state.algorithmId = null;
      render();
    });
    categoryList.appendChild(button);
  }

  renderAlgorithmList(categories.find((c) => c.id === state.categoryId));
}

function renderAlgorithmList(category) {
  algorithmList.innerHTML = "";
  if (!category) {
    algorithmDetails.innerHTML = "<p class='panel-placeholder'>No algorithm available.</p>";
    return;
  }

  if (!category.algorithms.find((a) => a.id === state.algorithmId)) {
    state.algorithmId = category.algorithms[0]?.id ?? null;
  }

  for (const algorithm of category.algorithms) {
    const button = document.createElement("button");
    button.className = `algorithm-card ${algorithm.id === state.algorithmId ? "active" : ""}`;
    button.innerHTML = `<strong>${algorithm.title}</strong><p>${algorithm.codeFiles.length} files • ${algorithm.path}</p>`;
    button.addEventListener("click", () => {
      state.algorithmId = algorithm.id;
      state.selectedCodeFileName = null;
      renderAlgorithmDetails(algorithm);
      renderAlgorithmList(category);
    });
    algorithmList.appendChild(button);
  }

  renderAlgorithmDetails(category.algorithms.find((a) => a.id === state.algorithmId));
}

function renderAlgorithmDetails(algorithm) {
  if (!algorithm) {
    algorithmDetails.innerHTML = "<p class='panel-placeholder'>Select an algorithm to view details.</p>";
    return;
  }

  if (!algorithm.codeFiles.find((f) => f.name === state.selectedCodeFileName)) {
    state.selectedCodeFileName = algorithm.codeFiles[0].name;
  }

  const activeCode = algorithm.codeFiles.find((f) => f.name === state.selectedCodeFileName) ?? algorithm.codeFiles[0];

  const tabs = algorithm.codeFiles
    .map(
      (file) =>
        `<button data-code-file='${file.name}' class='${file.name === activeCode.name ? "active" : ""}'>${file.language} • ${file.name}</button>`
    )
    .join("");

  algorithmDetails.innerHTML = `
    <h2>${algorithm.title}</h2>
    <p class='panel-subtle'>${algorithm.path}</p>
    <section class='explanation'>${markdownToHtml(algorithm.explanation)}</section>
    <div class='code-tab-bar'>${tabs}</div>
    <pre><code>${htmlEscape(activeCode.content)}</code></pre>
  `;

  algorithmDetails.querySelectorAll("[data-code-file]").forEach((tab) => {
    tab.addEventListener("click", (event) => {
      state.selectedCodeFileName = event.currentTarget.getAttribute("data-code-file");
      renderAlgorithmDetails(algorithm);
    });
  });
}

function render() {
  renderCategories();
}

async function bootstrap() {
  let progress = 5;
  const timer = setInterval(() => {
    progress = Math.min(progress + Math.random() * 12, 90);
    introBar.style.width = `${progress}%`;
  }, 180);

  const response = await fetch("./site-data.json", { cache: "no-store" });
  state.data = await response.json();

  clearInterval(timer);
  introBar.style.width = "100%";

  searchInput.addEventListener("input", (event) => {
    state.query = event.target.value.trim();
    render();
  });

  render();
  setTimeout(() => intro.classList.add("done"), 500);
}

bootstrap().catch((error) => {
  intro.classList.add("done");
  algorithmDetails.innerHTML = `<p class='panel-placeholder'>Failed to load website data: ${htmlEscape(String(error))}</p>`;
});
