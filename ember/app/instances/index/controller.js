import Controller from '@ember/controller'
import { task } from 'ember-concurrency'

export default Controller.extend({
  queryParams: ['group'],
  group: null,

  instances: task(function*() {
    return yield this.store.query('instance', {
      group: this.group,
      include: 'form,instance-state,location'
    })
  }).restartable(),

  actions: {
    navigate(instance) {
      this.transitionToRoute('instances.edit', instance.id, {
        queryParams: { group: this.group }
      })
    }
  }
})
