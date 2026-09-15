const plantList = document.getElementById("plant-list");
const searchInput = document.getElementById("search");

let plants = [];


// ===============================
// LOAD PLANT DATABASE
// ===============================

fetch("./plants.json")
  .then(function(response) {

    if (!response.ok) {
      throw new Error(
        "Database HTTP error: " + response.status
      );
    }

    return response.json();

  })

  .then(function(data) {

    console.log("Plant database loaded:", data);

    plants = data;

    displayPlants(plants);

  })

  .catch(function(error) {

    console.error("Database loading error:", error);

    if (plantList) {

      plantList.innerHTML = `
        <div style="
          padding:20px;
          background:#ffe6e6;
          border:1px solid #cc0000;
          border-radius:12px;
          color:#990000;
        ">
          <h3>Unable to load plant database</h3>
          <p>${error.message}</p>
        </div>
      `;

    }

  });


// ===============================
// DISPLAY PLANTS
// ===============================

function displayPlants(list) {

  if (!plantList) {
    console.error("plant-list element not found.");
    return;
  }

  plantList.innerHTML = "";

  if (!list || list.length === 0) {

    plantList.innerHTML = `
      <p>No plants found.</p>
    `;

    return;
  }


  list.forEach(function(plant) {

    const card = document.createElement("div");

    card.className = "user-card";


    card.innerHTML = `

      <div class="icon">🌿</div>

      <h2>
        ${plant.name || ""}
      </h2>

      <p>
        ${plant.sanskrit_name || ""}
      </p>

      <p>
        <em>
          ${plant.botanical_name || ""}
        </em>
      </p>

      <p>
        Family:
        ${plant.family || ""}
      </p>

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


// ===============================
// SEARCH
// ===============================

if (searchInput) {

  searchInput.addEventListener(
    "input",
    function() {

      const query =
        this.value.toLowerCase().trim();


      const filteredPlants = plants.filter(
        function(plant) {

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

        }
      );


      displayPlants(filteredPlants);

    }
  );

}
