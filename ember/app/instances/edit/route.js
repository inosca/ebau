import Route from '@ember/routing/route'

export default Route.extend({
  model({ instance_id: id }) {
    return this.store.findRecord('instance', id, {
      include: 'form,instance_state'
    })
  }
})
