import Route from '@ember/routing/route'

export default Route.extend({
  beforeModel() {
    return this.store.findAll('form')
  },

  model() {
    return this.store.createRecord('instance')
  }
})
