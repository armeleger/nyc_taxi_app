let map;
let markers = [];

window.onload = () => {
  initMap();
};

function initMap() {
  map = L.map('map').setView([40.7128, -74.0060], 12);

  L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    { attribution: '&copy; OpenStreetMap contributors' }
  ).addTo(map);
}

function applyFilters() {
  const start = document.getElementById('filter-start-date').value;
  const end = document.getElementById('filter-end-date').value;
  const minDist = document.getElementById('filter-min-km').value;
  const maxDist = document.getElementById('filter-max-km').value;
  const limit = document.getElementById('filter-record-limit').value;

  // For demo purposes, let's use dummy data instead of a real API
  const dummyTrips = [
    { trip_id: 1, pickup_lat: 40.713, pickup_lon: -74.005, fare_amount: 15.2 },
    { trip_id: 2, pickup_lat: 40.716, pickup_lon: -74.002, fare_amount: 22.5 },
  ];

  const dummyTopRoutes = [
    { route: "Downtown → Uptown", count: 120 },
    { route: "Midtown → Brooklyn", count: 95 },
  ];

  const dummyTopFares = [
    { trip_id: 999, fare_amount: 75.0 },
    { trip_id: 500, fare_amount: 60.0 },
  ];

  const dummySummary = {
    totalTrips: 2,
    avgDistance: 5.5,
    avgFare: 18.85
  };

  updateMap(dummyTrips);
  updateTopRoutes(dummyTopRoutes);
  updateTopFares(dummyTopFares);
  updateSummary(dummySummary);
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
    const marker = L.marker([trip.pickup_lat, trip.pickup_lon]).addTo(map);
    marker.bindPopup(
      `Trip ID: ${trip.trip_id}<br>Fare: $${trip.fare_amount}`
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
