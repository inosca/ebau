'use strict'

const EmberApp = require('ember-cli/lib/broccoli/ember-app')

module.exports = function(defaults) {
  let app = new EmberApp(defaults, {
    'ember-service-worker': {
      versionStrategy: 'every-build',
      registrationStrategy: 'inline'
    }
  })

  app.import('vendor/leaflet-image.js')
  app.import('node_modules/proj4/dist/proj4.js')
  app.import('node_modules/proj4leaflet/src/proj4leaflet.js')

  return app.toTree()
}
