import Application from '@ember/application'
import { run } from '@ember/runloop'

import { initialize } from 'citizen-portal/initializers/promise'
import { module, test } from 'qunit'
import destroyApp from '../../helpers/destroy-app'

import { Promise } from 'rsvp'

module('Unit | Initializer | promise', {
  beforeEach() {
    run(() => {
      this.application = Application.create()
      this.application.deferReadiness()
    })
  },
  afterEach() {
    destroyApp(this.application)
  }
})

test('it works', function(assert) {
  initialize(this.application)

  assert.equal(window.Promise, Promise)
})
