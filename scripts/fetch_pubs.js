// Run this script via node from the project root.
console.log('Fetching publications...');

var http = require('http'),
    fs = require('fs');

// List of URLs to grab
var PUB_URLS = [
    'http://publications.eng.cam.ac.uk/cgi/exportview/creators/Wareham=3ARJ=3A=3A/JSON/Wareham=3ARJ=3A=3A.js',
    'http://publications.eng.cam.ac.uk/cgi/exportview/creators/Wareham=3AR=3A=3A/JSON/Wareham=3AR=3A=3A.js',
];

var processUrls = function(urls, cb) {
  var pubs = [];
  var processEntry = function(idx) {
    if(idx >= urls.length) { return; }
    var url = urls[idx];
    console.log('GET-ing', url);
    http.get(url, function(res) {
      var json_data = '';
      res.on('data', function(chunk) { json_data += chunk; });
      res.on('end', function() {
        // We use naked evals because the CUED database has some naked unescape-s in them :(
        var parsed_pubs = eval(json_data);
        console.log('Got ' + parsed_pubs.length + ' publication(s)');

        // Do some post-processing
        parsed_pubs.forEach(function(pub) {
          // Parse date
          pub.timestamp = Date.parse(pub.date);
          pub.date = new Date(pub.timestamp).toISOString();

          // Add to output
          pubs.push(pub);
        });

        if(idx+1 < PUB_URLS.length) {
          processEntry(idx+1);
        } else {
          // Sort publications by descending date
          pubs.sort(function(a,b) {
            return b.timestamp - a.timestamp;
          });

          if(cb) { cb(pubs); }
        }
      });
    });
  };

  processEntry(0);
};

processUrls(PUB_URLS, function(pubs) {
  fs.writeFile('publications.json', JSON.stringify(pubs), function() {
    console.log('Wrote ' + pubs.length + ' publications');
  });
});
