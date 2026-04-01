const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");
const formEl = document.getElementById("search-form");
const inputEl = document.getElementById("city-input");

// Frontend Mapbox token (stored in local file for development)
const MAPBOX_TOKEN = window.MAPBOX_TOKEN || "";

if (!MAPBOX_TOKEN) {
  statusEl.textContent = "Mapbox token missing. Define window.MAPBOX_TOKEN in a local ignored file.";
}

mapboxgl.accessToken = MAPBOX_TOKEN;

const map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/streets-v12",
  center: [13.405, 52.52],
  zoom: 4,
});

let marker = null;

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.style.color = isError ? "crimson" : "#333";
}

function renderResults(items) {
  resultsEl.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.name}${item.country ? ", " + item.country : ""} (${item.latitude.toFixed(3)}, ${item.longitude.toFixed(3)})`;
    li.addEventListener("click", () => focusCity(item));
    resultsEl.appendChild(li);
  });
}

function focusCity(item) {
  const lngLat = [item.longitude, item.latitude];
  map.flyTo({ center: lngLat, zoom: 9 });

  if (marker) marker.remove();
  marker = new mapboxgl.Marker().setLngLat(lngLat).addTo(map);
}

async function searchCities(query) {
  const url = `http://127.0.0.1:8001/cities/search?q=${encodeURIComponent(query)}&limit=5`;
  const res = await fetch(url);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Search failed: ${res.status} ${text}`);
  }
  return res.json();
}

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const query = inputEl.value.trim();
  if (!query) return;

  setStatus("Searching...");
  resultsEl.innerHTML = "";

  try {
    const results = await searchCities(query);
    if (!results.length) {
      setStatus("No matches found.");
      return;
    }

    renderResults(results);
    focusCity(results[0]);
    setStatus(`Found ${results.length} result(s). Click a result to focus.`);
  } catch (err) {
    setStatus(err.message, true);
  }
});