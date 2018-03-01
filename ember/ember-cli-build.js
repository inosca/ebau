'use strict'

const EmberApp = require('ember-cli/lib/broccoli/ember-app')

module.exports = function(defaults) {
  let app = new EmberApp(defaults, {
    babel: {
      plugins: ['transform-object-rest-spread']
    },
    emberCliConcat: {
      js: {
        concat: true,
        useAsync: true
      },
      css: {
        concat: true
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
    'esw-cache-fallback': {
      patterns: ['https://fonts.gstatic.com/(.+)']
    }
  })

  app.import('vendor/leaflet-image.js')
  app.import('node_modules/proj4/dist/proj4.js')
  app.import('node_modules/proj4leaflet/src/proj4leaflet.js')

  return app.toTree()
}
