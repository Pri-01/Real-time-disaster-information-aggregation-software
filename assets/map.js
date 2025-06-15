// Initialize Leaflet map centered over India
const map = L.map("map").setView([20.5937, 78.9629], 5);

// Add OpenStreetMap tile layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Cache to avoid redundant geocoding
const locationCache = {};

// Geocode using Nominatim with caching
async function getLatLng(location) {
  if (locationCache[location]) return locationCache[location];

  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}`;
  try {
    const response = await fetch(url);
    const data = await response.json();
    if (data && data.length > 0) {
      const latlng = [parseFloat(data[0].lat), parseFloat(data[0].lon)];
      locationCache[location] = latlng;
      return latlng;
    }
  } catch (err) {
    console.error("Geocoding failed for:", location);
  }
  return null;
}

// Add marker with type-specific icon
async function addMarker(location, type, description) {
  const latlng = await getLatLng(location);
  if (!latlng) return;

  const iconUrl = type === "need"
    ? "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png"
    : "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png";

  const icon = L.icon({
    iconUrl,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [0, -41]
  });

  L.marker(latlng, { icon })
    .addTo(map)
    .bindPopup(`<strong>${type.toUpperCase()}</strong><br>${location}<br>${description}`);
}

// Load tweets from test2.json and add markers
async function loadMarkers() {
  try {
    const res = await fetch("/assets/test2.json");
    const data = await res.json();

    for (const entry of data) {
      const type = entry?.predictions?.type;
      const location = entry?.predictions?.nerInformation?.locations?.[0];
      const tweet = entry.tweet;

      if (!location || (type !== "need" && type !== "available")) continue;

      await addMarker(location, type, tweet);
    }
  } catch (err) {
    console.error("Failed to load map data:", err);
  }
}

// Start loading markers
loadMarkers();
