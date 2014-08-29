module.exports = function(grunt) {
  // Project configuration.
  grunt.initConfig({

    pkg: grunt.file.readJSON('package.json'),
    jekyllConfig: grunt.file.readYAML('_config.yml'),

    jekyll: {
      build: {
      },
      serve: {
        options: {
          watch: true,
        }
      }
    },

    vulcanize: {
      options: {
        strip: true,
        csp: false,
        inline: true
      },
      build: {
        files: {
          'elements/elements.vulcanized.html': 'elements/elements.html'
        },
      }
    },

    watch: {
      elements: {
        files: ['elements/**/*.html'],
        tasks: ['vulcanize'],
        options: {
          spawn: false,
        }
      }
    },

    concurrent: {
      options: {
        logConcurrentOutput: true,
        limit: 5
      },
      target1: [
        'vulcanize',
        'watch'
      ]
    },

  });

  // Fetch publications task
  grunt.registerTask('fetchpubs', function() {
    var done = this.async();
    grunt.log.writeln('Fetching publications...');
    // Run this script via node from the project root.

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
        grunt.log.writeln('GET-ing', url);
        http.get(url, function(res) {
          var json_data = '';
          res.on('data', function(chunk) { json_data += chunk; });
          res.on('end', function() {
            // We use naked evals because the CUED database has some naked unescape-s in them :(
            var parsed_pubs = eval(json_data);
            grunt.log.writeln('Got ' + parsed_pubs.length + ' publication(s)');

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
        grunt.log.writeln('Wrote ' + pubs.length + ' publications');
        done(true);
      });
    });
  });

  // Plugin and grunt tasks.
  require('load-grunt-tasks')(grunt);

  // Default task
  // Task to run vulcanize, jekyll, app engine server, compass watch, vulcanize watch
  grunt.registerTask('default', ['concurrent']);

  // Task to run vulcanize and build the jekyll site
  grunt.registerTask('build', ['fetchpubs', 'vulcanize', 'jekyll:build']);
};
