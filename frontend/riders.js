let map;
let markers = [];

const API_BASE = 'http://localhost:5000';

window.onload = () => {
  initMap();
  // Initial load
  applyFilters();
};

function initMap() {
  map = L.map('map').setView([40.7128, -74.0060], 12);

  L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    { attribution: '&copy; OpenStreetMap contributors' }
  ).addTo(map);
}

async function applyFilters() {
  const start = document.getElementById('filter-start-date').value;
  const end = document.getElementById('filter-end-date').value;
  const minDist = document.getElementById('filter-min-km').value;
  const maxDist = document.getElementById('filter-max-km').value;
  const limit = document.getElementById('filter-record-limit').value || 100;

  try {
    // Summary
    const sRes = await fetch(`${API_BASE}/api/summary`);
    const sData = await sRes.json();
    updateSummary({
      totalTrips: sData.total_trips ?? 0,
      avgDistance: sData.avg_distance ?? '',
      avgFare: sData.avg_fare_per_km ?? ''
    });

    // Trips
    const params = new URLSearchParams();
    if (start) params.set('start', start);
    if (end) params.set('end', end);
    if (minDist) params.set('min_distance', minDist);
    if (maxDist) params.set('max_distance', maxDist);
    params.set('per_page', limit);

    const tRes = await fetch(`${API_BASE}/api/trips?${params.toString()}`);
    const tData = await tRes.json();
    updateMap(tData.results || []);

    // Placeholder lists until real endpoints exist
    updateTopRoutes([]);
    updateTopFares([]);
  } catch (e) {
    console.error('Failed to load data', e);
  }
}

function updateSummary(summary) {
  document.getElementById('total-trips').innerText = summary.totalTrips;
  document.getElementById('avg-distance').innerText = `${summary.avgDistance} km`;
  document.getElementById('avg-fare').innerText = `$${summary.avgFare}`;
}

function updateMap(trips) {
  markers.forEach(m => map.removeLayer(m));
  markers = [];

  trips.forEach(trip => {
    if (trip.pickup_lat == null || trip.pickup_lon == null) return;
    const marker = L.marker([trip.pickup_lat, trip.pickup_lon]).addTo(map);
    marker.bindPopup(
      `Trip ID: ${trip.id ?? trip.trip_id}<br>Fare: $${trip.fare_amount ?? ''}`
    );
    markers.push(marker);
  });
}

function updateTopRoutes(routes) {
  const list = document.getElementById('top-routes-list');
  list.innerHTML = '';

  routes.forEach(r => {
    const li = document.createElement('li');
    li.textContent = `${r.route} (${r.count} trips)`;
    list.appendChild(li);
  });
}

function updateTopFares(fares) {
  const list = document.getElementById('top-fares-list');
  list.innerHTML = '';

  fares.forEach(f => {
    const li = document.createElement('li');
    li.textContent = `Trip ${f.trip_id}: $${f.fare_amount}`;
    list.appendChild(li);
  });
}
