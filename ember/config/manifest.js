/* eslint-env node */
'use strict'

module.exports = function(/* environment, appConfig */) {
  // See https://github.com/san650/ember-web-app#documentation for a list of
  // supported properties

  return {
    name: 'Kanton Schwyz - Bürgerportal',
    short_name: 'Bürgerportal',
    description: 'Bürgerportal für eBau-Gesuche des Kanton Schwyz',
    start_url: '/',
    display: 'standalone',
    background_color: '#FFFFFF',
    theme_color: '#E10A16',
    icons: [
      {
        src: '/assets/images/android-chrome-192x192.png',
        sizes: '192x192'
      },
      {
        src: '/assets/images/android-chrome-512x512.png',
        sizes: '512x512'
      },
      {
        src: '/assets/images/apple-touch-icon.png',
        sizes: '280x280',
        targets: ['apple']
      },
      {
        src: '/assets/images/favicon-16x16.png',
        sizes: '16x16',
        targets: ['favicon']
      },
      {
        src: '/assets/images/favicon-32x32.png',
        sizes: '32x32',
        targets: ['favicon']
      },
      {
        src: '/assets/images/mstile-150x150.png',
        element: 'square150x150logo',
        targets: ['ms']
      },
      {
        src: '/assets/images/safari-pinned-tab.svg',
        safariPinnedTabColor: '#E10A16',
        targets: ['safari-pinned-tab']
      }
    ],
    ms: {
      tileColor: '#FFFFFF'
    }
  }
}
