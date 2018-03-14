'use strict'

const EmberApp = require('ember-cli/lib/broccoli/ember-app')

module.exports = function(defaults) {
  let app = new EmberApp(defaults, {
    jquery: {
      slim: true
    },
    babel: {
      plugins: ['transform-object-rest-spread']
    },
    fingerprint: {
      extensions: ['ico', 'js', 'css', 'png', 'jpg', 'svg']
    },
    emberCliConcat: {
      js: {
        concat: true,
        useAsync: true,
        preserveOriginal: false
      },
      css: {
        concat: true,
        preserveOriginal: false
      }
    },
    'ember-service-worker': {
      versionStrategy: 'every-build',
      registrationStrategy: 'inline'
    },
    'asset-cache': {
      manual: [
        'https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,700'
      ]
    },
    'esw-index': {
      excludeScope: [/manifest.webmanifest$/, /robots.txt$/, /sw.js$/]
    },
    'esw-cache-fallback': {
      patterns: ['https://fonts.gstatic.com/(.+)']
    },
    'ember-app-shell': {
      chromeFlags: ['--no-sandbox'],
      criticalCSSOptions: {
        inline: true,
        ignore: [/font-face/, /font-family/]
      }
    },
    minifyHTML: {
      minifierOptions: {
        minifyJS: false,
        minifyCSS: false,
        ignoreCustomComments: [/^\s*EMBER_APP_SHELL_PLACEHOLDER/]
      }
    }
  })

  app.import('vendor/leaflet-image.js')
  app.import('node_modules/proj4/dist/proj4.js')
  app.import('node_modules/proj4leaflet/src/proj4leaflet.js')

  return app.toTree()
}
