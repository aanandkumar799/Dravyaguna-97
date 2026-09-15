document.addEventListener("DOMContentLoaded", () => {
  const plantList = document.getElementById("plant-list");
  const searchInput = document.getElementById("search");

  const databaseURL =
    new URL("plants.json", window.location.href).href + "?v=23";

  const indexURL =
    new URL("plant-index.json", window.location.href).href + "?v=2";

  let masterPlants = [];
  let currentSearchTerm = "";

  /* =========================================================
     BASIC HELPERS
  ========================================================= */

  function escapeHTML(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function normalizeText(value) {
    if (value === null || value === undefined) return "";

    return String(value)
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/[^\p{L}\p{N}]+/gu, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function arrayToText(value) {
    if (!Array.isArray(value)) return "";
    return value
      .map(item => {
        if (typeof item === "object" && item !== null) {
          return Object.values(item).join(" ");
        }
        return String(item ?? "");
      })
      .join(" ");
  }

  function getIdentity(plant) {
    return plant?.identity || {};
  }

  function getPlantName(plant) {
    return (
      getIdentity(plant).name ||
      plant?.name ||
      ""
    );
  }

  function getSanskritName(plant) {
    return (
      getIdentity(plant).sanskrit_name ||
      plant?.sanskrit_name ||
      ""
    );
  }

  function getTransliteration(plant) {
    return (
      getIdentity(plant).transliteration ||
      plant?.transliteration ||
      ""
    );
  }

  function getBotanicalName(plant) {
    return (
      getIdentity(plant).botanical_name ||
      plant?.botanical_name ||
      ""
    );
  }

  function getFamily(plant) {
    return (
      getIdentity(plant).family ||
      plant?.family ||
      ""
    );
  }

  function getEnglishName(plant) {
    return (
      getIdentity(plant).english_name ||
      plant?.english_name ||
      ""
    );
  }

  function getHindiName(plant) {
    return (
      getIdentity(plant).hindi_name ||
      plant?.hindi_name ||
      ""
    );
  }

  function getImage(plant) {
    const images = plant?.images || {};

    return (
      images.whole_plant ||
      images.habit ||
      images.leaf ||
      ""
    );
  }

  function getOrder(plant) {
    const value = Number(plant?.order);
    return Number.isFinite(value) ? value : 9999;
  }

  function getStatus(plant) {
    return (
      plant?.metadata?.status ||
      plant?.status ||
      "draft"
    );
  }

  function getSyllabusMarker(plant) {
    return (
      plant?.syllabus_marker ||
      ""
    );
  }

  /* =========================================================
     SEARCH DATA
  ========================================================= */

  function collectSearchText(plant) {
    const identity = plant?.identity || {};
    const classification = plant?.classification || {};
    const identification = plant?.identification || {};
    const dravyaGuna =
      plant?.dravya_guna ||
      plant?.dravyaguna ||
      {};

    const dosha = plant?.dosha || {};
    const therapeutics = plant?.therapeutics || {};
    const phytochemistry = plant?.phytochemistry || {};
    const modern = plant?.modern_information || {};
    const student = plant?.student || {};
    const teacher = plant?.teacher || {};
    const doctor = plant?.doctor || {};

    const formulations = Array.isArray(plant?.formulations)
      ? plant.formulations
          .map(formulation =>
            Object.values(formulation || {}).join(" ")
          )
          .join(" ")
      : "";

    const classical =
      plant?.classical_reference || {};

    const synonyms = arrayToText(identity.synonyms);
    const regionalNames = arrayToText(identity.regional_names);

    const rasa = arrayToText(dravyaGuna.rasa);
    const guna = arrayToText(dravyaGuna.guna);
    const karma = arrayToText(dravyaGuna.karma);

    const usefulPart = arrayToText(
      therapeutics.useful_part
    );

    const indications = arrayToText(
      therapeutics.indications
    );

    const therapeuticActions = arrayToText(
      therapeutics.therapeutic_actions
    );

    const examPoints = arrayToText(
      student.exam_points
    );

    const vivaQuestions = arrayToText(
      student.viva_questions
    );

    const identificationPoints = arrayToText(
      student.identification_points
    );

    const teachingPoints = arrayToText(
      teacher.teaching_points
    );

    const discussionPoints = arrayToText(
      teacher.discussion_points
    );

    const practicalPoints = arrayToText(
      teacher.practical_points
    );

    const importantIndications = arrayToText(
      doctor.important_indications
    );

    const keyPrecautions = arrayToText(
      doctor.key_precautions
    );

    const sources = arrayToText(
      plant.sources
    );

    const shlokas = arrayToText(
      classical.shlokas
    );

    const nighantuReferences = arrayToText(
      classical.nighantu_references
    );

    const samhitaReferences = arrayToText(
      classical.samhita_references
    );

    const majorConstituents = arrayToText(
      phytochemistry.major_constituents
    );

    const recognizedUses = arrayToText(
      modern.recognized_uses
    );

    return [
      getPlantName(plant),
      getSanskritName(plant),
      getTransliteration(plant),
      getBotanicalName(plant),
      getFamily(plant),
      getEnglishName(plant),
      getHindiName(plant),

      synonyms,
      regionalNames,

      classification.kingdom,
      classification.habit,
      classification.habitat,
      classification.distribution,

      identification.description,
      identification.whole_plant,
      identification.root,
      identification.stem,
      identification.leaf,
      identification.flower,
      identification.fruit,
      identification.seed,
      identification.bark,
      arrayToText(
        identification.identification_points
      ),

      rasa,
      guna,
      dravyaGuna.virya,
      dravyaGuna.vipaka,
      dravyaGuna.prabhava,
      karma,

      dosha.vata,
      dosha.pitta,
      dosha.kapha,

      usefulPart,
      indications,
      therapeuticActions,
      therapeutics.dose,
      therapeutics.anupana,
      therapeutics.duration,
      therapeutics.precautions,
      therapeutics.contraindications,

      formulations,

      shlokas,
      nighantuReferences,
      samhitaReferences,

      majorConstituents,
      phytochemistry.chemical_notes,

      modern.evidence_summary,
      recognizedUses,
      modern.safety_notes,
      sources,

      examPoints,
      vivaQuestions,
      identificationPoints,
      student.mnemonics,
      student.quick_revision,

      teachingPoints,
      discussionPoints,
      practicalPoints,

      doctor.quick_reference,
      importantIndications,
      doctor.useful_part,
      doctor.dose,
      doctor.anupana,
      keyPrecautions,

      plant?.id,
      plant?.syllabus_marker,
      plant?.status,
      plant?.metadata?.status
    ].join(" ");
  }

  /* =========================================================
     SEARCH INDEX
  ========================================================= */

  function createSearchIndex(plant) {
    return {
      normalized: normalizeText(
        collectSearchText(plant)
      ),

      name: normalizeText(
        getPlantName(plant)
      ),

      sanskrit: normalizeText(
        getSanskritName(plant)
      ),

      transliteration: normalizeText(
        getTransliteration(plant)
      ),

      botanical: normalizeText(
        getBotanicalName(plant)
      ),

      family: normalizeText(
        getFamily(plant)
      ),

      english: normalizeText(
        getEnglishName(plant)
      ),

      hindi: normalizeText(
        getHindiName(plant)
      ),

      id: normalizeText(
        plant?.id || ""
      ),

      order: String(
        getOrder(plant)
      )
    };
  }

  /* =========================================================
     SEARCH SCORING
  ========================================================= */

  function scorePlant(plant, searchTerm) {
    const query = normalizeText(searchTerm);

    if (!query) return 0;

    const index = plant._searchIndex;

    if (!index) return 0;

    const queryWords = query
      .split(" ")
      .filter(Boolean);

    let score = 0;

    /*
      Exact matches receive the strongest score.
    */

    if (index.name === query) {
      score += 1000;
    }

    if (index.sanskrit === query) {
      score += 950;
    }

    if (index.transliteration === query) {
      score += 900;
    }

    if (index.botanical === query) {
      score += 850;
    }

    if (index.english === query) {
      score += 800;
    }

    if (index.hindi === query) {
      score += 800;
    }

    if (index.family === query) {
      score += 700;
    }

    if (index.id === query) {
      score += 750;
    }

    if (index.order === query) {
      score += 700;
    }

    /*
      Prefix matches.
    */

    if (index.name.startsWith(query)) {
      score += 600;
    }

    if (index.sanskrit.startsWith(query)) {
      score += 580;
    }

    if (index.transliteration.startsWith(query)) {
      score += 560;
    }

    if (index.botanical.startsWith(query)) {
      score += 540;
    }

    if (index.english.startsWith(query)) {
      score += 520;
    }

    if (index.hindi.startsWith(query)) {
      score += 520;
    }

    /*
      Partial field matches.
    */

    if (index.name.includes(query)) {
      score += 450;
    }

    if (index.sanskrit.includes(query)) {
      score += 430;
    }

    if (index.transliteration.includes(query)) {
      score += 410;
    }

    if (index.botanical.includes(query)) {
      score += 390;
    }

    if (index.english.includes(query)) {
      score += 370;
    }

    if (index.hindi.includes(query)) {
      score += 370;
    }

    if (index.family.includes(query)) {
      score += 300;
    }

    /*
      General database search.
    */

    if (index.normalized.includes(query)) {
      score += 150;
    }

    /*
      Multi-word search.

      Every individual search word must occur somewhere
      in the searchable database text.
    */

    if (queryWords.length > 1) {
      let matchedWords = 0;

      for (const word of queryWords) {
        if (index.normalized.includes(word)) {
          matchedWords++;
        }
      }

      if (matchedWords === queryWords.length) {
        score += 250;
      } else {
        score += matchedWords * 35;
      }
    }

    /*
      Small boost for developed profiles.
      This is NOT used to exclude draft plants.
    */

    if (
      getStatus(plant) === "verified" ||
      getStatus(plant) === "complete"
    ) {
      score += 5;
    }

    return score;
  }

  function searchPlants(searchTerm) {
    const query = normalizeText(searchTerm);

    if (!query) {
      return [...masterPlants].sort(
        (a, b) => getOrder(a) - getOrder(b)
      );
    }

    return masterPlants
      .map(plant => ({
        plant,
        score: scorePlant(plant, query)
      }))
      .filter(item => item.score > 0)
      .sort((a, b) => {
        if (b.score !== a.score) {
          return b.score - a.score;
        }

        return getOrder(a.plant) - getOrder(b.plant);
      })
      .map(item => item.plant);
  }

  /* =========================================================
     HIGHLIGHT SEARCH MATCH
  ========================================================= */

  function highlightText(value, searchTerm) {
    const text = String(value ?? "");

    if (!searchTerm) {
      return escapeHTML(text);
    }

    const escaped = escapeHTML(text);
    const normalizedQuery = normalizeText(searchTerm);

    if (!normalizedQuery) {
      return escaped;
    }

    /*
      Highlighting is intentionally limited to simple
      Latin-text matches so Sanskrit text is never damaged.
    */

    const safeQuery = normalizedQuery
      .replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

    if (!safeQuery) {
      return escaped;
    }

    try {
      return escaped.replace(
        new RegExp(`(${safeQuery})`, "gi"),
        "<mark>$1</mark>"
      );
    } catch {
      return escaped;
    }
  }

  /* =========================================================
     MASTER LIST
  ========================================================= */

  function buildMasterPlantList(
    detailedPlants,
    plantIndex
  ) {
    const detailedMap = new Map();

    detailedPlants.forEach(plant => {
      if (
        plant &&
        typeof plant === "object" &&
        typeof plant.id === "string" &&
        plant.id.trim()
      ) {
        detailedMap.set(
          plant.id.trim(),
          plant
        );
      }
    });

    const merged = plantIndex.map(indexPlant => {
      const detailedPlant =
        detailedMap.get(indexPlant.id);

      if (detailedPlant) {
        return {
          ...indexPlant,
          ...detailedPlant,
          order:
            detailedPlant.order ||
            indexPlant.order,

          syllabus_marker:
            detailedPlant.syllabus_marker ||
            indexPlant.syllabus_marker,

          _indexStatus:
            indexPlant.status || "draft"
        };
      }

      return {
        ...indexPlant,

        identity: {
          name:
            indexPlant.name || "",

          sanskrit_name:
            indexPlant.sanskrit_name || ""
        },

        metadata: {
          status:
            indexPlant.status || "draft"
        }
      };
    });

    return merged
      .sort(
        (a, b) =>
          getOrder(a) - getOrder(b)
      )
      .map(plant => {
        plant._searchIndex =
          createSearchIndex(plant);

        return plant;
      });
  }

  /* =========================================================
     PLANT CARD
  ========================================================= */

  function renderPlantCard(
    plant,
    searchTerm = ""
  ) {
    const name = getPlantName(plant);
    const sanskrit = getSanskritName(plant);
    const botanical = getBotanicalName(plant);
    const family = getFamily(plant);
    const english = getEnglishName(plant);
    const image = getImage(plant);

    const order = getOrder(plant);

    const marker =
      getSyllabusMarker(plant);

    const status =
      getStatus(plant);

    const isDeveloped =
      status === "verified" ||
      status === "complete";

    const plantId =
      plant?.id || "";

    const safePlantId =
      encodeURIComponent(plantId);

    const imageHTML = image
      ? `
        <img
          src="${escapeHTML(image)}"
          alt="${escapeHTML(name)}"
          loading="lazy"
          onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
        >
        <div class="plant-placeholder" style="display:none;">
          🌿
        </div>
      `
      : `
        <div class="plant-placeholder">
          🌿
        </div>
      `;

    const statusHTML = isDeveloped
      ? ""
      : `
        <span class="plant-status">
          Profile in development
        </span>
      `;

    const markerHTML = marker
      ? `
        <span class="syllabus-marker">
          ${escapeHTML(marker)}
        </span>
      `
      : "";

    return `
      <article
        class="plant-card"
        data-plant-id="${escapeHTML(plantId)}"
        data-order="${order}"
      >

        <div class="plant-image">
          ${imageHTML}
        </div>

        <div class="plant-card-content">

          <div class="plant-card-top">
            <span class="plant-number">
              ${order}
            </span>

            ${markerHTML}
          </div>

          <h3>
            ${highlightText(name, searchTerm)}
          </h3>

          ${
            sanskrit
              ? `
                <p class="plant-sanskrit">
                  ${highlightText(
                    sanskrit,
                    searchTerm
                  )}
                </p>
              `
              : ""
          }

          ${
            botanical
              ? `
                <p class="plant-botanical">
                  ${highlightText(
                    botanical,
                    searchTerm
                  )}
                </p>
              `
              : ""
          }

          ${
            english
              ? `
                <p class="plant-english">
                  ${highlightText(
                    english,
                    searchTerm
                  )}
                </p>
              `
              : ""
          }

          ${
            family
              ? `
                <p class="plant-family">
                  <strong>Family:</strong>
                  ${highlightText(
                    family,
                    searchTerm
                  )}
                </p>
              `
              : ""
          }

          ${statusHTML}

          <a
            class="view-plant"
            href="./plant.html?id=${safePlantId}"
          >
            View Plant →
          </a>

        </div>
      </article>
    `;
  }

  /* =========================================================
     RESULT INFORMATION
  ========================================================= */

  function updateSearchResultInfo(
    count,
    total,
    searchTerm
  ) {
    let info =
      document.getElementById(
        "search-result-info"
      );

    if (!info) {
      info = document.createElement("div");
      info.id = "search-result-info";

      if (searchInput?.parentNode) {
        searchInput.parentNode.insertBefore(
          info,
          searchInput.nextSibling
        );
      }
    }

    if (!searchTerm) {
      info.textContent =
        `${total} plants in the NCISM Dravyaguna library`;

      info.style.display = "block";
      return;
    }

    info.textContent =
      `${count} ${count === 1 ? "plant" : "plants"} found for "${searchTerm}"`;

    info.style.display = "block";
  }

  /* =========================================================
     EMPTY RESULT
  ========================================================= */

  function renderNoResults(searchTerm) {
    plantList.innerHTML = `
      <div class="no-results">
        <div style="font-size:3rem;">🔎</div>

        <h3>No plants found</h3>

        <p>
          No plant matched
          <strong>${escapeHTML(searchTerm)}</strong>.
        </p>

        <p>
          Try the common name, Sanskrit name,
          botanical name, family, formulation,
          therapeutic use, or NCISM number.
        </p>

        <button
          type="button"
          id="clear-search"
        >
          Clear Search
        </button>
      </div>
    `;

    const clearButton =
      document.getElementById(
        "clear-search"
      );

    if (clearButton) {
      clearButton.addEventListener(
        "click",
        () => {
          if (searchInput) {
            searchInput.value = "";
            searchInput.focus();
          }

          currentSearchTerm = "";

          renderPlants("");
        }
      );
    }
  }

  /* =========================================================
     RENDER PLANTS
  ========================================================= */

  function renderPlants(searchTerm = "") {
    currentSearchTerm = searchTerm;

    const results =
      searchPlants(searchTerm);

    updateSearchResultInfo(
      results.length,
      masterPlants.length,
      searchTerm
    );

    if (!results.length) {
      renderNoResults(searchTerm);
      return;
    }

    plantList.innerHTML =
      results
        .map(plant =>
 
