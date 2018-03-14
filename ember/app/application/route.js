import Route from '@ember/routing/route'
import { inject as service } from '@ember/service'
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin'

export default Route.extend(ApplicationRouteMixin, {
  intl: service(),

  beforeModel() {
    this._super(...arguments)

    return this.get('intl').setLocale('de-ch')
  }
})
