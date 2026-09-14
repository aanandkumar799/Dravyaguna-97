const plantList = document.getElementById("plant-list");
const searchInput = document.getElementById("searchInput");

let plants = [];


/* =========================
   LOAD PLANT DATA
========================= */

fetch("plants.json")
    .then(response => {

        if (!response.ok) {
            throw new Error("plants.json could not be loaded");
        }

        return response.json();

    })
    .then(data => {

        plants = data;

        displayPlants(plants);

    })
    .catch(error => {

        console.error("Unable to load plant data:", error);

        plantList.innerHTML = `
            <p style="text-align:center;">
                Unable to load plant data.
            </p>
        `;

    });


/* =========================
   DISPLAY PLANTS
========================= */

function displayPlants(list) {

    plantList.innerHTML = "";

    if (list.length === 0) {

        plantList.innerHTML = `
            <p style="text-align:center;">
                No plants found.
            </p>
        `;

        return;
    }


    list.forEach(plant => {

        const card = document.createElement("div");

        card.className = "user-card";

        card.innerHTML = `

            <div class="icon">🌿</div>

            <h2>${plant.name}</h2>

            <p>
                ${plant.botanical_name}
            </p>

            <p>
                Family: ${plant.family}
            </p>

            <a
                href="plants/${plant.id}.html"
                class="plant-button"
            >
                View Plant →
            </a>

        `;

        /* IMPORTANT */
        plantList.appendChild(card);

    });

}


/* =========================
   SEARCH
========================= */

searchInput.addEventListener("input", function() {

    const searchTerm =
        searchInput.value.toLowerCase().trim();


    const filteredPlants = plants.filter(plant => {

        return (

            (plant.name || "")
                .toLowerCase()
                .includes(searchTerm)

            ||

            (plant.botanical_name || "")
                .toLowerCase()
                .includes(searchTerm)

            ||

            (plant.family || "")
                .toLowerCase()
                .includes(searchTerm)

            ||

            (plant.sanskrit_name || "")
                .toLowerCase()
                .includes(searchTerm)

        );

    });


    displayPlants(filteredPlants);

});
