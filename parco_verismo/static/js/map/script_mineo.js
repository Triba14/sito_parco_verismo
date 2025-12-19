document.addEventListener('DOMContentLoaded', function() {
    // Inizializza la mappa centrata su Mineo
    var map = L.map(document.querySelector(".map-container"), { zoomControl: false }).setView([37.26647353811028, 14.69049488989791], 17);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    L.control.zoom({ position: 'bottomleft' }).addTo(map);

    // Legge le variabili CSS dal tema corrente
    const rootStyles = getComputedStyle(document.documentElement);
    const getColor = (varName) => rootStyles.getPropertyValue(varName).trim();

    // Colori da variabili CSS del tema
    const colors = {
        primary: getColor('--color-primary') || '#4A6741',
        primaryLight: getColor('--color-primary-light') || '#7A9A6F',
        secondary: getColor('--color-secondary') || '#BF9B30',
        secondaryDark: getColor('--color-secondary-dark') || '#8B6F15',
        accent: getColor('--color-accent') || '#A85D3A',
        success: getColor('--color-success') || '#52A770',
        info: getColor('--color-info') || '#3D7A6F',
        warning: getColor('--color-warning') || '#D89020'
    };

    // Funzione per creare icona marker con Bootstrap Icons
    function createMarkerIcon(iconClass, bgColor) {
        return L.divIcon({
            className: 'custom-marker',
            html: `<div class="marker-pin" style="background: ${bgColor};">
                     <i class="bi ${iconClass}"></i>
                   </div>`,
            iconSize: [36, 36],
            iconAnchor: [18, 36],
            popupAnchor: [0, -36]
        });
    }

    // Icone categorie con colori dal tema
    var categoryIcons = {
        "Servizi Pubblici": createMarkerIcon("bi-building-fill", colors.info),
        "Servizi Culturali": createMarkerIcon("bi-bank2", colors.primary),
        "Prodotti Tipici": createMarkerIcon("bi-basket2-fill", colors.secondaryDark),
        "Ospitalità": createMarkerIcon("bi-house-heart-fill", colors.accent),
        "Luoghi Capuaniani": createMarkerIcon("bi-book-fill", colors.secondary),
        "Ristorazione": createMarkerIcon("bi-cup-hot-fill", colors.warning)
    };

    var markers = [];
    var allPointsData = [];

    // Aggiungi marker con link Google Maps
    mineoPoints.forEach(p => {
        allPointsData.push(p);
        if(!p.coords) return;

        // Link Google Maps per il percorso
        var routeLink = `https://www.google.com/maps/dir/?api=1&destination=${p.coords[0]},${p.coords[1]}`;

        // Marker + popup con link percorso
        var m = L.marker(p.coords, {icon: categoryIcons[p.type] || categoryIcons["Servizi Pubblici"]})
                 .bindPopup(`
                    <strong>${p.name}</strong><br>
                    ${p.type}<br><br>
                    <a href="${routeLink}" target="_blank" style="color:#007bff; font-weight:bold;">
                      ➤ Ottieni percorso
                    </a>
                 `);

        m.type = p.type;
        m.name = p.name;
        markers.push(m);
        m.addTo(map);
    });

    // Filtri con centratura automatica
    function filterMarkers(type){
        markers.forEach(m => {
            if(type === "all" || m.type === type){
                if(!map.hasLayer(m)) map.addLayer(m);
            } else {
                if(map.hasLayer(m)) map.removeLayer(m);
            }
        });

        // Centra sui marker visibili
        var visibleMarkers = markers.filter(m => map.hasLayer(m));
        if(visibleMarkers.length > 0){
            var group = new L.featureGroup(visibleMarkers);
            map.fitBounds(group.getBounds().pad(0.1));
        }
    }

    // Gestisci i filtri dal sidebar
    var filterItems = document.querySelectorAll('.filter-item');
    filterItems.forEach(function(item) {
        item.addEventListener('click', function() {
            // Rimuovi active da tutti
            filterItems.forEach(function(el) {
                el.classList.remove('active');
            });
            // Aggiungi active al cliccato
            this.classList.add('active');
            
            var filter = this.getAttribute('data-type');
            filterMarkers(filter);
        });
    });

    // Ricerca live
    const searchBox = document.querySelector(".search-box");
    const searchResults = document.querySelector(".search-results");

    if(searchBox && searchResults) {
        searchBox.addEventListener("input", function(){
            const q = this.value.toLowerCase().trim();
            searchResults.innerHTML = "";
            if(q.length < 2){
                searchResults.style.display = "none";
                return;
            }

            const filtered = allPointsData.filter(p => p.name.toLowerCase().includes(q));

            filtered.forEach(p => {
                const div = document.createElement("div");
                div.className = "search-result-item";
                div.textContent = p.name;
                div.addEventListener("click", function(){
                    if(p.coords) map.setView(p.coords, 18);
                    const m = markers.find(m => m.name === p.name);
                    if(m) m.openPopup();

                    searchBox.value = "";
                    searchResults.style.display = "none";
                });
                searchResults.appendChild(div);
            });

            searchResults.style.display = filtered.length ? "block" : "none";
        });

        document.addEventListener("click", function(e){
            if(!e.target.closest(".search-container")){
                searchResults.style.display = "none";
            }
        });
    }

    // Click su marker centra e zoom
    markers.forEach(m => {
        m.on('click', function(e) {
            map.setView(e.latlng, 17);
        });
    });

    // Fix per rendering della mappa quando diventa visibile
    setTimeout(function() {
        map.invalidateSize();
    }, 100);

    // Observer per quando la sezione mappa diventa visibile
    var mapSection = document.querySelector('.pages-mappa');
    if (mapSection) {
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    map.invalidateSize();
                }
            });
        }, { threshold: 0.1 });
        observer.observe(mapSection);
    }
});
