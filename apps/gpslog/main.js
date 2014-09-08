$(document).ready(function() {
  // Create the map
  var map = L.map('map').setView([51.505, -0.09], 13);

  // Create the base map
  L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpg', {
    attribution: ['© OpenStreetMap contributors', 'Tiles Courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">'],
    maxZoom: 18,
    subdomains: '1234',
  }).addTo(map);

  var traceLayer = L.geoJson().addTo(map);

  console.log('Setup complete. Requesting data.');

  // Kick off a request to get the GPS log as a GeoJSON feature collection
  $.getJSON('log', function(data) {
    console.log('Data received. Adding to map.');
    traceLayer.addData(data);
    map.fitBounds(traceLayer.getBounds(), { padding: [10, 10], });
  });
});
