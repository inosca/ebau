'use strict'

const EmberApp = require('ember-cli/lib/broccoli/ember-app')
const env = EmberApp.env()

module.exports = function(defaults) {
  let app = new EmberApp(defaults, {
    jquery: {
      slim: true
    },
    babel: {
      plugins: ['transform-object-rest-spread']
    },
    'ember-cli-babel': {
      includePolyfill: true
    },
    fingerprint: {
      extensions: ['ico', 'js', 'css', 'png', 'jpg', 'svg']
    },
    emberCliConcat: {
      js: {
        concat: true,
        useAsync: true,
        preserveOriginal: env === 'test'
      },
      css: {
        concat: true,
        preserveOriginal: env === 'test'
      }
    },
    imagemin: {
      plugins: [
        require('imagemin-jpegtran')({ progressive: true }),
        require('imagemin-optipng')(),
        require('imagemin-svgo')()
      ]
    },
    'ember-service-worker': {
      versionStrategy: 'every-build',
      registrationStrategy: 'inline'
    },
    'esw-index': {
      excludeScope: [/manifest.webmanifest$/, /robots.txt$/, /sw.js$/]
    },
    'ember-app-shell': {
      chromeFlags: ['--no-sandbox'],
      criticalCSSOptions: {
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

  app.import('vendor/canvas-to-blob-polyfill.js')

  app.import('node_modules/downloadjs/download.min.js', {
    using: [{ transformation: 'amd', as: 'downloadjs' }]
  })

  app.import('node_modules/html2canvas/dist/html2canvas.js', {
    using: [{ transformation: 'amd', as: 'html2canvas' }]
  })

  app.import('node_modules/proj4/dist/proj4.js')
  app.import('node_modules/proj4leaflet/src/proj4leaflet.js')

  return app.toTree()
}
