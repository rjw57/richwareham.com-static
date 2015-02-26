$(document).ready(function() {
  // Create the map
  var map = L.map('map').setView([51.505, -0.09], 13);

  // Create the base map
  L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: ['© OpenStreetMap contributors',],
    maxZoom: 18,
    subdomains: 'ab',
  }).addTo(map);

  // The logGeoJSON object is initialised explicitly in the index.html returned
  // from the server.
  var traceLayer = L.geoJson(logGeoJSON).addTo(map);

  // Zoom to fit
  map.fitBounds(traceLayer.getBounds(), { padding: [10, 10], });
});
