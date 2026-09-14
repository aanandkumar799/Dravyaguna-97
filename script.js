const plantList = document.getElementById("plant-list");
const searchInput = document.getElementById("search");

let plants = [];

// Load plant database
fetch("plants.json")
  .then(response => {
    if (!response.ok) {
      throw new Error("Could not load plants.json");
    }

    return response.json();
  })

  .then(data => {

    plants = data;

    displayPlants(plants);

  })

  .catch(error => {

    console.error(error);

    plantList.innerHTML = `
      <p style="color:red;">
        Unable to load plant database.
      </p>
    `;

  });


// Display plants
function displayPlants(list) {

  plantList.innerHTML = "";

  if (list.length === 0) {

    plantList.innerHTML = `
      <p>No plants found.</p>
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
        ${plant.sanskrit_name || ""}
      </p>

      <p>
        <em>${plant.botanical_name || ""}</em>
      </p>

      <p>
        Family: ${plant.family || ""}
      </p>

      <a
        href="plant.html?id=${plant.id}"
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

    const query =
      this.value.toLowerCase().trim();


    const filteredPlants = plants.filter(plant => {

      return (

        (plant.name || "")
          .toLowerCase()
          .includes(query)

        ||

        (plant.sanskrit_name || "")
          .toLowerCase()
          .includes(query)

        ||

        (plant.botanical_name || "")
          .toLowerCase()
          .includes(query)

        ||

        (plant.family || "")
          .toLowerCase()
          .includes(query)

      );

    });


    displayPlants(filteredPlants);

  });

}
