const plantList = document.getElementById("plant-list");

const plants = [
    {
        id: "ashwagandha",
        name: "Ashwagandha",
        sanskrit_name: "अश्वगन्धा",
        botanical_name: "Withania somnifera",
        family: "Solanaceae"
    },
    {
        id: "guduchi",
        name: "Guduchi",
        sanskrit_name: "गुडूची",
        botanical_name: "Tinospora cordifolia",
        family: "Menispermaceae"
    },
    {
        id: "shatavari",
        name: "Shatavari",
        sanskrit_name: "शतावरी",
        botanical_name: "Asparagus racemosus",
        family: "Asparagaceae"
    }
];


function displayPlants() {

    plantList.innerHTML = "";

    plants.forEach(plant => {

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

        plantList.appendChild(card);

    });
}


displayPlants();
