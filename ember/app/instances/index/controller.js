import Controller from '@ember/controller'
import { task } from 'ember-concurrency'

export default Controller.extend({
  instances: task(function*() {
    return yield this.store.findAll('instance', {
      include: 'form,instance-state,location'
    })
  }).restartable()
})
