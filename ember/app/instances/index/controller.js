import Controller from '@ember/controller'
import { task } from 'ember-concurrency'

export default Controller.extend({
  queryParams: ['group'],
  group: null,

  instances: task(function*() {
    return yield this.store.query('instance', {
      // group: this.group,
      include: 'form,instance-state,location'
    })
  }).restartable(),

  navigate: task(function*(instance) {
    let group = this.group

    yield this.transitionToRoute('instances.edit', instance.id, {
      queryParams: group ? { group } : {}
    })
  })
})
