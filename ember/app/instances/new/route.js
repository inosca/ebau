import Route from '@ember/routing/route'

const breadCrumb = {
  title: 'Neues Dossier erstellen'
}

export default Route.extend({
  breadCrumb,

  model() {
    return this.store.createRecord('instance')
  }
})
