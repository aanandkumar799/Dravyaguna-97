document.addEventListener("DOMContentLoaded", function () {
  const plantList = document.getElementById("plant-list");
  const searchInput = document.getElementById("search");

  if (!plantList) {
    console.error("Plant list element not found.");
    return;
  }

  let plants = [];

  // Show loading message
  plantList.innerHTML = `
    <p class="loading-message">
      Loading plants...
    </p>
  `;

  // Load plant database
  fetch("./plants.json?v=8", {
    cache: "no-store"
  })
    .then(function (response) {
      if (!response.ok) {
        throw new Error(
          "plants.json could not be loaded. HTTP status: " +
            response.status
        );
      }

      return response.text();
    })
    .then(function (text) {
      if (!text.trim()) {
        throw new Error("plants.json is empty.");
      }

      try {
        return JSON.parse(text);
      } catch (error) {
        throw new Error(
          "plants.json contains invalid JSON: " + error.message
        );
      }
    })
    .then(function (data) {
      if (!Array.isArray(data)) {
        throw new Error("Plant database must be a JSON array.");
      }

      plants = data;

      displayPlants(plants);
    })
    .catch(function (error) {
      console.error("DravyaGuna 97:", error);

      plantList.innerHTML = `
        <div class="database-error">
          <h3>Unable to load plant database</h3>
          <p>Please check your connection and refresh the page. If the problem continues, the plant database may be temporarily unavailable.</p>
        </div>
      `;
      plantList.setAttribute("aria-busy", "false");
    });

  // Display plant cards
  function displayPlants(list) {
    plantList.innerHTML = "";
    plantList.setAttribute("aria-busy", "false");

    if (!list || list.length === 0) {
      plantList.innerHTML = `
        <div class="database-error">
          <h3>No plants found</h3>
          <p>Try another search.</p>
        </div>
      `;
      return;
    }

    list.forEach(function (plant) {
      if (!plant || !plant.id) {
        return;
      }

      const card = document.createElement("div");
      card.className = "user-card plant-card";

      const name =
        plant.name ||
        plant.sanskrit_name ||
        "Unnamed Plant";

      const sanskrit =
        plant.sanskrit_name || "";

      const botanical =
        plant.botanical_name || "";

      const family =
        plant.family || "";

      card.innerHTML = `
        <div class="icon">🌿</div>

        <h2>${escapeHTML(name)}</h2>

        ${
          sanskrit
            ? `<p>${escapeHTML(sanskrit)}</p>`
            : ""
        }

        ${
          botanical
            ? `<p><em>${escapeHTML(botanical)}</em></p>`
            : ""
        }

        ${
          family
            ? `<p>Family: ${escapeHTML(family)}</p>`
            : ""
        }

        <a
          href="./plant.html?id=${encodeURIComponent(plant.id)}"
          class="plant-button"
        >
          View Plant →
        </a>
      `;

      plantList.appendChild(card);
    });
  }

  // Search
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const query = searchInput.value
        .trim()
        .toLowerCase();

      if (!query) {
        displayPlants(plants);
        return;
      }

      const filteredPlants = plants.filter(function (plant) {
        if (!plant) {
          return false;
        }

        const searchableText = [
          plant.name,
          plant.sanskrit_name,
          plant.transliteration,
          plant.botanical_name,
          plant.family,
          plant.english_name,
          plant.hindi_name,
          plant.id
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();

        return searchableText.includes(query);
      });

      displayPlants(filteredPlants);
    });
  }

  // Prevent broken HTML if plant data contains special characters
  function escapeHTML(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
});
