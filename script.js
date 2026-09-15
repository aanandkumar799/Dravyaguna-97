document.addEventListener("DOMContentLoaded", function () {

    const plantList = document.getElementById("plant-list");
    const searchInput = document.getElementById("search");

    if (!plantList) {
        console.error("plant-list not found");
        return;
    }

    let plants = [];

    // ============================
    // LOAD DATABASE
    // ============================

    fetch("./plants.json?v=10", {
        cache: "no-store"
    })

    .then(function (response) {

        if (!response.ok) {
            throw new Error(
                "Cannot load plants.json. HTTP " +
                response.status
            );
        }

        return response.json();

    })

    .then(function (data) {

        if (!Array.isArray(data)) {
            throw new Error(
                "plants.json must contain a JSON array."
            );
        }

        plants = data;

        console.log(
            "Plant database loaded:",
            plants
        );

        displayPlants(plants);

    })

    .catch(function (error) {

        console.error(
            "Database error:",
            error
        );

        plantList.innerHTML = `
            <div class="database-error">

                <h3>
                    ⚠️ Unable to load plant database
                </h3>

                <p>
                    ${error.message}
                </p>

            </div>
        `;

    });


    // ============================
    // DISPLAY PLANTS
    // ============================

    function displayPlants(list) {

        plantList.innerHTML = "";

        if (!list.length) {

            plantList.innerHTML = `
                <div class="no-results">

                    <h3>
                        🌿 No plants found
                    </h3>

                    <p>
                        Try another search term.
                    </p>

                </div>
            `;

            return;
        }


        list.forEach(function (plant) {

            const card =
                document.createElement("article");

            card.className = "plant-card";


            let imageHTML = "";

            if (
                plant.images &&
                plant.images.whole_plant
            ) {

                imageHTML = `
                    <img
                        src="${plant.images.whole_plant}"
                        alt="${plant.name || "Plant"}"
                        class="plant-card-image"
                        onerror="this.style.display='none'"
                    >
                `;

            } else {

                imageHTML = `
                    <div class="plant-card-placeholder">
                        🌿
                    </div>
                `;

            }


            card.innerHTML = `

                ${imageHTML}

                <div class="plant-card-content">

                    <h2>
                        ${plant.name || "Unnamed Plant"}
                    </h2>

                    <p class="sanskrit-name">
                        ${plant.sanskrit_name || ""}
                    </p>

                    <p class="botanical-name">
                        ${plant.botanical_name || ""}
                    </p>

                    <p>
                        <strong>Family:</strong>
                        ${plant.family || "-"}
                    </p>

                    <a
    href="plant.html?id=${plant.id}"
    class="plant-button"
>
    View Plant →
</a>

                </div>

            `;


            plantList.appendChild(card);

        });

    }


    // ============================
    // SEARCH
    // ============================

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            function () {

                const query =
                    searchInput.value
                        .toLowerCase()
                        .trim();


                if (!query) {

                    displayPlants(plants);

                    return;

                }


                const filtered =
                    plants.filter(function (plant) {

                        return [

                            plant.name,
                            plant.sanskrit_name,
                            plant.transliteration,
                            plant.botanical_name,
                            plant.family,
                            plant.english_name,
                            plant.hindi_name

                        ]
                        .filter(Boolean)
                        .some(function (value) {

                            return value
                                .toString()
                                .toLowerCase()
                                .includes(query);

                        });

                    });


                displayPlants(filtered);

            }
        );

    }

});
