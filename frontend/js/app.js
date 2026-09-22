// Apuntamos a la dirección donde tu FastAPI está corriendo
const API_URL = 'http://127.0.0.1:8000';

// Al cargar la página, traemos los datos de la base de datos
document.addEventListener('DOMContentLoaded', () => {
    loadDevelopers();
    loadGames();
});

// ==========================================
// LÓGICA DE DESARROLLADORES (DEVELOPERS)
// ==========================================
async function loadDevelopers() {
    try {
        // Petición GET a la API
        const response = await axios.get(`${API_URL}/developers/`);
        const developers = response.data;
        
        const devList = document.getElementById('dev-list');
        const selectDev = document.getElementById('game-dev-id');
        
        devList.innerHTML = '';
        // Reseteamos el selector de juegos
        selectDev.innerHTML = '<option value="" disabled selected>Selecciona un desarrollador...</option>';

        developers.forEach(dev => {
            // Pintamos la tarjeta del desarrollador en el DOM
            devList.innerHTML += `
                <div class="item-card">
                    <div class="item-info">
                        <strong>${dev.name}</strong>
                        <p>País: ${dev.country || 'Desconocido'}</p>
                    </div>
                    <button class="btn-delete" onclick="deleteDeveloper(${dev.id})">Borrar</button>
                </div>
            `;
            // Añadimos el desarrollador al select del formulario de videojuegos
            selectDev.innerHTML += `<option value="${dev.id}">${dev.name}</option>`;
        });
    } catch (error) {
        console.error("Error cargando desarrolladores:", error);
    }
}

// Escuchar el evento de crear un nuevo desarrollador
document.getElementById('dev-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Evita que la página se recargue
    const name = document.getElementById('dev-name').value;
    const country = document.getElementById('dev-country').value;

    try {
        // Petición POST a la API
        await axios.post(`${API_URL}/developers/`, { name, country });
        document.getElementById('dev-form').reset();
        loadDevelopers(); // Refrescamos la lista
    } catch (error) {
        alert("Error al crear el desarrollador");
    }
});

// Borrar desarrollador
async function deleteDeveloper(id) {
    if (!confirm('¿Estás seguro? Al borrar el desarrollador también se borrarán sus juegos en cascada.')) return;
    try {
        // Petición DELETE a la API
        await axios.delete(`${API_URL}/developers/${id}`);
        loadDevelopers();
        loadGames(); // Recargamos los juegos porque SQLAlchemy borra en cascada los huérfanos
    } catch (error) {
        alert("Error al borrar el desarrollador");
    }
}

// ==========================================
// LÓGICA DE VIDEOJUEGOS (GAMES)
// ==========================================
async function loadGames() {
    try {
        const response = await axios.get(`${API_URL}/games/`);
        const games = response.data;
        const gameList = document.getElementById('game-list');
        
        gameList.innerHTML = '';

        games.forEach(game => {
            gameList.innerHTML += `
                <div class="item-card">
                    <div class="item-info">
                        <strong>${game.title}</strong>
                        <p>Género: ${game.genre} | Año: ${game.release_year}</p>
                    </div>
                    <button class="btn-delete" onclick="deleteGame(${game.id})">Borrar</button>
                </div>
            `;
        });
    } catch (error) {
        console.error("Error cargando videojuegos:", error);
    }
}

// Crear videojuego
document.getElementById('game-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const release_year = parseInt(document.getElementById('game-year').value);
    const developer_id = parseInt(document.getElementById('game-dev-id').value);

    try {
        await axios.post(`${API_URL}/games/`, { title, genre, release_year, developer_id });
        document.getElementById('game-form').reset();
        loadGames();
    } catch (error) {
        alert("Error al crear el videojuego. Asegúrate de completar todos los campos.");
    }
});

// Borrar videojuego
async function deleteGame(id) {
    if (!confirm('¿Borrar este juego?')) return;
    try {
        await axios.delete(`${API_URL}/games/${id}`);
        loadGames();
    } catch (error) {
        alert("Error al borrar el juego");
    }
}