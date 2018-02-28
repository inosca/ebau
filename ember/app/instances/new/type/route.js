import Route from '@ember/routing/route'

const breadCrumb = {
  title: 'Gesuchsart'
}

export default Route.extend({
  breadCrumb,

  beforeModel() {
    return this.store.findAll('form')
  }
})
