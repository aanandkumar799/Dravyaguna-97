document.addEventListener("DOMContentLoaded", () => {
  const plantList = document.getElementById("plant-list");
  const searchInput = document.getElementById("search");

  const databaseURL = new URL("plants.json", window.location.href).href;
  const indexURL = new URL("plant-index.json", window.location.href).href;

  let masterPlants = [];
  let searchTimer = null;
  let showAllPlants = false;
  const initialPlantLimit = 24;

  function escapeHTML(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function normalizeText(value) {
    return String(value ?? "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/[^\p{L}\p{N}]+/gu, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function toSearchableText(value) {
    if (Array.isArray(value)) {
      return value.map(toSearchableText).join(" ");
    }
    if (value && typeof value === "object") {
      return Object.values(value).map(toSearchableText).join(" ");
    }
    return String(value ?? "");
  }

  function identity(plant) { return plant?.identity || {}; }
  function name(plant) { return identity(plant).name || plant?.name || ""; }
  function sanskrit(plant) { return identity(plant).sanskrit_name || plant?.sanskrit_name || ""; }
  function transliteration(plant) { return identity(plant).transliteration || plant?.transliteration || ""; }
  function botanical(plant) { return identity(plant).botanical_name || plant?.botanical_name || ""; }
  function family(plant) { return identity(plant).family || plant?.family || ""; }
  function english(plant) { return identity(plant).english_name || plant?.english_name || ""; }
  function hindi(plant) { return identity(plant).hindi_name || plant?.hindi_name || ""; }
  function order(plant) {
    const n = Number(plant?.order);
    return Number.isFinite(n) ? n : 9999;
  }
  function status(plant) {
    return plant?.metadata?.status || plant?.status || "draft";
  }
  function marker(plant) { return plant?.syllabus_marker || ""; }

  function image(plant) {
    const images = plant?.images || {};
    return images.whole_plant || images.habit || images.leaf || "";
  }

  function searchableText(plant) {
    return toSearchableText(plant);
  }

  function makeSearchIndex(plant) {
    return {
      all: normalizeText(searchableText(plant)),
      name: normalizeText(name(plant)),
      sanskrit: normalizeText(sanskrit(plant)),
      transliteration: normalizeText(transliteration(plant)),
      botanical: normalizeText(botanical(plant)),
      family: normalizeText(family(plant)),
      english: normalizeText(english(plant)),
      hindi: normalizeText(hindi(plant)),
      id: normalizeText(plant?.id),
      order: String(order(plant))
    };
  }

  function scorePlant(plant, rawQuery) {
    const query = normalizeText(rawQuery);
    if (!query) return 0;

    const idx = plant._searchIndex;
    const words = query.split(" ").filter(Boolean);
    let score = 0;

    const exactFields = [
      [idx.name, 1000], [idx.sanskrit, 950], [idx.transliteration, 900],
      [idx.botanical, 850], [idx.english, 800], [idx.hindi, 800],
      [idx.id, 750], [idx.family, 700], [idx.order, 700]
    ];
    exactFields.forEach(([field, points]) => {
      if (field && field === query) score += points;
    });

    const prefixFields = [
      [idx.name, 600], [idx.sanskrit, 580], [idx.transliteration, 560],
      [idx.botanical, 540], [idx.english, 520], [idx.hindi, 520], [idx.family, 300]
    ];
    prefixFields.forEach(([field, points]) => {
      if (field && field.startsWith(query)) score += points;
    });

    const partialFields = [
      [idx.name, 450], [idx.sanskrit, 430], [idx.transliteration, 410],
      [idx.botanical, 390], [idx.english, 370], [idx.hindi, 370], [idx.family, 300]
    ];
    partialFields.forEach(([field, points]) => {
      if (field && field.includes(query)) score += points;
    });

    if (idx.all.includes(query)) score += 150;

    if (words.length > 1) {
      const matched = words.filter(word => idx.all.includes(word)).length;
      score += matched === words.length ? 250 : matched * 35;
    }

    return score;
  }

  function searchPlants(query) {
    const normalized = normalizeText(query);
    if (!normalized) return [...masterPlants];

    return masterPlants
      .map(plant => ({ plant, score: scorePlant(plant, query) }))
      .filter(item => item.score > 0)
      .sort((a, b) => b.score - a.score || order(a.plant) - order(b.plant))
      .map(item => item.plant);
  }

  function highlight(value, query) {
    const text = String(value ?? "");
    const normalized = normalizeText(query);
    if (!normalized || !/^[\x00-\x7F]*$/.test(normalized)) return escapeHTML(text);

    const escapedText = escapeHTML(text);
    const escapedQuery = normalized.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    if (!escapedQuery) return escapedText;

    try {
      return escapedText.replace(new RegExp(`(${escapedQuery})`, "gi"), "<mark>$1</mark>");
    } catch {
      return escapedText;
    }
  }

  function buildMasterList(detailedPlants, indexPlants) {
    const detailMap = new Map();
    detailedPlants.forEach(plant => {
      if (plant && typeof plant.id === "string" && plant.id.trim()) {
        detailMap.set(plant.id.trim(), plant);
      }
    });

    return indexPlants
      .map(indexPlant => {
        const detailed = detailMap.get(indexPlant.id);
        if (detailed) {
          return {
            ...indexPlant,
            ...detailed,
            order: detailed.order || indexPlant.order,
            syllabus_marker: detailed.syllabus_marker || indexPlant.syllabus_marker
          };
        }
        return {
          ...indexPlant,
          identity: {
            name: indexPlant.name || "",
            sanskrit_name: indexPlant.sanskrit_name || ""
          },
          metadata: { status: indexPlant.status || "draft" }
        };
      })
      .sort((a, b) => order(a) - order(b))
      .map(plant => {
        plant._searchIndex = makeSearchIndex(plant);
        return plant;
      });
  }

  function renderCard(plant, query) {
    const plantName = name(plant);
    const plantImage = image(plant);
    const developed = ["verified", "complete"].includes(status(plant));
    const id = String(plant?.id || "");

    const imageHTML = plantImage
      ? `<img src="${escapeHTML(plantImage)}" alt="${escapeHTML(plantName)}" loading="lazy" data-fallback="true"><div class="plant-placeholder" hidden>🌿</div>`
      : `<div class="plant-placeholder">🌿</div>`;

    return `<article class="plant-card" data-plant-id="${escapeHTML(id)}">
      <div class="plant-image">${imageHTML}</div>
      <div class="plant-card-content">
        <div class="plant-card-top">
          <span class="plant-number">${order(plant)}</span>
          ${marker(plant) ? `<span class="syllabus-marker">${escapeHTML(marker(plant))}</span>` : ""}
        </div>
        <h3>${highlight(plantName, query)}</h3>
        ${sanskrit(plant) ? `<p class="plant-sanskrit">${highlight(sanskrit(plant), query)}</p>` : ""}
        ${botanical(plant) ? `<p class="plant-botanical"><em>${highlight(botanical(plant), query)}</em></p>` : ""}
        ${english(plant) ? `<p class="plant-english">${highlight(english(plant), query)}</p>` : ""}
        ${family(plant) ? `<p class="plant-family"><strong>Family:</strong> ${highlight(family(plant), query)}</p>` : ""}
        ${!developed ? `<span class="plant-status">Profile in development</span>` : ""}
        <a class="view-plant" href="./plant.html?id=${encodeURIComponent(id)}">View Plant →</a>
      </div>
    </article>`;
  }

  function updateResultInfo(count, query) {
    let info = document.getElementById("search-result-info");
    if (!info && searchInput?.parentNode) {
      info = document.createElement("div");
      info.id = "search-result-info";
      searchInput.parentNode.insertBefore(info, searchInput.nextSibling);
    }
    if (!info) return;
    info.textContent = query
      ? `${count} ${count === 1 ? "plant" : "plants"} found for "${query}"`
      : `${masterPlants.length} plants in the NCISM Dravyaguna library`;
  }

  function renderNoResults(query) {
    plantList.innerHTML = `<div class="no-results">
      <div style="font-size:3rem">🔎</div>
      <h3>No plants found</h3>
      <p>No plant matched <strong>${escapeHTML(query)}</strong>.</p>
      <p>Try a common name, Sanskrit name, botanical name, family, formulation, therapeutic use, or NCISM number.</p>
      <button type="button" id="clear-search">Clear Search</button>
    </div>`;
    document.getElementById("clear-search")?.addEventListener("click", () => {
      searchInput.value = "";
      showAllPlants = false;
      renderPlants("");
      searchInput.focus();
    });
  }

  function renderPlants(query = "") {
    const results = searchPlants(query);
    updateResultInfo(results.length, query);
    if (!results.length) {
      renderNoResults(query);
      return;
    }

    const visibleResults = query || showAllPlants ? results : results.slice(0, initialPlantLimit);
    plantList.innerHTML = visibleResults.map(plant => renderCard(plant, query)).join("") +
      (!query && !showAllPlants && results.length > initialPlantLimit
        ? `<div class="plant-list-actions"><p>Showing ${initialPlantLimit} of ${results.length} plants.</p><button type="button" id="show-all-plants">Show all ${results.length} plants</button></div>`
        : "");

    plantList.querySelectorAll('img[data-fallback="true"]').forEach(img => {
      img.addEventListener("error", () => {
        img.hidden = true;
        const fallback = img.nextElementSibling;
        if (fallback) fallback.hidden = false;
      }, { once: true });
    });

    document.getElementById("show-all-plants")?.addEventListener("click", () => {
      showAllPlants = true;
      renderPlants(searchInput?.value || "");
    });
  }

  function renderLoading() {
    plantList.innerHTML = `<div class="loading-plants"><div style="font-size:2.5rem">🌿</div><p>Loading Dravyaguna plant library…</p></div>`;
    plantList.setAttribute("aria-busy", "true");
  }

  function renderError(message) {
    plantList.innerHTML = `<div class="plant-error"><div style="font-size:2.5rem">⚠️</div><h3>Unable to load the plant library</h3><p>${escapeHTML(message)}</p><button type="button" id="retry-load">Retry</button></div>`;
    plantList.setAttribute("aria-busy", "false");
    document.getElementById("retry-load")?.addEventListener("click", loadDatabase);
  }

  async function fetchJSON(url, label) {
    const response = await fetch(url, { cache: "no-store", headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error(`${label} returned HTTP ${response.status}`);
    const contentType = response.headers.get("content-type") || "";
    if (!contentType.includes("json") && !url.endsWith(".json")) throw new Error(`${label} returned an unexpected content type`);
    return response.json();
  }

  async function loadDatabase() {
    if (!plantList) return;
    renderLoading();
    try {
      const [detailedPlants, indexData] = await Promise.all([
        fetchJSON(databaseURL, "plants.json"),
        fetchJSON(indexURL, "plant-index.json")
      ]);

      if (!Array.isArray(detailedPlants)) throw new Error("plants.json must contain an array of plant records.");
      if (!indexData || !Array.isArray(indexData.plants)) throw new Error("plant-index.json must contain a plants array.");

      const validDetailed = detailedPlants.filter(plant => plant && typeof plant.id === "string" && plant.id.trim());
      const validIndex = indexData.plants.filter(plant => plant && typeof plant.id === "string" && plant.id.trim());
      if (!validIndex.length) throw new Error("plant-index.json contains no valid plant records.");

      masterPlants = buildMasterList(validDetailed, validIndex);
      if (masterPlants.length !== validIndex.length) throw new Error("Plant index could not be resolved into the master library.");

      plantList.setAttribute("aria-busy", "false");
      renderPlants(searchInput?.value || "");
      console.log(`DravyaGuna 97 loaded: ${masterPlants.length} plants`);
    } catch (error) {
      console.error("Dravyaguna database error:", error);
      renderError(error?.message || "An unexpected error occurred while loading the database.");
    }
  }

  if (searchInput) {
    searchInput.addEventListener("input", event => {
      clearTimeout(searchTimer);
      const value = event.target.value;
      if (!value.trim()) showAllPlants = false;
      searchTimer = setTimeout(() => renderPlants(value), 80);
    });

    searchInput.addEventListener("keydown", event => {
      if (event.key === "Enter") {
        event.preventDefault();
        clearTimeout(searchTimer);
        renderPlants(searchInput.value);
      } else if (event.key === "Escape") {
        event.preventDefault();
        clearTimeout(searchTimer);
        searchInput.value = "";
        showAllPlants = false;
        renderPlants("");
        searchInput.focus();
      }
    });
  }

  if (!plantList) {
    console.warn("Dravyaguna: #plant-list was not found.");
    return;
  }

  loadDatabase();
});
