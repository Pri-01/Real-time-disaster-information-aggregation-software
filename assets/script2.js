// Global resource storage
let allResources = [];
const locationCoords = {}; // Geocode cache

// Fetch and process tweet-based data
fetch("/assets/test2.json")
  .then(res => res.json())
  .then(data => {
    const transformed = transformTweetData(data);
    allResources = transformed;
    renderResources(transformed);
    renderTweetList(data);
  })
  .catch(err => console.error("Failed to load JSON:", err));

/******************************************************************
 * 1. TRANSFORMATION LAYER                                         *
 ******************************************************************/

/**
 * Converts raw tweet JSON into a uniform resource list.
 * We only rely on `nerInformation.entities`.
 */
function transformTweetData(tweetData) {
  const resources = [];

  tweetData.forEach(entry => {
    const meta = entry.predictions;
    const type = meta.type; // "need" | "available"
    const location = meta.nerInformation.locations?.[0];
    const entitiesRaw = meta.nerInformation.entities || "";

    if (!location || !entitiesRaw.trim() || type === "NA") return;

    resources.push({
      location,
      entities: entitiesRaw,
      type,
      tweet: entry.tweet
    });
  });

  return resources;
}

/******************************************************************
 * 2.  HELPER UTILITIES                                            *
 ******************************************************************/

// Geocode via Nominatim (cached)
async function getLatLng(location) {
  if (locationCoords[location]) return locationCoords[location];
  try {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}`
    );
    const data = await res.json();
    if (data.length) {
      const coords = [parseFloat(data[0].lat), parseFloat(data[0].lon)];
      locationCoords[location] = coords;
      return coords;
    }
  } catch (err) {
    console.error("Geocode failed:", err);
  }
  return null;
}

// Haversine distance in km
function haversineDistance([lat1, lon1], [lat2, lon2]) {
  const R = 6371;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

/**
 * Extract name & quantity from a raw entity chunk like
 *   "of ORS packets", "of rice 50 kg", "of clean drinking water"
 */
function extractItemDetails(entity) {
  const quantityMatch = entity.match(/(\d+(?:\.\d+)?\s*\w*)/);
  if (quantityMatch) {
    const quantity = quantityMatch[0].trim();
    const name = entity
      .replace(quantity, "")
      .replace(/^of\s+/i, "")
      .trim();
    return { name, quantity };
  }
  return {
    name: entity.trim().replace(/^of\s+/i, ""),
    quantity: "Quantity not mentioned"
  };
}

/**
 * Helper to get individual cleaned entity names from the combined string.
 */
function splitEntityNames(entitiesString) {
  return entitiesString
    .split(",")
    .map(e => extractItemDetails(e).name.toLowerCase())
    .filter(Boolean);
}

/**
 * Flexible name‑matching:
 *  - exact substring check (A in B or B in A)
 *  - ignores plurals like "packet(s)", "kit(s)", generic words (stopwords)
 */
const GENERIC_WORDS = [
  "kg",
  "pack",
  "packs",
  "packet",
  "packets",
  "bottle",
  "bottles",
  "unit",
  "units",
  "piece",
  "pieces",
  "kit",
  "kits",
  "bag",
  "bags"
];

function cleanNameForMatch(name) {
  return name
    .split(/[^a-z0-9]+/i)
    .filter(w => w && !GENERIC_WORDS.includes(w))
    .join(" ");
}

function namesMatch(nameA, nameB) {
  const a = cleanNameForMatch(nameA.toLowerCase());
  const b = cleanNameForMatch(nameB.toLowerCase());

  if (!a || !b) return false;
  return a.includes(b) || b.includes(a);
}

/******************************************************************
 * 3.  RENDERING                                                   *
 ******************************************************************/

function createResourceGroup(location, entities, type, tweet = "") {
  const group = document.createElement("div");
  group.className = "resource-group";

  group.innerHTML = `
    <div class="resource-header"><span class="location">${location}</span></div>
    <div class="tweet-inline">Tweet: ${tweet}</div>
    <div class="resource-items"></div>
  `;

  const itemList = group.querySelector(".resource-items");

  if (entities.trim()) {
    const items = entities.split(",").map(e => e.trim()).filter(Boolean);
    items.forEach((raw) => {
      const { name, quantity } = extractItemDetails(raw);
      itemList.insertAdjacentHTML(
        "beforeend",
        `
        <div class="resource-item">
          <span>${name}</span>
          <span>${quantity}</span>
          <button class="match-btn" data-type="${type}" data-location="${location}" data-resource="${name}">See nearest match</button>
        </div>`
      );
    });
  } else {
    itemList.innerHTML = '<div class="no-items">No items listed</div>';
  }

  return group;
}

function renderResources(data) {
  const needList = document.getElementById("need-list");
  const availList = document.getElementById("available-list");
  needList.innerHTML = availList.innerHTML = "";

  let needed = false,
    available = false;

  data.forEach(entry => {
    const block = createResourceGroup(
      entry.location,
      entry.entities,
      entry.type,
      entry.tweet
    );

    if (entry.type === "need") {
      needList.appendChild(block);
      needed = true;
    } else {
      availList.appendChild(block);
      available = true;
    }
  });

  if (!needed)
    needList.innerHTML = '<div class="no-items">No needed resources</div>';
  if (!available)
    availList.innerHTML = '<div class="no-items">No available resources</div>';
}

function renderTweetList(tweetData) {
  const tweetList = document.querySelector(".tweet-list");
  tweetList.innerHTML = "";
  tweetData.forEach(t => {
    tweetList.insertAdjacentHTML(
      "beforeend",
      `<div class="tweet-card"><p class="tweet-text">${t.tweet}</p></div>`
    );
  });
}

/******************************************************************
 * 4.  MATCH‑FINDING WITH BETTER NAME LOGIC                        *
 ******************************************************************/

document.addEventListener("click", async e => {
  if (!e.target.classList.contains("match-btn")) return;

  const btn = e.target;
  const originType = btn.dataset.type; // need | available (clicked)
  const originLoc = btn.dataset.location;
  const originResource = btn.dataset.resource.toLowerCase();

  const originCoords = await getLatLng(originLoc);
  if (!originCoords) {
    Swal.fire("Location Error", `Couldn't get coordinates for ${originLoc}`, "error");
    return;
  }

  const targetType = originType === "need" ? "available" : "need";
  let nearest = null,
    minDist = Infinity;

  for (const entry of allResources) {
    if (entry.type !== targetType) continue;

    // Does this entry offer/request a matching resource?
    const candidateNames = splitEntityNames(entry.entities);
    const isMatch = candidateNames.some(n => namesMatch(originResource, n));
    if (!isMatch) continue;

    const destCoords = await getLatLng(entry.location);
    if (!destCoords) continue;

    const dist = haversineDistance(originCoords, destCoords);
    if (dist < minDist) {
      minDist = dist;
      nearest = entry;
    }
  }

  if (nearest) {
    Swal.fire({
      title: "Match Found!",
      html: `<b>From:</b> ${originLoc}<br>
             <b>Nearest ${targetType} location:</b> ${nearest.location}<br>
             <b>Distance:</b> ${minDist.toFixed(2)} km<br>
             <b>Resources:</b> ${nearest.entities}`,
      icon: "success"
    });
  } else {
    Swal.fire(
      "No Match",
      `No nearby ${targetType} found for ${originResource}`,
      "info"
    );
  }
});
