document.addEventListener("DOMContentLoaded", () => {
  const plantList = document.getElementById("plant-list");
  const searchInput = document.getElementById("search");

  if (!plantList) {
    console.error("Plant list element not found.");
    return;
  }

  let plants = [];

  const databaseURL =
    new URL("plants.json", window.location.href).href + "?v=20";

  function escapeHTML(value) {
    if (value === null || value === undefined) return "";

    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function getPlantName(plant) {
    return (
      plant?.identity?.name ||
      plant?.name ||
      "Unnamed Plant"
    );
  }

  function getBotanicalName(plant) {
    return (
      plant?.identity?.botanical_name ||
      plant?.botanical_name ||
      ""
    );
  }

  function getSanskritName(plant) {
    return (
      plant?.identity?.sanskrit_name ||
      plant?.sanskrit_name ||
      ""
    );
  }

  function getFamily(plant) {
    return (
      plant?.identity?.family ||
      plant?.family ||
      ""
    );
  }

  function getImage(plant) {
    return (
      plant?.images?.whole_plant ||
      plant?.images?.habit ||
      ""
    );
  }

  function renderPlants(list) {
    if (!list.length) {
      plantList.innerHTML = `
        <div class="empty-state">
          <h3>No plants found</h3>
          <p>Try another plant name, Sanskrit name, botanical name or family.</p>
        </div>
      `;
      return;
    }

    plantList.innerHTML = list
      .map((plant) => {
        const id = escapeHTML(plant.id || "");
        const name = escapeHTML(getPlantName(plant));
        const sanskrit = escapeHTML(getSanskritName(plant));
        const botanical = escapeHTML(getBotanicalName(plant));
        const family = escapeHTML(getFamily(plant));
        const image = getImage(plant);

        return `
          <article class="plant-card">

            ${
              image
                ? `
                  <div class="plant-card-image">
                    <img
                      src="${escapeHTML(image)}"
                      alt="${name} - whole plant"
                      loading="lazy"
                    >
                  </div>
                `
                : `
                  <div class="plant-card-image plant-image-placeholder">
                    <span>🌿</span>
                  </div>
                `
            }

            <div class="plant-card-content">

              <h3>${name}</h3>

              ${
                sanskrit
                  ? `<p class="sanskrit-name">${sanskrit}</p>`
                  : ""
              }

              ${
                botanical
                  ? `<p class="botanical-name">${botanical}</p>`
                  : ""
              }

              ${
                family
                  ? `<p class="plant-family">
                      <strong>Family:</strong> ${family}
                    </p>`
                  : ""
              }

              <a
                class="plant-card-button"
                href="./plant.html?id=${encodeURIComponent(
                  plant.id || ""
                )}"
                aria-label="View details of ${name}"
              >
                View Plant →
              </a>

            </div>
          </article>
        `;
      })
      .join("");
  }

  function filterPlants() {
    const query = searchInput
      ? searchInput.value.trim().toLowerCase()
      : "";

    if (!query) {
      renderPlants(plants);
      return;
    }

    const filtered = plants.filter((plant) => {
      const identity = plant.identity || {};

      const searchableText = [
        plant.id,
        identity.name,
        identity.sanskrit_name,
        identity.transliteration,
        identity.botanical_name,
        identity.family,
        identity.english_name,
        identity.hindi_name,
        ...(identity.regional_names || []),
        ...(identity.synonyms || [])
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();

      return searchableText.includes(query);
    });

    renderPlants(filtered);
  }

  async function loadPlants() {
    plantList.setAttribute("aria-busy", "true");

    plantList.innerHTML = `
      <p class="loading-message">
        Loading Dravyaguna plants...
      </p>
    `;

    try {
      const response = await fetch(databaseURL, {
        cache: "no-store"
      });

      if (!response.ok) {
        throw new Error(
          `Database request failed: ${response.status}`
        );
      }

      const text = await response.text();

      if (!text.trim()) {
        throw new Error("plants.json is empty.");
      }

      try {
        plants = JSON.parse(text);
      } catch (jsonError) {
        throw new Error(
          "plants.json contains invalid JSON."
        );
      }

      if (!Array.isArray(plants)) {
        throw new Error(
          "plants.json must contain an array of plants."
        );
      }

      plants = plants.filter(
        (plant) =>
          plant &&
          typeof plant === "object" &&
          plant.id
      );

      renderPlants(plants);

      if (searchInput) {
        searchInput.addEventListener(
          "input",
          filterPlants
        );
      }

      console.log(
        `DravyaGuna database loaded: ${plants.length} plant(s)`
      );

    } catch (error) {
      console.error("Plant database error:", error);

      plantList.innerHTML = `
        <div class="error-state">
          <h3>Unable to load plant database</h3>
          <p>
            Please check the plants.json file and try again.
          </p>

          <button
            type="button"
            id="retry-plants"
            class="plant-card-button"
          >
            Retry
          </button>
        </div>
      `;

      const retryButton =
        document.getElementById("retry-plants");

      if (retryButton) {
        retryButton.addEventListener(
          "click",
          loadPlants
        );
      }

    } finally {
      plantList.setAttribute("aria-busy", "false");
    }
  }

  loadPlants();
});
