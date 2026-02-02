// ================================================
// ITINERARI CAPUANIANI - GESTIONE MAPPA INTERATTIVA
// Sistema ottimizzato con percorsi pre-calcolati (ZERO chiamate API)
// ================================================

(function() {
    'use strict';
    
    let map = null;
    let markersLayer = null;
    let routesLayer = null;
    let currentItinerario = null;
    
    document.addEventListener('DOMContentLoaded', function() {
        initMap();
        setupEventListeners();
        setupPopupEventDelegation();
    });
    
    function initMap() {
        const defaultCenter = [37.5, 14.7];
        const defaultZoom = 9;
        
        map = L.map('map', {
            center: defaultCenter,
            zoom: defaultZoom,
            zoomControl: true
        });
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18
        }).addTo(map);
        
        markersLayer = L.layerGroup().addTo(map);
        routesLayer = L.layerGroup().addTo(map);
        
        // NON mostrare i marker all'inizio - mappa vuota
    }
    
    function setupEventListeners() {
        const cards = document.querySelectorAll('.itinerario-card');
        
        cards.forEach(card => {
            const showBtn = card.querySelector('.btn-show-route');
            const infoBtn = card.querySelector('.btn-info-itinerario');
            
            if (showBtn) {
                showBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const scriptTag = card.querySelector('script.itinerario-data');
                    if (!scriptTag) return;
                    
                    const itinerarioData = JSON.parse(scriptTag.textContent);
                    showItinerarioOnMap(itinerarioData, card);
                });
            }
            
            if (infoBtn) {
                infoBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const scriptTag = card.querySelector('script.itinerario-data');
                    if (!scriptTag) return;
                    
                    const itinerarioData = JSON.parse(scriptTag.textContent);
                    openItinerarioInfoModal(itinerarioData);
                });
            }
        });
        
        const resetBtn = document.getElementById('resetMapView');
        if (resetBtn) {
            resetBtn.addEventListener('click', resetMapView);
        }
        
        const closeInfoBtn = document.getElementById('closeInfoBox');
        if (closeInfoBtn) {
            closeInfoBtn.addEventListener('click', function() {
                document.getElementById('mapInfoBox').classList.add('d-none');
            });
        }
    }
    
    function setupPopupEventDelegation() {
        // Event delegation globale per gestire i click sui bottoni info nei popup
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('tappa-info-btn') || e.target.closest('.tappa-info-btn')) {
                const btn = e.target.classList.contains('tappa-info-btn') ? e.target : e.target.closest('.tappa-info-btn');
                
                const tappaIndex = btn.dataset.tappaIndex;
                const tappaNome = btn.dataset.tappaNome;
                const tappaDescrizione = btn.dataset.tappaDescrizione;
                const itinerarioTitolo = btn.dataset.itinerarioTitolo;
                
                // Ottieni le coordinate della tappa dal dataset o dal currentItinerario
                if (currentItinerario && currentItinerario.coordinate_tappe) {
                    const tappaCoords = currentItinerario.coordinate_tappe[tappaIndex].coords;
                    openTappaModal(tappaNome, tappaDescrizione, itinerarioTitolo, parseInt(tappaIndex) + 1, tappaCoords);
                }
            }
        });
    }
    
    function showAllItinerari() {
        const cards = document.querySelectorAll('.itinerario-card');
        const allBounds = [];
        
        cards.forEach(card => {
            try {
                const scriptTag = card.querySelector('script.itinerario-data');
                if (!scriptTag) return;
                
                const itinerarioData = JSON.parse(scriptTag.textContent);
                if (itinerarioData.coordinate_tappe && itinerarioData.coordinate_tappe.length > 0) {
                    itinerarioData.coordinate_tappe.forEach((tappa, index) => {
                        if (tappa.coords && tappa.coords.length >= 2) {
                            const marker = createMarker(tappa, itinerarioData, index);
                            markersLayer.addLayer(marker);
                            allBounds.push(tappa.coords);
                        }
                    });
                }
            } catch (e) {
                console.error('Errore parsing:', e);
            }
        });
        
        if (allBounds.length > 0) {
            map.fitBounds(allBounds, { padding: [50, 50] });
        }
    }
    
    function showItinerarioOnMap(itinerarioData, cardElement) {
        document.querySelectorAll('.itinerario-card').forEach(c => {
            c.classList.remove('active');
        });
        
        if (cardElement) {
            cardElement.classList.add('active');
        }
        
        markersLayer.clearLayers();
        routesLayer.clearLayers();
        
        currentItinerario = itinerarioData;
        
        if (!itinerarioData.coordinate_tappe || itinerarioData.coordinate_tappe.length === 0) {
            alert('Questo itinerario non ha tappe definite.');
            return;
        }
        
        const bounds = [];
        
        itinerarioData.coordinate_tappe.forEach((tappa, index) => {
            if (tappa.coords && tappa.coords.length >= 2) {
                const marker = createMarker(tappa, itinerarioData, index);
                markersLayer.addLayer(marker);
                bounds.push(tappa.coords);
            }
        });
        
        drawPreCalculatedRoutes(itinerarioData);
        
        if (bounds.length > 0) {
            map.fitBounds(bounds, { padding: [50, 50], maxZoom: 16 });
        }
        
        if (window.innerWidth < 992) {
            document.getElementById('map')?.scrollIntoView({ behavior: 'smooth' });
        }
        
        showInfoBox(itinerarioData);
    }
    
    function drawPreCalculatedRoutes(itinerarioData) {
        const percorsi = itinerarioData.percorsi_calcolati;
        
        if (!percorsi || Object.keys(percorsi).length === 0) {
            console.warn('Nessun percorso pre-calcolato');
            drawStraightLines(itinerarioData);
            return;
        }
        
        console.log(`✓ Carico ${Object.keys(percorsi).length} percorsi pre-calcolati`);
        
        Object.keys(percorsi).forEach(key => {
            const percorso = percorsi[key];
            
            const routeLine = L.polyline(percorso.coords, {
                color: '#4A6741',
                weight: 4,
                opacity: 0.8,
                smoothFactor: 1,
                dashArray: percorso.tratteggiato ? '10, 10' : null
            });
            
            if (percorso.distance && percorso.duration) {
                const distanceKm = (percorso.distance / 1000).toFixed(2);
                const durationMin = (percorso.duration / 60).toFixed(0);
                routeLine.bindTooltip(
                    `<div class="route-tooltip">${distanceKm} km - ${durationMin} min</div>`,
                    { permanent: false, direction: 'center', opacity: 1, className: 'route-tooltip-wrapper' }
                );
            }
            
            routesLayer.addLayer(routeLine);
        });
    }
    
    function drawStraightLines(itinerarioData) {
        const tappe = itinerarioData.coordinate_tappe;
        
        for (let i = 0; i < tappe.length - 1; i++) {
            const start = tappe[i].coords;
            const end = tappe[i + 1].coords;
            const isDashed = tappe[i + 1].tratteggiato || false;
            
            const straightLine = L.polyline([start, end], {
                color: '#4A6741',
                weight: 4,
                opacity: 0.6,
                dashArray: isDashed ? '10, 10' : null
            });
            
            routesLayer.addLayer(straightLine);
        }
    }
    
    function createMarker(tappa, itinerarioData, index) {
        const markerIcon = L.divIcon({
            className: 'custom-marker-icon',
            html: `
                <div class="marker-pin">
                    <span class="marker-number">${tappa.order || index + 1}</span>
                </div>
            `,
            iconSize: [32, 32],
            iconAnchor: [16, 16],
            popupAnchor: [0, -20]
        });
        
        const marker = L.marker(tappa.coords, { icon: markerIcon });
        
        const popupContent = `
            <div class="custom-popup">
                <h5 class="mb-2">
                    <span class="badge bg-success me-1">${tappa.order || index + 1}</span>
                    ${tappa.nome}
                </h5>
                ${tappa.descrizione_breve ? `<p class="mb-2 small">${tappa.descrizione_breve}</p>` : ''}
                <button class="btn btn-sm btn-primary w-100 tappa-info-btn" 
                        data-tappa-index="${index}"
                        data-tappa-nome="${tappa.nome.replace(/"/g, '&quot;')}"
                        data-tappa-descrizione="${(tappa.descrizione || '').replace(/"/g, '&quot;')}"
                        data-itinerario-titolo="${itinerarioData.titolo.replace(/"/g, '&quot;')}">
                    <i class="bi bi-info-circle me-1"></i>
                    Vedi informazioni
                </button>
            </div>
        `;
        
        marker.bindPopup(popupContent, { maxWidth: 300 });
        
        return marker;
    }
    
    function openItinerarioInfoModal(itinerarioData) {
        document.getElementById('itinerarioInfoModalTitolo').textContent = itinerarioData.titolo;
        
        const modalBody = document.getElementById('itinerarioInfoModalBody');
        
        // Carosello immagini
        let carouselHtml = '';
        if (itinerarioData.galleria_immagini && itinerarioData.galleria_immagini.length > 0) {
            carouselHtml = `
            <div id="itinerarioCarousel" class="carousel slide mb-4" data-bs-ride="carousel">
                <div class="carousel-indicators">
                    ${itinerarioData.galleria_immagini.map((img, index) => `
                        <button type="button" data-bs-target="#itinerarioCarousel" data-bs-slide-to="${index}" 
                                ${index === 0 ? 'class="active" aria-current="true"' : ''} 
                                aria-label="Slide ${index + 1}"></button>
                    `).join('')}
                </div>
                <div class="carousel-inner" style="border-radius: 8px; overflow: hidden;">
                    ${itinerarioData.galleria_immagini.map((img, index) => `
                        <div class="carousel-item ${index === 0 ? 'active' : ''}">
                            <img src="${img}" class="d-block w-100" alt="Immagine ${index + 1}" 
                                 style="height: 400px; object-fit: cover;">
                        </div>
                    `).join('')}
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#itinerarioCarousel" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Precedente</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#itinerarioCarousel" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Successiva</span>
                </button>
            </div>
            `;
        }
        
        modalBody.innerHTML = `
            ${carouselHtml}
            
            <div class="mb-4">
                <div class="d-flex align-items-start gap-3 mb-3">
                    <div class="flex-fill">
                        <h5 class="mb-2">${itinerarioData.titolo}</h5>
                        <div class="d-flex gap-2 flex-wrap mb-3">
                            <span class="badge bg-success">
                                <i class="bi bi-geo-alt me-1"></i>
                                ${itinerarioData.coordinate_tappe?.length || 0} tappe
                            </span>
                            <span class="badge bg-primary">
                                <i class="bi bi-clock me-1"></i>
                                ${itinerarioData.durata_stimata || 'Non specificata'}
                            </span>
                            <span class="badge bg-info">
                                <i class="bi bi-signal me-1"></i>
                                ${itinerarioData.difficolta || 'Media'}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mb-4">
                <h6 class="text-muted mb-3">
                    <i class="bi bi-info-circle-fill me-2"></i>
                    Descrizione
                </h6>
                <p class="lead" style="white-space: pre-line;">${itinerarioData.descrizione || 'Nessuna descrizione disponibile.'}</p>
                
                ${itinerarioData.link_maps ? `
                <div class="mt-3">
                    <a href="${itinerarioData.link_maps}" target="_blank" class="btn btn-outline-primary">
                        <i class="bi bi-map-fill me-2"></i>
                        Vedi percorso su Google Maps
                    </a>
                </div>
                ` : ''}
            </div>
            
            ${itinerarioData.coordinate_tappe && itinerarioData.coordinate_tappe.length > 0 ? `
            <div class="mb-3">
                <h6 class="text-muted mb-3">
                    <i class="bi bi-signpost-2 me-2"></i>
                    Tappe del percorso
                </h6>
                <div class="list-group">
                    ${itinerarioData.coordinate_tappe.map((tappa, index) => `
                        <div class="list-group-item">
                            <div class="d-flex align-items-start gap-2">
                                <span class="badge bg-success" style="min-width: 30px;">${tappa.order || index + 1}</span>
                                <div class="flex-fill">
                                    <h6 class="mb-1">${tappa.nome}</h6>
                                    ${tappa.descrizione_breve ? `<p class="mb-0 small text-muted">${tappa.descrizione_breve}</p>` : ''}
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('itinerarioInfoModal'));
        modal.show();
    }
    
    function openTappaModal(nome, descrizione, itinerarioTitolo, numero, coords) {
        document.getElementById('tappaModalTitolo').textContent = `Tappa ${numero}: ${nome}`;
        
        const lat = coords[0];
        const lng = coords[1];
        
        const modalBody = document.getElementById('tappaModalBody');
        modalBody.innerHTML = `
            <div class="mb-3">
                <div class="alert alert-light border">
                    <i class="bi bi-map me-2 text-success"></i>
                    <strong>Itinerario:</strong> ${itinerarioTitolo}
                </div>
            </div>
            <div class="mb-3">
                <h6 class="text-muted mb-3">
                    <i class="bi bi-info-circle-fill me-2"></i>
                    Descrizione della tappa
                </h6>
                <p class="lead" style="white-space: pre-line;">${descrizione || 'Nessuna descrizione disponibile per questa tappa.'}</p>
            </div>
            <div class="mt-4">
                <a href="https://www.google.com/maps?q=${lat},${lng}" 
                   target="_blank" 
                   class="btn btn-outline-success btn-sm">
                    <i class="bi bi-map me-1"></i>
                    Apri in Google Maps
                </a>
            </div>
        `;
        
        // Apri il modale usando Bootstrap
        const modal = new bootstrap.Modal(document.getElementById('tappaModal'));
        modal.show();
    }
    
    function showInfoBox(itinerarioData) {
        const infoBox = document.getElementById('mapInfoBox');
        const infoContent = document.getElementById('mapInfoContent');
        
        if (!infoBox || !infoContent) return;
        
        const html = `
            <div class="info-box-content">
                <div class="d-flex align-items-center mb-3">
                    <span class="fs-2 me-3">${itinerarioData.icona_percorso || '📍'}</span>
                    <div>
                        <h4 class="mb-1">${itinerarioData.titolo}</h4>
                        <span class="badge bg-secondary">${itinerarioData.difficolta}</span>
                    </div>
                </div>
                <div class="d-flex gap-2 mb-3 flex-wrap">
                    <span class="badge bg-primary">
                        <i class="bi bi-geo-alt"></i>
                        ${itinerarioData.coordinate_tappe.length} tappe
                    </span>
                    <span class="badge bg-info">
                        <i class="bi bi-clock"></i>
                        ${itinerarioData.durata_stimata}
                    </span>
                </div>
                <a href="${itinerarioData.url_detail}" class="btn btn-primary btn-sm w-100">
                    Vedi dettagli
                </a>
            </div>
        `;
        
        infoContent.innerHTML = html;
        infoBox.classList.remove('d-none');
    }
    
    function resetMapView() {
        document.querySelectorAll('.itinerario-card').forEach(c => {
            c.classList.remove('active');
        });
        
        document.getElementById('mapInfoBox')?.classList.add('d-none');
        
        markersLayer.clearLayers();
        routesLayer.clearLayers();
        
        currentItinerario = null;
        
        // Ritorna alla vista iniziale (mappa vuota)
        map.setView([37.5, 14.7], 9);
    }
    
})();
