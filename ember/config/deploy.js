/* eslint-env node */
'use strict'

module.exports = function(deployTarget) {
  let ENV = {
    build: {
      outputPath: 'build'
    },
    compress: {
      keep: true,
      compression: ['gzip', 'brotli']
    }
  }

  if (deployTarget === 'development') {
    ENV.build.environment = 'development'
  }

  if (deployTarget === 'production') {
    ENV.build.environment = 'production'

    ENV.pipeline = {
      activateOnDeploy: true
    }
  }

  return ENV
}
