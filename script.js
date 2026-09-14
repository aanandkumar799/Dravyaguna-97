const plantList = document.getElementById("plant-list");
const searchInput = document.getElementById("searchInput");

let plants = [];


/* LOAD PLANT DATA */

fetch("plants.json")
    .then(response => response.json())
    .then(data => {

        plants = data;

        displayPlants(plants);

    })
    .catch(error => {

        console.error("Unable to load plant data:", error);

    });


/* DISPLAY PLANTS */

function displayPlants(list) {

    plantList.innerHTML = "";

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


/* SEARCH */

searchInput.addEventListener("input", function() {

    const searchTerm =
        searchInput.value.toLowerCase();

    const filteredPlants = plants.filter(plant =>

        plant.name
            .toLowerCase()
            .includes(searchTerm)

        ||

        plant.botanical_name
            .toLowerCase()
            .includes(searchTerm)

        ||

        plant.family
            .toLowerCase()
            .includes(searchTerm)

    );

    displayPlants(filteredPlants);

});
