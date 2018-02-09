import Controller from '@ember/controller'
import { inject as service } from '@ember/service'
import { task } from 'ember-concurrency'

export default Controller.extend({
  session: service(),

  login: task(function*(identification, password) {
    yield this.get('session').authenticate('authenticator:jwt', {
      identification,
      password
    })

    yield this.transitionToRoute('index')
  })
})
