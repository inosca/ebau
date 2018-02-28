import Route from '@ember/routing/route'

const breadCrumb = {
  title: 'Dossier bearbeiten'
}

export default Route.extend({
  breadCrumb,

  model({ instance_id: id }) {
    return this.store.findRecord('instance', id, {
      include: 'form,instance_state'
    })
  }
})
