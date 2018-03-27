import Route from '@ember/routing/route'
import { inject as service } from '@ember/service'
import { v4 } from 'ember-uuid'

export default Route.extend({
  questionStore: service(),

  model() {
    return this.get('questionStore.find').perform(
      'gwr',
      this.modelFor('instances.edit').id
    )
  }
})
