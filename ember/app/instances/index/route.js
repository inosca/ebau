import Route from '@ember/routing/route'

const breadCrumb = {
  title: 'Ihre Dossiers'
}

export default Route.extend({
  breadCrumb,

  model() {
    return this.store.findAll('instance', {
      include: 'form,instance-state,location'
    })
  }
})
