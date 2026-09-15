document.addEventListener("DOMContentLoaded", function () {

    const plantList = document.getElementById("plant-list");
    const searchInput = document.getElementById("search");

    if (!plantList) {
        console.error("plant-list not found");
        return;
    }

    let plants = [];


    // ================================
    // LOAD DATABASE
    // ================================

    fetch("./plants.json?v=6")

        .then(function (response) {

            if (!response.ok) {
                throw new Error(
                    "Cannot load plants.json. HTTP " +
                    response.status
                );
            }

            return response.text();

        })

        .then(function (text) {

            console.log("Raw JSON:", text);

            let data;

            try {

                data = JSON.parse(text);

            } catch (error) {

                throw new Error(
                    "plants.json contains invalid JSON: " +
                    error.message
                );

            }

            if (!Array.isArray(data)) {

                throw new Error(
                    "plants.json must contain a JSON array."
                );

            }

            plants = data;

            displayPlants(plants);

        })

        .catch(function (error) {

            console.error(error);

            plantList.innerHTML = `

                <div style="
                    padding:25px;
                    margin:15px 0;
                    background:#ffe8e8;
                    border:2px solid #d33;
                    border-radius:15px;
                    text-align:center;
                ">

                    <h3>
                        ⚠️ Unable to load plant database
                    </h3>

                    <p>
                        ${error.message}
                    </p>

                </div>

            `;

        });


    // ================================
    // DISPLAY PLANTS
    // ================================

    function displayPlants(list) {

        plantList.innerHTML = "";

        if (list.length === 0) {

            plantList.innerHTML = `
                <p>No plants found.</p>
            `;

            return;
        }


        list.forEach(function (plant) {

            const card =
                document.createElement("div");

            card.className = "user-card";


            card.innerHTML = `

                <div class="icon">
                    🌿
                </div>

                <h2>
                    ${plant.name || "Unnamed Plant"}
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
                    href="./plant.html?id=${encodeURIComponent(
                        plant.id
                    )}"
                    class="plant-button"
                >
                    View Plant →
                </a>

            `;


            plantList.appendChild(card);

        });

    }


    // ================================
    // SEARCH
    // ================================

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            function () {

                const query =
                    this.value
                        .toLowerCase()
                        .trim();


                const filtered =
                    plants.filter(function (plant) {

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


                displayPlants(filtered);

            }
        );

    }

});
