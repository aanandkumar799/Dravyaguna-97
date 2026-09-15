document.addEventListener("DOMContentLoaded", () => {
  const plantList = document.getElementById("plant-list");
  const searchInput = document.getElementById("search");

  if (!plantList) {
    console.error("Plant list element not found.");
    return;
  }

  let plants = [];

  const databaseURL =
    new URL("plants.json", window.location.href).href + "?v=21";

  function escapeHTML(value) {
    if (value === null || value === undefined) return "";

    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function arrayToText(value) {
    if (Array.isArray(value)) return value.join(", ");
    return value || "";
  }

  function getIdentity(plant) {
    return plant.identity || {};
  }

  function getPlantName(plant) {
    const identity = getIdentity(plant);

    return (
      identity.name ||
      plant.name ||
      "Unnamed Plant"
    );
  }

  function getSanskritName(plant) {
    const identity = getIdentity(plant);

    return (
      identity.sanskrit_name ||
      plant.sanskrit_name ||
      ""
    );
  }

  function getBotanicalName(plant) {
    const identity = getIdentity(plant);

    return (
      identity.botanical_name ||
      plant.botanical_name ||
      ""
    );
  }

  function getFamily(plant) {
    const identity = getIdentity(plant);

    return (
      identity.family ||
      plant.family ||
      ""
    );
  }

  function getEnglishName(plant) {
    const identity = getIdentity(plant);

    return (
      identity.english_name ||
      ""
    );
  }

  function getImage(plant) {
    return (
      plant.images?.whole_plant ||
      plant.images?.habit ||
      plant.image ||
      ""
    );
  }

  function renderPlants(list) {
    if (!list.length) {
      plantList.innerHTML = `
        <div class="empty-state">
          <h3>No plants found</h3>
          <p>
            Try searching by plant name, Sanskrit name,
            botanical name, family or synonym.
          </p>
        </div>
      `;
      return;
    }

    plantList.innerHTML = list
      .map((plant) => {
        const id = plant.id || "";
        const name = getPlantName(plant);
        const sanskrit = getSanskritName(plant);
        const botanical = getBotanicalName(plant);
        const family = getFamily(plant);
        const english = getEnglishName(plant);
        const image = getImage(plant);

        return `
          <article class="plant-card">

            ${
              image
                ? `
                  <div class="plant-card-image">
                    <img
                      src="${escapeHTML(image)}"
                      alt="${escapeHTML(name)} - whole plant"
                      loading="lazy"
                    >
                  </div>
                `
                : `
                  <div
                    class="plant-card-image plant-image-placeholder"
                    aria-hidden="true"
                  >
                    <span>🌿</span>
                  </div>
                `
            }

            <div class="plant-card-content">

              <h3>${escapeHTML(name)}</h3>

              ${
                sanskrit
                  ? `
                    <p class="sanskrit-name">
                      ${escapeHTML(sanskrit)}
                    </p>
                  `
                  : ""
              }

              ${
                botanical
                  ? `
                    <p class="botanical-name">
                      ${escapeHTML(botanical)}
                    </p>
                  `
                  : ""
              }

              ${
                english
                  ? `
                    <p>
                      <strong>English:</strong>
                      ${escapeHTML(english)}
                    </p>
                  `
                  : ""
              }

              ${
                family
                  ? `
                    <p class="plant-family">
                      <strong>Family:</strong>
                      ${escapeHTML(family)}
                    </p>
                  `
                  : ""
              }

              <a
                class="plant-card-button"
                href="./plant.html?id=${encodeURIComponent(id)}"
                aria-label="View details of ${escapeHTML(name)}"
              >
                View Plant →
              </a>

            </div>
          </article>
        `;
      })
      .join("");
  }

  function buildSearchText(plant) {
    const identity = getIdentity(plant);

    const fields = [
      plant.id,

      identity.name,
      identity.sanskrit_name,
      identity.transliteration,
      identity.botanical_name,
      identity.family,
      identity.english_name,
      identity.hindi_name,

      arrayToText(identity.regional_names),
      arrayToText(identity.synonyms),

      plant.name,
      plant.sanskrit_name,
      plant.botanical_name,
      plant.family,

      plant.classification?.habit,
      plant.classification?.habitat,

      plant.identification?.description,
      plant.identification?.identification_points
        ? arrayToText(
            plant.identification.identification_points
          )
        : "",

      plant.dravya_guna?.rasa
        ? arrayToText(plant.dravya_guna.rasa)
        : "",

      plant.dravya_guna?.guna
        ? arrayToText(plant.dravya_guna.guna)
        : "",

      plant.dravya_guna?.virya,
      plant.dravya_guna?.vipaka,

      plant.dravya_guna?.karma
        ? arrayToText(plant.dravya_guna.karma)
        : "",

      plant.therapeutics?.indications
        ? arrayToText(plant.therapeutics.indications)
        : "",

      plant.student?.exam_points
        ? arrayToText(plant.student.exam_points)
        : ""
    ];

    return fields
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
  }

  function filterPlants() {
    if (!searchInput) {
      renderPlants(plants);
      return;
    }

    const query = searchInput.value
      .trim()
      .toLowerCase();

    if (!query) {
      renderPlants(plants);
      return;
    }

    const filteredPlants = plants.filter((plant) =>
      buildSearchText(plant).includes(query)
    );

    renderPlants(filteredPlants);
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
          `plants.json request failed: ${response.status}`
        );
      }

      const text = await response.text();

      if (!text.trim()) {
        throw new Error("plants.json is empty.");
      }

      try {
        plants = JSON.parse(text);
      } catch (error) {
        throw new Error(
          "plants.json contains invalid JSON."
        );
      }

      if (!Array.isArray(plants)) {
        throw new Error(
          "plants.json must contain an array of plant records."
        );
      }

      plants = plants.filter(
        (plant) =>
          plant &&
          typeof plant === "object" &&
          typeof plant.id === "string" &&
          plant.id.trim() !== ""
      );

      if (!plants.length) {
        throw new Error(
          "No valid plant records were found."
        );
      }

      renderPlants(plants);

      if (searchInput) {
        searchInput.removeEventListener(
          "input",
          filterPlants
        );

        searchInput.addEventListener(
          "input",
          filterPlants
        );
      }

      console.log(
        `DravyaGuna database loaded successfully: ${plants.length} plant(s)`
      );

    } catch (error) {
      console.error(
        "DravyaGuna database error:",
        error
      );

      plantList.innerHTML = `
        <div class="error-state">
          <h3>Unable to load plant database</h3>

          <p>
            The plant database could not be loaded.
            Please try again.
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
