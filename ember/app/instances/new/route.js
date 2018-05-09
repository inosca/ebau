import Route from '@ember/routing/route'

export default Route.extend({
  model() {
    return this.store.createRecord('instance')
  },

  setupController(controller) {
    this._super(...arguments)

    controller.forms.perform()
  }
})
