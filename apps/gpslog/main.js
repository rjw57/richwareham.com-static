$(document).ready(function() {
  // Create the map
  var map = L.map('map').setView([51.505, -0.09], 13);

  // Create the base map
  L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpg', {
    attribution: ['© OpenStreetMap contributors', 'Tiles Courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">'],
    maxZoom: 18,
    subdomains: '1234',
  }).addTo(map);

  // The logGeoJSON object is initialised explicitly in the index.html returned
  // from the server.
  var traceLayer = L.geoJson(logGeoJSON).addTo(map);

  // Zoom to fit
  map.fitBounds(traceLayer.getBounds(), { padding: [10, 10], });
});
