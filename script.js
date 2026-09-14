alert("DravyaGuna JavaScript is running!");

const plantList = document.getElementById("plant-list");

plantList.innerHTML = `
    <div class="user-card">
        <div class="icon">🌿</div>
        <h2>Ashwagandha</h2>
        <p>Withania somnifera</p>
        <p>Family: Solanaceae</p>
    </div>

    <div class="user-card">
        <div class="icon">🌿</div>
        <h2>Guduchi</h2>
        <p>Tinospora cordifolia</p>
        <p>Family: Menispermaceae</p>
    </div>

    <div class="user-card">
        <div class="icon">🌿</div>
        <h2>Shatavari</h2>
        <p>Asparagus racemosus</p>
        <p>Family: Asparagaceae</p>
    </div>
`;
