import Route from '@ember/routing/route'

export default Route.extend({
  redirect() {
    return this.replaceWith('instances.edit.b.1')
  }
})
