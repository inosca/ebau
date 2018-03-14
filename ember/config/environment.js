'use strict'

module.exports = function(environment) {
  let ENV = {
    modulePrefix: 'citizen-portal',
    environment,
    rootURL: '/',
    locationType: 'auto',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    },

    exportApplicationGlobal: true,

    'ember-simple-auth-oidc': {
      authEndpoint:
        'http://camac-ng-ember.local/auth/realms/ebau/protocol/openid-connect/auth',
      tokenEndpoint:
        'http://camac-ng-ember.local/auth/realms/ebau/protocol/openid-connect/token',
      logoutEndpoint:
        'http://camac-ng-ember.local/auth/realms/ebau/protocol/openid-connect/logout',
      clientId: 'portal'
    }
  }

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.locationType = 'none'

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false
    ENV.APP.LOG_VIEW_LOOKUPS = false

    ENV.APP.rootElement = '#ember-testing'
    ENV.APP.autoboot = false

    ENV['ember-simple-auth-oidc'] = {
      authEndpoint: '/auth/realms/ebau/protocol/openid-connect/auth',
      tokenEndpoint: '/auth/realms/ebau/protocol/openid-connect/token',
      logoutEndpoint: '/auth/realms/ebau/protocol/openid-connect/logout'
    }
  }

  if (environment === 'production') {
    ENV['ember-cli-mirage'] = {
      enabled: process.env.EMBER_CLI_MIRAGE || false
    }
  }

  return ENV
}
