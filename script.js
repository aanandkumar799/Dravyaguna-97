document.addEventListener("DOMContentLoaded", () => {
  const plantList = document.getElementById("plant-list");
  const searchInput = document.getElementById("search");

  if (!plantList) {
    console.error("Plant list element not found.");
    return;
  }

  let plants = [];
  let plantIndex = [];

  /*
   * Main detailed database
   * Contains fully developed plant records such as Ashwagandha.
   */
  const databaseURL =
    new URL("plants.json", window.location.href).href + "?v=22";

  /*
   * Master NCISM 97-plant index
   * Contains all 97 syllabus plants and their permanent IDs.
   */
  const indexURL =
    new URL("plant-index.json", window.location.href).href + "?v=1";

  function escapeHTML(value) {
    if (value === null || value === undefined) {
      return "";
    }

    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function arrayToText(value) {
    if (Array.isArray(value)) {
      return value.join(", ");
    }

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
      plant.english_name ||
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

  /*
   * Creates a searchable text block for each plant.
   */
  function buildSearchText(plant) {
    const identity = getIdentity(plant);

    const fields = [
      plant.id,
      plant.order,
      plant.name,
      plant.sanskrit_name,
      plant.botanical_name,
      plant.family,
      plant.english_name,
      plant.syllabus_marker,

      identity.name,
      identity.sanskrit_name,
      identity.transliteration,
      identity.botanical_name,
      identity.family,
      identity.english_name,
      identity.hindi_name,

      arrayToText(identity.regional_names),
      arrayToText(identity.synonyms),

      plant.classification?.habit,
      plant.classification?.habitat,
      plant.classification?.distribution,

      plant.identification?.description,
      plant.identification?.whole_plant,
      plant.identification?.root,
      plant.identification?.stem,
      plant.identification?.leaf,
      plant.identification?.flower,
      plant.identification?.fruit,
      plant.identification?.seed,
      plant.identification?.bark,

      arrayToText(
        plant.identification?.identification_points
      ),

      arrayToText(
        plant.dravya_guna?.rasa
      ),

      arrayToText(
        plant.dravya_guna?.guna
      ),

      plant.dravya_guna?.virya,
      plant.dravya_guna?.vipaka,
      plant.dravya_guna?.prabhava,

      arrayToText(
        plant.dravya_guna?.karma
      ),

      plant.dosha?.vata,
      plant.dosha?.pitta,
      plant.dosha?.kapha,

      arrayToText(
        plant.therapeutics?.useful_part
      ),

      arrayToText(
        plant.therapeutics?.indications
      ),

      arrayToText(
        plant.therapeutics?.therapeutic_actions
      ),

      plant.therapeutics?.dose,
      plant.therapeutics?.anupana,

      arrayToText(
        plant.student?.exam_points
      ),

      arrayToText(
        plant.student?.viva_questions
      ),

      arrayToText(
        plant.student?.identification_points
      ),

      arrayToText(
        plant.student?.mnemonics
      ),

      plant.student?.quick_revision,

      plant.teacher?.teaching_points,
      plant.teacher?.discussion_points,
      plant.teacher?.practical_points,

      plant.doctor?.quick_reference,

      arrayToText(
        plant.doctor?.important_indications
      )
    ];

    return fields
      .filter(
        (value) =>
          value !== null &&
          value !== undefined &&
          value !== ""
      )
      .join(" ")
      .toLowerCase();
  }

  /*
   * Merge the NCISM master index with the detailed database.
   *
   * The index guarantees all 97 plants appear.
   * The detailed database supplies richer information
   * whenever a plant has already been developed.
   */
  function buildMasterPlantList() {
    const detailedMap = new Map();

    plants.forEach((plant) => {
      if (
        plant &&
        typeof plant === "object" &&
        typeof plant.id === "string" &&
        plant.id.trim() !== ""
      ) {
        detailedMap.set(
          plant.id.trim(),
          plant
        );
      }
    });

    const merged = plantIndex.map((indexPlant) => {
      const detailedPlant =
        detailedMap.get(indexPlant.id);

      if (detailedPlant) {
        return {
          ...indexPlant,
          ...detailedPlant,
          order:
            detailedPlant.order ||
            indexPlant.order
        };
      }

      return {
        ...indexPlant,
        identity: {
          name: indexPlant.name || "",
          sanskrit_name:
            indexPlant.sanskrit_name || ""
        },

        metadata: {
          status:
            indexPlant.status || "draft"
        }
      };
    });

    /*
     * If a detailed plant exists that is not yet in the
     * master index, keep it visible rather than losing it.
     */
    const indexIDs = new Set(
      plantIndex.map((plant) => plant.id)
    );

    plants.forEach((plant) => {
      if (
        plant &&
        typeof plant.id === "string" &&
        plant.id.trim() !== "" &&
        !indexIDs.has(plant.id)
      ) {
        merged.push(plant);
      }
    });

    /*
     * Maintain official syllabus order.
     */
    merged.sort((a, b) => {
      const orderA =
        Number(a.order) || 9999;

      const orderB =
        Number(b.order) || 9999;

      return orderA - orderB;
    });

    return merged;
  }

  function renderPlants(list) {
    if (!list.length) {
      plantList.innerHTML = `
        <div class="empty-state">
          <h3>No plants found</h3>

          <p>
            Try searching by plant name,
            Sanskrit name, botanical name,
            family or synonym.
          </p>
        </div>
      `;

      return;
    }

    plantList.innerHTML = list
      .map((plant) => {
        const id =
          plant.id || "";

        const name =
          getPlantName(plant);

        const sanskrit =
          getSanskritName(plant);

        const botanical =
          getBotanicalName(plant);

        const family =
          getFamily(plant);

        const english =
          getEnglishName(plant);

        const image =
          getImage(plant);

        const order =
          plant.order || "";

        const marker =
          plant.syllabus_marker || "";

        const status =
          plant.metadata?.status ||
          plant.status ||
          "draft";

        return `
          <article
            class="plant-card"
            data-plant-id="${escapeHTML(id)}"
          >

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

              ${
                order
                  ? `
                    <div
                      class="plant-number"
                      aria-label="Syllabus number ${escapeHTML(order)}"
                    >
                      ${escapeHTML(order)}
                    </div>
                  `
                  : ""
              }

              <h3>
                ${escapeHTML(name)}
              </h3>

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

              ${
                marker
                  ? `
                    <span class="syllabus-marker">
                      ${escapeHTML(marker)}
                    </span>
                  `
                  : ""
              }

              ${
                status === "draft"
                  ? `
                    <span
                      class="plant-status"
                      title="Detailed profile is being developed"
                    >
                      Profile in development
                    </span>
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

  function filterPlants() {
    if (!searchInput) {
      renderPlants(plants);
      return;
    }

    const query =
      searchInput.value
        .trim()
        .toLowerCase();

    if (!query) {
      renderPlants(plants);
      return;
    }

    const filteredPlants =
      plants.filter((plant) =>
        buildSearchText(plant)
          .includes(query)
      );

    renderPlants(filteredPlants);
  }

  async function fetchJSON(url, errorMessage) {
    const response =
      await fetch(url, {
        cache: "no-store"
      });

    if (!response.ok) {
      throw new Error(
        `${errorMessage}: ${response.status}`
      );
    }

    const text =
      await response.text();

    if (!text.trim()) {
      throw new Error(
        `${errorMessage}: file is empty.`
      );
    }

    try {
      return JSON.parse(text);
    } catch (error) {
      throw new Error(
        `${errorMessage}: invalid JSON.`
      );
    }
  }

  async function loadPlants() {
    plantList.setAttribute(
      "aria-busy",
      "true"
    );

    plantList.innerHTML = `
      <p class="loading-message">
        Loading Dravyaguna plants...
      </p>
    `;

    try {
      /*
       * Load both files.
       */
      const [
        detailedDatabase,
        masterIndex
      ] = await Promise.all([
        fetchJSON(
          databaseURL,
          "plants.json"
        ),
        fetchJSON(
          indexURL,
          "plant-index.json"
        )
      ]);

      /*
       * Validate detailed database.
       */
      if (!Array.isArray(detailedDatabase)) {
        throw new Error(
          "plants.json must contain an array of plant records."
        );
      }

      plants =
        detailedDatabase.filter(
          (plant) =>
            plant &&
            typeof plant === "object" &&
            typeof plant.id === "string" &&
            plant.id.trim() !== ""
        );

      /*
       * Validate master index.
       */
      if (
        !masterIndex ||
        typeof masterIndex !== "object"
      ) {
        throw new Error(
          "plant-index.json must contain an object."
        );
      }

      if (
        !Array.isArray(
          masterIndex.plants
        )
      ) {
        throw new Error(
          "plant-index.json must contain a plants array."
        );
      }

      plantIndex =
        masterIndex.plants.filter(
          (plant) =>
            plant &&
            typeof plant === "object" &&
            typeof plant.id === "string" &&
            plant.id.trim() !== ""
        );

      if (!plantIndex.length) {
        throw new Error(
          "No valid plants were found in plant-index.json."
        );
      }

      /*
       * Build the complete 97-plant library.
       */
      plants =
        buildMasterPlantList();

      /*
       * Render all plants.
       */
      renderPlants(plants);

      /*
       * Connect search.
       */
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
        `DravyaGuna master library loaded successfully: ${plants.length} plant(s)`
      );

      console.log(
        `NCISM master index: ${plantIndex.length} plant(s)`
      );

    } catch (error) {
      console.error(
        "DravyaGuna database error:",
        error
      );

      plantList.innerHTML = `
        <div class="error-state">

          <h3>
            Unable to load plant database
          </h3>

          <p>
            The Dravyaguna plant database
            could not be loaded.
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
        document.getElementById(
          "retry-plants"
        );

      if (retryButton) {
        retryButton.addEventListener(
          "click",
          loadPlants
        );
      }

    } finally {
      plantList.setAttribute(
        "aria-busy",
        "false"
      );
    }
  }

  loadPlants();
});
