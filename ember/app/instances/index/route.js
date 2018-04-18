import Route from '@ember/routing/route'

export default Route.extend({
  queryParams: {
    group: { refreshModel: true }
  },

  setupController(controller) {
    this._super(...arguments)

    controller.get('instances').perform()
  }
})
