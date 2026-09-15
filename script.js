document.addEventListener("DOMContentLoaded", () => {
  const plantList = document.getElementById("plant-list");
  const searchInput = document.getElementById("search");

  const databaseURL =
    new URL("plants.json", window.location.href).href + "?v=24";

  const indexURL =
    new URL("plant-index.json", window.location.href).href + "?v=3";

  let masterPlants = [];
  let searchTimer = null;

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

  function arrayToText(value) {
    if (!Array.isArray(value)) return "";

    return value
      .map(item => {
        if (item && typeof item === "object") {
          return Object.values(item).join(" ");
        }

        return String(item ?? "");
      })
      .join(" ");
  }

  function identity(plant) {
    return plant?.identity || {};
  }

  function name(plant) {
    return identity(plant).name || plant?.name || "";
  }

  function sanskrit(plant) {
    return (
      identity(plant).sanskrit_name ||
      plant?.sanskrit_name ||
      ""
    );
  }

  function transliteration(plant) {
    return (
      identity(plant).transliteration ||
      plant?.transliteration ||
      ""
    );
  }

  function botanical(plant) {
    return (
      identity(plant).botanical_name ||
      plant?.botanical_name ||
      ""
    );
  }

  function family(plant) {
    return (
      identity(plant).family ||
      plant?.family ||
      ""
    );
  }

  function english(plant) {
    return (
      identity(plant).english_name ||
      plant?.english_name ||
      ""
    );
  }

  function hindi(plant) {
    return (
      identity(plant).hindi_name ||
      plant?.hindi_name ||
      ""
    );
  }

  function order(plant) {
    const n = Number(plant?.order);
    return Number.isFinite(n) ? n : 9999;
  }

  function status(plant) {
    return (
      plant?.metadata?.status ||
      plant?.status ||
      "draft"
    );
  }

  function marker(plant) {
    return plant?.syllabus_marker || "";
  }

  function image(plant) {
    const images = plant?.images || {};

    return (
      images.whole_plant ||
      images.habit ||
      images.leaf ||
      ""
    );
  }

  /* =========================================================
     SEARCHABLE DATABASE CONTENT
  ========================================================= */

  function searchableText(plant) {
    const i = identity(plant);
    const c = plant?.classification || {};
    const d = plant?.identification || {};
    const g =
      plant?.dravya_guna ||
      plant?.dravyaguna ||
      {};
    const dosha = plant?.dosha || {};
    const t = plant?.therapeutics || {};
    const ph = plant?.phytochemistry || {};
    const m = plant?.modern_information || {};
    const s = plant?.student || {};
    const teacher = plant?.teacher || {};
    const doctor = plant?.doctor || {};
    const classical =
      plant?.classical_reference || {};

    const formulations =
      Array.isArray(plant?.formulations)
        ? plant.formulations
            .map(item =>
              Object.values(item || {}).join(" ")
            )
            .join(" ")
        : "";

    return [
      plant?.id,
      plant?.order,
      plant?.syllabus_marker,

      name(plant),
      sanskrit(plant),
      transliteration(plant),
      botanical(plant),
      family(plant),
      english(plant),
      hindi(plant),

      arrayToText(i.synonyms),
      arrayToText(i.regional_names),

      c.kingdom,
      c.habit,
      c.habitat,
      c.distribution,

      d.description,
      d.whole_plant,
      d.root,
      d.stem,
      d.leaf,
      d.flower,
      d.fruit,
      d.seed,
      d.bark,
      arrayToText(d.identification_points),

      arrayToText(g.rasa),
      arrayToText(g.guna),
      g.virya,
      g.vipaka,
      g.prabhava,
      arrayToText(g.karma),

      dosha.vata,
      dosha.pitta,
      dosha.kapha,

      arrayToText(t.useful_part),
      arrayToText(t.indications),
      arrayToText(t.therapeutic_actions),
      t.dose,
      t.anupana,
      t.duration,
      t.precautions,
      t.contraindications,

      formulations,

      arrayToText(classical.shlokas),
      arrayToText(
        classical.nighantu_references
      ),
      arrayToText(
        classical.samhita_references
      ),

      arrayToText(ph.major_constituents),
      ph.chemical_notes,

      m.evidence_summary,
      arrayToText(m.recognized_uses),
      m.safety_notes,

      arrayToText(s.exam_points),
      arrayToText(s.viva_questions),
      arrayToText(s.identification_points),
      arrayToText(s.mnemonics),
      s.quick_revision,

      arrayToText(teacher.teaching_points),
      arrayToText(teacher.discussion_points),
      arrayToText(teacher.practical_points),

      doctor.quick_reference,
      arrayToText(
        doctor.important_indications
      ),
      doctor.useful_part,
      doctor.dose,
      doctor.anupana,
      arrayToText(
        doctor.key_precautions
      ),

      arrayToText(plant?.sources)
    ].join(" ");
  }

  /* =========================================================
     SEARCH INDEX
  ========================================================= */

  function makeSearchIndex(plant) {
    return {
      all: normalizeText(
        searchableText(plant)
      ),

      name: normalizeText(
        name(plant)
      ),

      sanskrit: normalizeText(
        sanskrit(plant)
      ),

      transliteration: normalizeText(
        transliteration(plant)
      ),

      botanical: normalizeText(
        botanical(plant)
      ),

      family: normalizeText(
        family(plant)
      ),

      english: normalizeText(
        english(plant)
      ),

      hindi: normalizeText(
        hindi(plant)
      ),

      id: normalizeText(
        plant?.id
      ),

      order: String(
        order(plant)
      )
    };
  }

  /* =========================================================
     SEARCH RELEVANCE SCORE
  ========================================================= */

  function scorePlant(plant, rawQuery) {
    const query = normalizeText(rawQuery);

    if (!query) return 0;

    const idx = plant._searchIndex;

    const words = query
      .split(" ")
      .filter(Boolean);

    let score = 0;

    const exactFields = [
      [idx.name, 1000],
      [idx.sanskrit, 950],
      [idx.transliteration, 900],
      [idx.botanical, 850],
      [idx.english, 800],
      [idx.hindi, 800],
      [idx.id, 750],
      [idx.family, 700],
      [idx.order, 700]
    ];

    exactFields.forEach(
      ([field, points]) => {
        if (field && field === query) {
          score += points;
        }
      }
    );

    const prefixFields = [
      [idx.name, 600],
      [idx.sanskrit, 580],
      [idx.transliteration, 560],
      [idx.botanical, 540],
      [idx.english, 520],
      [idx.hindi, 520],
      [idx.family, 300]
    ];

    prefixFields.forEach(
      ([field, points]) => {
        if (
          field &&
          field.startsWith(query)
        ) {
          score += points;
        }
      }
    );

    const partialFields = [
      [idx.name, 450],
      [idx.sanskrit, 430],
      [idx.transliteration, 410],
      [idx.botanical, 390],
      [idx.english, 370],
      [idx.hindi, 370],
      [idx.family, 300]
    ];

    partialFields.forEach(
      ([field, points]) => {
        if (
          field &&
          field.includes(query)
        ) {
          score += points;
        }
      }
    );

    if (idx.all.includes(query)) {
      score += 150;
    }

    if (words.length > 1) {
      const matched =
        words.filter(word =>
          idx.all.includes(word)
        ).length;

      if (matched === words.length) {
        score += 250;
      } else {
        score += matched * 35;
      }
    }

    return score;
  }

  function searchPlants(query) {
    const normalized =
      normalizeText(query);

    if (!normalized) {
      return [...masterPlants];
    }

    return masterPlants
      .map(plant => ({
        plant,
        score: scorePlant(
          plant,
          query
        )
      }))
      .filter(
        item => item.score > 0
      )
      .sort(
        (a, b) =>
          b.score - a.score ||
          order(a.plant) -
            order(b.plant)
      )
      .map(item => item.plant);
  }

  /* =========================================================
     SEARCH HIGHLIGHT
  ========================================================= */

  function highlight(value, query) {
    const text = String(value ?? "");

    const normalized =
      normalizeText(query);

    if (
      !normalized ||
      !/^[\x00-\x7F]*$/.test(
        normalized
      )
    ) {
      return escapeHTML(text);
    }

    const escapedText =
      escapeHTML(text);

    const escapedQuery =
      normalized.replace(
        /[.*+?^${}()|[\]\\]/g,
        "\\$&"
      );

    if (!escapedQuery) {
      return escapedText;
    }

    try {
      return escapedText.replace(
        new RegExp(
          `(${escapedQuery})`,
          "gi"
        ),
        "<mark>$1</mark>"
      );
    } catch {
      return escapedText;
    }
  }

  /* =========================================================
     BUILD MASTER 97-PLANT LIST
  ========================================================= */

  function buildMasterList(
    detailedPlants,
    indexPlants
  ) {
    const detailMap =
      new Map();

    detailedPlants.forEach(
      plant => {
        if (
          plant &&
          typeof plant.id ===
            "string" &&
          plant.id.trim()
        ) {
          detailMap.set(
            plant.id.trim(),
            plant
          );
        }
      }
    );

    return indexPlants
      .map(indexPlant => {
        const detailed =
          detailMap.get(
            indexPlant.id
          );

        if (detailed) {
          return {
            ...indexPlant,
            ...detailed,

            order:
              detailed.order ||
              indexPlant.order,

            syllabus_marker:
              detailed.syllabus_marker ||
              indexPlant.syllabus_marker
          };
        }

        return {
          ...indexPlant,

          identity: {
            name:
              indexPlant.name || "",

            sanskrit_name:
              indexPlant.sanskrit_name ||
              ""
          },

          metadata: {
            status:
              indexPlant.status ||
              "draft"
          }
        };
      })
      .sort(
        (a, b) =>
          order(a) -
          order(b)
      )
      .map(plant => {
        plant._searchIndex =
          makeSearchIndex(plant);

        return plant;
      });
  }

  /* =========================================================
     PLANT CARD
  ========================================================= */

  function renderCard(
    plant,
    query
  ) {
    const plantName =
      name(plant);

    const plantSanskrit =
      sanskrit(plant);

    const plantBotanical =
      botanical(plant);

    const plantEnglish =
      english(plant);

    const plantFamily =
      family(plant);

    const plantImage =
      image(plant);

    const plantOrder =
      order(plant);

    const plantMarker =
      marker(plant);

    const plantStatus =
      status(plant);

    const developed =
      plantStatus ===
        "verified" ||
      plantStatus ===
        "complete";

    const id =
      String(
        plant?.id || ""
      );

    const imageHTML =
      plantImage
        ? `
          <img
            src="${escapeHTML(
              plantImage
            )}"
            alt="${escapeHTML(
              plantName
            )}"
            loading="lazy"
            onerror="
              this.style.display='none';
              this.nextElementSibling.style.display='flex';
            "
          >

          <div
            class="plant-placeholder"
            style="display:none"
          >
            🌿
          </div>
        `
        : `
          <div class="plant-placeholder">
            🌿
          </div>
        `;

    return `
      <article
        class="plant-card"
        data-plant-id="${escapeHTML(
          id
        )}"
      >

        <div class="plant-image">
          ${imageHTML}
        </div>

        <div class="plant-card-content">

          <div class="plant-card-top">

            <span class="plant-number">
              ${plantOrder}
            </span>

            ${
              plantMarker
                ? `
                  <span class="syllabus-marker">
                    ${escapeHTML(
                      plantMarker
                    )}
                  </span>
                `
                : ""
            }

          </div>

          <h3>
            ${highlight(
              plantName,
              query
            )}
          </h3>

          ${
            plantSanskrit
              ? `
                <p class="plant-sanskrit">
                  ${highlight(
                    plantSanskrit,
                    query
                  )}
                </p>
              `
              : ""
          }

          ${
            plantBotanical
              ? `
                <p class="plant-botanical">
                  ${highlight(
                    plantBotanical,
                    query
                  )}
                </p>
              `
              : ""
          }

          ${
            plantEnglish
              ? `
                <p class="plant-english">
                  ${highlight(
                    plantEnglish,
                    query
                  )}
                </p>
              `
              : ""
          }

          ${
            plantFamily
              ? `
                <p class="plant-family">
                  <strong>
                    Family:
                  </strong>

                  ${highlight(
                    plantFamily,
                    query
                  )}
                </p>
              `
              : ""
          }

          ${
            !developed
              ? `
                <span class="plant-status">
                  Profile in development
                </span>
              `
              : ""
          }

          <a
            class="view-plant"
            href="./plant.html?id=${encodeURIComponent(
              id
            )}"
          >
            View Plant →
          </a>

        </div>

      </article>
    `;
  }

  /* =========================================================
     SEARCH RESULT INFORMATION
  ========================================================= */

  function updateResultInfo(
    count,
    query
  ) {
    let info =
      document.getElementById(
        "search-result-info"
      );

    if (
      !info &&
      searchInput?.parentNode
    ) {
      info =
        document.createElement(
          "div"
        );

      info.id =
        "search-result-info";

      searchInput.parentNode.insertBefore(
        info,
        searchInput.nextSibling
      );
    }

    if (!info) return;

    info.textContent = query
      ? `${count} ${
          count === 1
            ? "plant"
            : "plants"
        } found for "${query}"`
      : `${masterPlants.length} plants in the NCISM Dravyaguna library`;
  }

  /* =========================================================
     NO RESULTS
  ========================================================= */

  function renderNoResults(
    query
  ) {
    plantList.innerHTML = `
      <div class="no-results">

        <div style="font-size:3rem">
          🔎
        </div>

        <h3>
          No plants found
        </h3>

        <p>
          No plant matched
          <strong>
            ${escapeHTML(query)}
          </strong>.
        </p>

        <p>
          Try a common name,
          Sanskrit name,
          botanical name,
          family,
          formulation,
          therapeutic use,
          or NCISM number.
        </p>

        <button
          type="button"
          id="clear-search"
        >
          Clear Search
        </button>

      </div>
    `;

    document
      .getElementById(
        "clear-search"
      )
      ?.addEventListener(
        "click",
        () => {
          searchInput.value =
            "";

          renderPlants("");

          searchInput.focus();
        }
      );
  }

  /* =========================================================
     RENDER PLANTS
  ========================================================= */

  function renderPlants(
    query = ""
  ) {
    const results =
      searchPlants(query);

    updateResultInfo(
      results.length,
      query
    );

    if (!results.length) {
      renderNoResults(
        query
      );
      return;
    }

    plantList.innerHTML =
      results
        .map(plant =>
          renderCard(
            plant,
            query
          )
        )
        .join("");
  }

  /* =========================================================
     LOADING
  ========================================================= */

  function renderLoading() {
    plantList.innerHTML = `
      <div class="loading-plants">

        <div style="font-size:2.5rem">
          🌿
        </div>

        <p>
          Loading Dravyaguna
          plant library…
        </p>

      </div>
    `;
  }

  /* =========================================================
     ERROR
  ========================================================= */

  function renderError(
    message
  ) {
    plantList.innerHTML = `
      <div class="plant-error">

        <div style="font-size:2.5rem">
          ⚠️
        </div>

        <h3>
          Unable to load the plant library
        </h3>

        <p>
          ${escapeHTML(
            message
          )}
        </p>

        <button
          type="button"
          id="retry-load"
        >
          Retry
        </button>

      </div>
    `;

    document
      .getElementById(
        "retry-load"
      )
      ?.addEventListener(
        "click",
        loadDatabase
      );
  }

  /* =========================================================
     LOAD DATABASE
  ========================================================= */

  async function loadDatabase() {
    try {
      renderLoading();

      const [
        databaseResponse,
        indexResponse
      ] = await Promise.all([
        fetch(
          databaseURL,
          {
            cache:
              "no-store"
          }
        ),

        fetch(
          indexURL,
          {
            cache:
              "no-store"
          }
        )
      ]);

      if (
        !databaseResponse.ok
      ) {
        throw new Error(
          `plants.json returned HTTP ${databaseResponse.status}`
        );
      }

      if (
        !indexResponse.ok
      ) {
        throw new Error(
          `plant-index.json returned HTTP ${indexResponse.status}`
        );
      }

      const detailedPlants =
        await databaseResponse.json();

      const indexData =
        await indexResponse.json();

      if (
        !Array.isArray(
          detailedPlants
        )
      ) {
        throw new Error(
          "plants.json must contain an array."
        );
      }

      if (
        !indexData ||
        !Array.isArray(
          indexData.plants
        )
      ) {
        throw new Error(
          "plant-index.json must contain a plants array."
        );
      }

      const validDetailed =
        detailedPlants.filter(
          plant =>
            plant &&
            typeof plant.id ===
              "string" &&
            plant.id.trim()
        );

      const validIndex =
        indexData.plants.filter(
          plant =>
            plant &&
            typeof plant.id ===
              "string" &&
            plant.id.trim()
        );

      if (!validIndex.length) {
        throw new Error(
          "plant-index.json contains no valid plant records."
        );
      }

      masterPlants =
        buildMasterList(
          validDetailed,
          validIndex
        );

      renderPlants(
        searchInput?.value ||
          ""
      );

      console.log(
        `DravyaGuna 97 loaded: ${masterPlants.length} plants`
      );

      console.log(
        `Detailed profiles: ${validDetailed.length}`
      );

      console.log(
        `NCISM index records: ${validIndex.length}`
      );

    } catch (error) {
      console.error(
        "Dravyaguna database error:",
        error
      );

      renderError(
        error?.message ||
          "An unexpected error occurred while loading the database."
      );
    }
  }

  /* =========================================================
     SEARCH INPUT
  ========================================================= */

  if (searchInput) {

    searchInput.addEventListener(
      "input",
      event => {
        clearTimeout(
          searchTimer
        );

        const value =
          event.target.value;

        searchTimer =
          setTimeout(
            () => {
              renderPlants(
                value
              );
            },
            80
          );
      }
    );

    searchInput.addEventListener(
      "keydown",
      event => {

        if (
          event.key ===
          "Enter"
        ) {
          event.preventDefault();

          clearTimeout(
            searchTimer
          );

          renderPlants(
            searchInput.value
          );
        }

        if (
          event.key ===
          "Escape"
        ) {
          event.preventDefault();

          clearTimeout(
            searchTimer
          );

          searchInput.value =
            "";

          renderPlants("");

          searchInput.focus();
        }

      }
    );
  }

  /* =========================================================
     START
  ========================================================= */

  if (!plantList) {
    console.warn(
      "Dravyaguna: #plant-list was not found."
    );

    return;
  }

  loadDatabase();
});
